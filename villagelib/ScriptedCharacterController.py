from .CharacterController import *
from .ScriptedCharacter import *

class ScriptedCharacterController(CharacterController):

	def __init__(self, s_obj):
		super().__init__(ScriptedCharacter(s_obj))

		try:
			self.character.locals["on_create"](self)
		except KeyError:
			pass # on_create wasn't defined.

		try:
			self.is_pushable = self.character.locals["is_pushable"]
		except KeyError:
			self.is_pushable = True

	def update(self, map_manager):
		super().update(map_manager)

	def on_collided(self, collided_by, delta_x, delta_y):
		try:
			self.character.locals["on_collided"](self, collided_by, delta_x, delta_y)
		except KeyError:
			pass

	def on_touched(self, touched_by):
		try:
			self.character.locals["on_touched"](self, touched_by)
		except KeyError:
			pass