import pygame

from . import NORTH, SOUTH, EAST, WEST
from .AnimationSet import *
from .CharacterEvent import *

class Character:
	def __init__(self, spawn_point):
		self.name = "Generic Character"
		self.sprite = None
		self.rect = pygame.Rect(0, 0, 0, 0)
		self.rect.x = spawn_point.x
		self.rect.y = spawn_point.y
		self.facing_direction = SOUTH
		self.speed = 1
		self.can_slide = False
		self.events = list()

	def __clamp_position(self):
		"""UNUSED: Make sure that the Character stays on the map."""
		self.rect.x = clamp(self.rect.x, map_manager.bounds.left, map_manager.bounds.right - self.rect.w - 1)
		self.rect.y = clamp(self.rect.y, map_manager.bounds.top, map_manager.bounds.bottom - self.rect.h - 1)

	def __slide_position(self, map_manager, delta_x, delta_y):
		"""All of this complication allows the character to slide around corners that would otherwise be hard to navigate using single-pixel movements."""
		tile_left, tile_top, tile_right, tile_bottom = self.rect.left // map_manager.tile_width, self.rect.top // map_manager.tile_height, (self.rect.right - 1) // map_manager.tile_width, (self.rect.bottom - 1) // map_manager.tile_height
		
		slide_speed = 1
		if not self.can_slide:
			slide_speed = 0 # Just reverse collisions, without sliding.

		# Sometimes, the character will not be facing in the direction they are moving.
		if delta_y < 0: # self.facing_direction == NORTH:
			if map_manager.collision_data[tile_top][tile_right] and not map_manager.collision_data[tile_top][tile_left]:
				self.rect.y -= delta_y
				self.rect.x -= slide_speed
			elif map_manager.collision_data[tile_top][tile_left] and not map_manager.collision_data[tile_top][tile_right]:
				self.rect.y -= delta_y
				self.rect.x += slide_speed
			elif map_manager.collision_data[tile_top][tile_left] and map_manager.collision_data[tile_top][tile_right]:
				self.rect.y -= delta_y
		elif delta_y > 0: # self.facing_direction == SOUTH:
			if map_manager.collision_data[tile_bottom][tile_right] and not map_manager.collision_data[tile_bottom][tile_left]:
				self.rect.y -= delta_y
				self.rect.x -= slide_speed
			elif map_manager.collision_data[tile_bottom][tile_left] and not map_manager.collision_data[tile_bottom][tile_right]:
				self.rect.y -= delta_y
				self.rect.x += slide_speed
			elif map_manager.collision_data[tile_bottom][tile_left] and map_manager.collision_data[tile_bottom][tile_right]:
				self.rect.y -= delta_y
		elif delta_x > 0: # self.facing_direction == EAST:
			if map_manager.collision_data[tile_bottom][tile_right] and not map_manager.collision_data[tile_top][tile_right]:
				self.rect.x -= delta_x
				self.rect.y -= slide_speed
			elif map_manager.collision_data[tile_top][tile_right] and not map_manager.collision_data[tile_bottom][tile_right]:
				self.rect.x -= delta_x
				self.rect.y += slide_speed
			elif map_manager.collision_data[tile_top][tile_right] and map_manager.collision_data[tile_bottom][tile_right]:
				self.rect.x -= delta_x
		elif delta_x < 0: # self.facing_direction == WEST:
			if map_manager.collision_data[tile_bottom][tile_left] and not map_manager.collision_data[tile_top][tile_left]:
				self.rect.x -= delta_x
				self.rect.y -= slide_speed
			elif map_manager.collision_data[tile_top][tile_left] and not map_manager.collision_data[tile_bottom][tile_left]:
				self.rect.x -= delta_x
				self.rect.y += slide_speed
			elif map_manager.collision_data[tile_top][tile_left] and map_manager.collision_data[tile_bottom][tile_left]:
				self.rect.x -= delta_x

	def load_sprite(self, sprite):
		self.sprite = sprite.clone()
		old_rect = self.rect
		self.rect = self.sprite.tileset.get_rect()
		self.rect.x = old_rect.x
		self.rect.y = old_rect.y
		self.sprite.animations.set_current(ANIM_STAND_SOUTH)

	def blit(self, screen, map_manager, player_rect):
		SCREEN_CENTER_X = screen.get_width() // 2
		SCREEN_CENTER_Y = screen.get_height() // 2

		tile_left, tile_right, tile_bottom = self.rect.left // map_manager.tile_width, (self.rect.right - 1) // map_manager.tile_width, (self.rect.bottom - 1) // map_manager.tile_height
		if map_manager.is_tile_tall(tile_left, tile_bottom) and map_manager.is_tile_tall(tile_right, tile_bottom):
			self.sprite.tileset.blit_top(screen, self.sprite.animations.tile_index, SCREEN_CENTER_X + self.rect.x - player_rect.x, SCREEN_CENTER_Y + self.rect.y - player_rect.y)
		else:
			self.sprite.tileset.blit(screen, self.sprite.animations.tile_index, SCREEN_CENTER_X + self.rect.x - player_rect.x, SCREEN_CENTER_Y + self.rect.y - player_rect.y)

	def move_by(self, map_manager, delta_x, delta_y):
		position = (self.rect.x, self.rect.y)
		self.rect = self.rect.move(delta_x, delta_y)
		#self.__clamp_position()
		self.__slide_position(map_manager, delta_x, delta_y)

		# Test for character collisions.
		undo_move = False
		collision_rect = self.rect.inflate(-1, -1)
		for npc in map_manager.characters:
			if (npc.character != self) and collision_rect.colliderect(npc.character.rect):
				#print(f"{self.name} crashed into {npc.character.name}.")
				npc.character.events.append(CharacterCollidedEvent(self, delta_x, delta_y))
				undo_move = True

		if undo_move:
			self.rect.x = position[0]
			self.rect.y = position[1]

	def move_north(self, map_manager):
		self.move_by(map_manager, 0, -self.speed)
		self.sprite.animations.set_current(ANIM_WALK_NORTH)
		self.facing_direction = NORTH
	
	def move_south(self, map_manager):
		self.move_by(map_manager, 0, self.speed)
		self.sprite.animations.set_current(ANIM_WALK_SOUTH)
		self.facing_direction = SOUTH

	def move_west(self, map_manager):
		self.move_by(map_manager, -self.speed, 0)
		self.sprite.animations.set_current(ANIM_WALK_WEST)
		self.facing_direction = WEST

	def move_east(self, map_manager):
		self.move_by(map_manager, self.speed, 0)
		self.sprite.animations.set_current(ANIM_WALK_EAST)
		self.facing_direction = EAST

	def stop_moving(self):
		if self.facing_direction == NORTH:
			self.face_north()
		elif self.facing_direction == SOUTH:
			self.face_south()
		elif self.facing_direction == WEST:
			self.face_west()
		elif self.facing_direction == EAST:
			self.face_east()

	def face_north(self):
		self.facing_direction = NORTH
		self.sprite.animations.set_current(ANIM_STAND_NORTH)

	def face_south(self):
		self.facing_direction = SOUTH
		self.sprite.animations.set_current(ANIM_STAND_SOUTH)

	def face_west(self):
		self.facing_direction = WEST
		self.sprite.animations.set_current(ANIM_STAND_WEST)

	def face_east(self):
		self.facing_direction = EAST
		self.sprite.animations.set_current(ANIM_STAND_EAST)
