from .CharacterController import *
from .ScriptedCharacter import *


class CharacterState:
    def __init__(self, anim_key, length_ms=0, next_state=None):
        self.anim_key = anim_key
        self.length_ms = length_ms
        self.next_state = next_state
        self.start_ms = 0

    def enter(self, ctrl):
        self.start_ms = pygame.time.get_ticks()
        ctrl.character.sprite.animations.set_current(self.anim_key)

    def leave(self, ctrl):
        ctrl.set_state(self.next_state)

    def update(self, ctrl):
        if self.length_ms <= 0:
            return
        if pygame.time.get_ticks() - self.start_ms >= self.length_ms:
            self.leave(ctrl)


class ScriptedCharacterController(CharacterController):
    STATE_DEFAULT = CharacterState(ANIM_STAND_SOUTH, 0, None)
    STATE_WAVING = CharacterState(ANIM_WAVE, 300 * 9, STATE_DEFAULT)
    STATE_NODDING = CharacterState(ANIM_NOD, 300 * 6, STATE_DEFAULT)

    def __init__(self, s_obj):
        super().__init__(ScriptedCharacter(s_obj))

        self.__state = None
        self.__state_start = 0

        self.set_state(ScriptedCharacterController.STATE_DEFAULT)

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

        if self.__state is not None:
            self.__state.update(self)

    def speak(self, message):
        self.character.events.append(CharacterSpeakEvent(self, message))

    def wave(self):
        self.set_state(CharacterState(ANIM_WAVE, 300 * 9, CharacterState(self.character.sprite.animations.get_current())))

    def nod(self):
        self.set_state(CharacterState(ANIM_NOD, 300 * 6, CharacterState(self.character.sprite.animations.get_current())))

    def set_state(self, state: int):
        self.__state = state
        if self.__state is None:
            self.__state = ScriptedCharacterController.STATE_DEFAULT
        self.__state.enter(self)

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
