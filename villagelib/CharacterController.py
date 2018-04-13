from .Character import *

class CharacterController:
	def __init__(self, character):
		self.character = character
		self.is_pushable = False

	def update(self, map_manager):
		for event in list(self.character.events):
			if type(event) == CharacterCollidedEvent:
				self.on_collided(event.collided_by, event.delta_x, event.delta_y)
				if self.is_pushable:
					self.character.move_by(map_manager, event.delta_x, event.delta_y)
			elif type(event) == CharacterTouchedEvent:
				self.on_touched(event.touched_by)

		self.character.events.clear()
		self.character.sprite.animations.update()

	def on_collided(self, collided_by, delta_x, delta_y):
		"""
			This character was rammed into by another character.

			collided_by: The Character class reference that hit this character.
			delta_x: The collision speed on the x-axis.
			delta_y: The collision speed on the y-axis.
		"""
		pass

	def on_touched(self, touched_by):
		"""
			This character was touched by another character.

			touched_by: The Character class reference that touched this character.
		"""
		pass
