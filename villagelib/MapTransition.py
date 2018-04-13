import pygame

from . import RENDER_SCALE

class MapTransition:
	"""Track the boundaries of this transition on the current map, along with the linked location in the target map."""

	def __init__(self, tiled_transition):
		self.bounds = pygame.Rect(
			tiled_transition.x * RENDER_SCALE,
			tiled_transition.y * RENDER_SCALE,
			tiled_transition.width * RENDER_SCALE,
			tiled_transition.height * RENDER_SCALE)
		self.target_map = tiled_transition.properties["Target Map"]

		tile_width = tiled_transition.parent.tilewidth * RENDER_SCALE
		tile_height = tiled_transition.parent.tileheight * RENDER_SCALE

		self.target_x = int(tiled_transition.properties["Target X"]) * tile_width
		self.target_y = int(tiled_transition.properties["Target Y"]) * tile_height
