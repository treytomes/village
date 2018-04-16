from .CharacterController import *
from .ScriptedCharacter import *


class ScriptedCharacterController(CharacterController):
    STATE_NONE = 0
    STATE_WAVING = 1
    LENGTH_WAVING = 300 * 9

    def __init__(self, s_obj):
        super().__init__(ScriptedCharacter(s_obj))

        self.__state = None
        self.__state_start = 0

        self.set_state(ScriptedCharacterController.STATE_NONE)

        try:
            self.character.locals["on_create"](self)
        except KeyError:
            pass  # on_create wasn't defined.

        try:
            self.is_pushable = self.character.locals["is_pushable"]
        except KeyError:
            self.is_pushable = True

    def update(self, map_manager, hud):
        super().update(map_manager, hud)

        if self.__state == ScriptedCharacterController.STATE_WAVING:
            if pygame.time.get_ticks() - self.__state_start >= ScriptedCharacterController.LENGTH_WAVING:
                self.set_state(ScriptedCharacterController.STATE_NONE)
                self.character.stop_moving()

    def speak(self, message):
        self.character.events.append(CharacterSpeakEvent(self, message))

    def wave(self):
        self.set_state(ScriptedCharacterController.STATE_WAVING)
        self.character.sprite.animations.set_current(ANIM_WAVE)

    def set_state(self, state: int):
        self.__state = state
        self.__state_start = pygame.time.get_ticks()

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
