import pygame
from pygame.locals import *

import pytmx
from pytmx import TiledImageLayer
from pytmx import TiledObjectGroup
from pytmx import TiledTileLayer
from util_pygame import load_pygame

from villagelib import RENDER_SCALE

class TiledRenderer(object):
	"""Super simple way to render a tiled map."""

	def __init__(self, filename):
		tm = load_pygame(filename)

		# self.size will be the pixel size of the map
		# this value is used later to render the entire map to a pygame surface
		self.pixel_size = tm.width * tm.tilewidth * RENDER_SCALE, tm.height * tm.tileheight * RENDER_SCALE
		self.tmx_data = tm
		self.__animated_tiles = self.__collect_animated_tiles()
		self.__dirty_tiles = list()

		# Scale all of the images to fit the window.
		for n in range(len(tm.images)):
			image = tm.images[n]
			if image != None:
				tm.images[n] = pygame.transform.scale(image, (tm.tilewidth * RENDER_SCALE, tm.tileheight * RENDER_SCALE))

	def build_collision_map(self, layer_name):
		"""Build a collision layer, a 2D array of boolean values, based on the contents of the requested layer name."""
		layer = self.tmx_data.get_layer_by_name(layer_name)
		collision_data = list()

		# Build a 2D list that is completely walkable.
		for y in range(0, layer.height):
			collision_data.append(list())
			for x in range(0, layer.width):
				collision_data[y].append(False)

		# Iterate over the existing tiles, and make them blocking.
		for x, y, image in layer.tiles():
			collision_data[y][x] = True

		return collision_data

	def get_object_by_name(self, object_layer_name, object_name):
		layer = self.tmx_data.get_layer_by_name(object_layer_name)
		for obj in layer:
			if obj.name == object_name:
				return obj
		raise Exception(f"Could not find an object named {object_name} in the {object_layer_name} layer.")

	def render_map(self, surface):
		"""Render our map to a pygame surface
		This method expects that the surface passed is the same pixel size as the map."""

		# fill the background color of our render surface
		if self.tmx_data.background_color:
			surface.fill(pygame.Color(self.tmx_data.ackground_color))

		# iterate over all the visible layers, then draw them
		for layer in self.tmx_data.visible_layers:
			# Each layer can be handled differently by checking their type.

			if isinstance(layer, TiledTileLayer):
				self.render_tile_layer(surface, layer)

			elif isinstance(layer, TiledObjectGroup):
				self.render_object_layer(surface, layer)

			elif isinstance(layer, TiledImageLayer):
				self.render_image_layer(surface, layer)

	def render_tile_layer_by_name(self, surface, layer_name):
		"""Render a layer by name."""
		self.render_tile_layer(surface, self.tmx_data.get_layer_by_name(layer_name))

	def render_tile_layer(self, surface, layer):
		"""Render all TiledTiles in this layer."""

		# Dereference these heavily used references for speed.
		tw = self.tmx_data.tilewidth
		th = self.tmx_data.tileheight
		surface_blit = surface.blit
		
		# Iterate over the tiles in the layer, and blit them.
		for x, y, image in layer.tiles():
			tile_point = [x * tw * RENDER_SCALE, y * th * RENDER_SCALE]
			surface_blit(image, tile_point)

	def update_animations(self):
		"""Update the animation timer, and any AnimationFrame object.
		Returns True if there are tiles that need to be re-rendered; otherwise returns False."""
		self.__dirty_tiles.clear()
		current_time = pygame.time.get_ticks()
		for gid in self.__animated_tiles:
			tile_props = self.__animated_tiles[gid]

			frames = tile_props["frames"]
			current_frame = tile_props["current_frame"]
			if (len(frames) > 0) and (current_time - tile_props["last_animate_time"] >= frames[current_frame].duration):
				tile_props["current_frame"] = (current_frame + 1) % len(frames)
				tile_props["last_animate_time"] = current_time
				self.__dirty_tiles.append(gid)
		return len(self.__dirty_tiles) > 0

	def __collect_animated_tiles(self):
		gids = dict()
		for gid in self.tmx_data.gidmap:
			tile_props = self.tmx_data.get_tile_properties_by_gid(gid)
			if tile_props == None:
				continue
			if len(tile_props["frames"]) > 0:
				gids[gid] = tile_props
		return gids

	def render_animation_updates(self, surface, layer):
		"""Update the animation timer, and re-render any tiles that have changed."""

		if type(layer) is str:
			layer = self.tmx_data.get_layer_by_name(layer)

		# Dereference these heavily used references for speed.
		tw = self.tmx_data.tilewidth
		th = self.tmx_data.tileheight
		surface_blit = surface.blit

		# Iterate over the tiles in the layer, and blit them.
		for tile_gid in self.__dirty_tiles:
			tile_props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
			for x, y, gid in [i for i in layer.iter_data() if (i[2] == tile_gid)]:
				image = layer.parent.images[tile_props["frames"][tile_props["current_frame"]].gid]
				tile_point = [x * tw * RENDER_SCALE, y * th * RENDER_SCALE]
				surface_blit(image, tile_point)

	def render_object_layer(self, surface, layer):
		"""Render all TiledObjects contained in this layer."""
		# deref these heavily used references for speed
		draw_rect = pygame.draw.rect
		draw_lines = pygame.draw.lines
		surface_blit = surface.blit

		# These colors are used to draw vector shapes, like polygon and box shapes
		rect_color = (255, 0, 0)
		poly_color = (0, 255, 0)

		# Iterate over all the objects in the layer.
		# These may be Tiled shapes like circles or polygons, GID objects, or Tiled Objects
		for obj in layer:
			# objects with points are polygons or lines
			if hasattr(obj, 'points'):
				draw_lines(surface, poly_color, obj.closed, obj.points, 3)

			# Some objects have an image.  Tiled calls them "GID Objects".
			elif obj.image:
				surface_blit(obj.image, (obj.x * RENDER_SCALE, obj.y * RENDER_SCALE))

				# draw a rect for everything else
				# Mostly, I am lazy, but you could check if it is circle/oval
				# and use pygame to draw an oval here...I just do a rect.
			else:
				draw_rect(surface, rect_color, (obj.x * RENDER_SCALE, obj.y * RENDER_SCALE, obj.width * RENDER_SCALE, obj.height * RENDER_SCALE), 3)

	def render_image_layer(self, surface, layer):
		if layer.image:
			surface.blit(layer.image, (0, 0, layer.image.get_width() * RENDER_SCALE, layer.image.get_height() * RENDER_SCALE)) #, -1 * self.get_offset())
