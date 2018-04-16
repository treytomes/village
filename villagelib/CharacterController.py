from .CharacterEvent import *


class CharacterController:
    def __init__(self, character):
        self.character = character
        self.is_pushable = False

    def update(self, map_manager, hud):
        while len(self.character.events) > 0:
            event = self.character.events.pop()

            if type(event) == CharacterCollidedEvent:
                self.on_collided(event.collided_by, event.delta_x, event.delta_y)
                if self.is_pushable:
                    self.character.move_by(map_manager, event.delta_x, event.delta_y)
            elif type(event) == CharacterTouchedEvent:
                self.on_touched(event.touched_by)
            elif type(event) == CharacterSpeakEvent:
                hud.show_message(event.message)

        self.character.sprite.animations.update()

    def on_collided(self, collided_by, delta_x, delta_y):
        """
			This character was rammed into by another character.

			:param collided_by: The Character class reference that hit this character.
			:param delta_x: The collision speed on the x-axis.
			:param delta_y: The collision speed on the y-axis.
		"""
        pass

    def on_touched(self, touched_by):
        """
			This character was touched by another character.

			:param touched_by: The Character class reference that touched this character.
		"""
        pass
