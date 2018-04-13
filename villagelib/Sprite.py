import pygame

from . import RENDER_SCALE
from .AnimationSet import *
from .TileSet import *

def create_npc_sprite(image_path, colors = None):
	"""
		Create a standard NPC sprite.
	
		colors is an optional length-3 list of RGB values for replacing the primary, secondary, and tertiary colors on the sprite.
			Dark versions of these colors will be calculated automatically as 25% darker than those specified.
	"""
	new_sprite = Sprite()
	new_sprite.tileset = TileSet(image_path, 3, 6)
	new_sprite.tileset.scale(RENDER_SCALE) # Make it twice as big.
	new_sprite.animations = AnimationSet({
		ANIM_STAND_SOUTH: [0],
		ANIM_STAND_NORTH: [3],
		ANIM_STAND_WEST: [6],
		ANIM_STAND_EAST: [9],
		ANIM_WALK_SOUTH: [0, 1, 0, 2],
		ANIM_WALK_NORTH: [3, 4, 3, 5],
		ANIM_WALK_WEST: [6, 7, 6, 8],
		ANIM_WALK_EAST: [9, 10, 9, 11],
		ANIM_RAISE_HAND: [12],
		ANIM_WAVE: [12, 13],
		ANIM_SAD: [15],
		ANIM_NOD: [0, 15],
		ANIM_DIE: [17]
	})
	new_sprite.animations.speed = 300

	if colors != None:
		# This magic is possible because all of the sprites use a standard palette for replaceable colors.
		new_sprite.recolor_image((
			(255, 0, 0),	# primary
			(127, 0, 0),	# primary-dark
			(255, 255, 0),	# secondary
			(127, 127, 0),	# secondary-dark
			(248, 152, 96),	# tertiary
			(216, 120, 16)	# tertiary-dark
		), colors)

	return new_sprite
	
def darken_color(color, percentage):
	new_color = pygame.Color(color[0], color[1], color[2])
	new_color.hsva = (new_color.hsva[0], new_color.hsva[1], new_color.hsva[2] * (1 - percentage), new_color.hsva[3])
	return (new_color.r, new_color.g, new_color.b)

class Sprite:
	def __init__(self):
		self.tileset = None # TileSet
		self.animations = None # AnimationSet

	def clone(self):
		sprite = Sprite()
		sprite.tileset = self.tileset.clone()
		sprite.animations = self.animations.clone()
		return sprite

	def recolor_image(self, src_colors, dst_colors):
		"""src_colors and dst_colors should lists of RGB tuples.  The input surface will be recolored in place, without making a copy."""
		if len(src_colors) != len(dst_colors) * 2:
			raise Exception("Not enough destination colors to go with the source colors.")

		pixels = pygame.PixelArray(self.tileset.image)
		for n in range(0, len(src_colors), 2):
			pixels.replace(src_colors[n], dst_colors[n // 2])
			pixels.replace(src_colors[n + 1], darken_color(dst_colors[n // 2], 0.25))
