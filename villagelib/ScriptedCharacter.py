from .Character import *
from .Sprite import *
from . import RENDER_SCALE

class ScriptedCharacter(Character):
	def __init__(self, script_object):
		"""script_object is the Tiled object."""
		super().__init__(pygame.Rect(script_object.x * RENDER_SCALE, script_object.y * RENDER_SCALE, 0, 0))
		self.script_path = script_object.properties["Script Path"]
		self.__globals = dict()
		self.locals = dict()
		exec(open(self.script_path).read(), self.__globals, self.locals)

		try:
			self.load_sprite(create_npc_sprite(self.locals["npc_sprite_path"], self.locals["palette"]))
		except KeyError:
			self.load_sprite(create_npc_sprite(self.locals["npc_sprite_path"]))

		try:
			self.name = self.locals["name"]
		except KeyError:
			self.name = "Generic Scripted Character"
		