import pygame

from .MapTransition import *
from .ScriptedCharacterController import *
from .TiledRenderer import *

from . import RENDER_SCALE, ASSETS_PATH

class MapManager:
	def __init__(self, initial_map_name):
		self.map_name = ""
		self.renderer = None
		self.tile_width = 0
		self.tile_height = 0
		self.__ground_layer = None
		self.__ground_decoration_layer = None
		self.__blocking_layer = None
		self.__overhead_layer = None
		self.__ground_surface = None
		self.__ground_decoration_surface = None
		self.__blocking_surface = None
		self.__overhead_surface = None
		self.objects = None
		self.characters = list()
		self.spawn_point = None
		self.transitions = None
		self.collision_data = None
		self.bounds = None

		self.load_map(initial_map_name)

	def __load_surface(self, layer):
		surface = pygame.Surface(self.renderer.pixel_size)
		self.renderer.render_tile_layer(surface, layer)
		surface.set_colorkey((0, 0, 0))
		return surface

	def load_map(self, map_name):
		self.map_name = map_name
		self.renderer = TiledRenderer(ASSETS_PATH + "maps/" + map_name + ".tmx")
		self.tile_width = self.renderer.tmx_data.tilewidth * RENDER_SCALE
		self.tile_height = self.renderer.tmx_data.tileheight * RENDER_SCALE

		self.__ground_layer = self.renderer.tmx_data.get_layer_by_name("Ground")
		self.__ground_decoration_layer = self.renderer.tmx_data.get_layer_by_name("Ground Decoration")
		self.__blocking_layer = self.renderer.tmx_data.get_layer_by_name("Blocking")
		self.__overhead_layer = self.renderer.tmx_data.get_layer_by_name("Overhead")

		self.__ground_surface = self.__load_surface(self.__ground_layer)
		self.__ground_decoration_surface = self.__load_surface(self.__ground_decoration_layer)
		self.__blocking_surface = self.__load_surface(self.__blocking_layer)
		self.__overhead_surface = self.__load_surface(self.__overhead_layer)
		self.objects = self.renderer.tmx_data.get_layer_by_name("Objects")

		self.spawn_point = self.get_object_by_name("Spawn Point")
		self.spawn_point.x *= RENDER_SCALE
		self.spawn_point.y *= RENDER_SCALE
		self.spawn_point.width *= RENDER_SCALE
		self.spawn_point.height *= RENDER_SCALE

		# Collect the transition objects into a useful dictionary.
		self.transitions = list()
		for t_obj in self.get_objects_by_type("TRANSITION"):
			self.transitions.append(MapTransition(t_obj))

		# Collect the script objects into a list.
		self.characters.clear()
		for s_obj in self.get_objects_by_type("SCRIPT"):
			self.characters.append(ScriptedCharacterController(s_obj))

		self.collision_data = self.renderer.build_collision_map("Blocking")
		self.bounds = self.__ground_surface.get_rect()

	def get_object_by_name(self, object_name):
		for obj in self.objects:
			if obj.name == object_name:
				return obj
		raise Exception(f"Could not find an object named {object_name} in the 'Objects' layer.")

	def get_objects_by_type(self, object_type):
		objs = list()
		for obj in self.objects:
			if obj.type == object_type:
				objs.append(obj)
		return objs

	def is_tile_tall(self, tile_x, tile_y):
		props = self.renderer.tmx_data.get_tile_properties(tile_x, tile_y, self.__ground_layer)
		if (props != None) and bool(props.get("Is Deep")):
			return True
		else:
			return False

	def update_animations(self):
		if self.renderer.update_animations():
			self.renderer.render_animation_updates(self.__ground_surface, self.__ground_layer)
			self.renderer.render_animation_updates(self.__ground_decoration_surface, self.__ground_decoration_layer)
			self.renderer.render_animation_updates(self.__blocking_surface, self.__blocking_layer)
			self.renderer.render_animation_updates(self.__overhead_surface, self.__overhead_layer)

	def render_under_sprites(self, screen, player_x, player_y):
		SCREEN_WIDTH = screen.get_width()
		SCREEN_HEIGHT = screen.get_height()
		SCREEN_CENTER_X = SCREEN_WIDTH // 2
		SCREEN_CENTER_Y = SCREEN_HEIGHT // 2

		screen.blit(self.__ground_surface, (0, 0), (player_x - SCREEN_CENTER_X, player_y - SCREEN_CENTER_Y, player_x + SCREEN_WIDTH, player_y + SCREEN_HEIGHT))
		screen.blit(self.__ground_decoration_surface, (0, 0), (player_x - SCREEN_CENTER_X, player_y - SCREEN_CENTER_Y, player_x + SCREEN_WIDTH, player_y + SCREEN_HEIGHT))
		screen.blit(self.__blocking_surface, (0, 0), (player_x - SCREEN_CENTER_X, player_y - SCREEN_CENTER_Y, player_x + SCREEN_WIDTH, player_y + SCREEN_HEIGHT))

	def render_over_sprites(self, screen, player_x, player_y):
		SCREEN_WIDTH = screen.get_width()
		SCREEN_HEIGHT = screen.get_height()
		SCREEN_CENTER_X = screen.get_width() // 2
		SCREEN_CENTER_Y = screen.get_height() // 2

		screen.blit(self.__overhead_surface, (0, 0), (player_x - SCREEN_CENTER_X, player_y - SCREEN_CENTER_Y, player_x + SCREEN_WIDTH, player_y + SCREEN_HEIGHT))
