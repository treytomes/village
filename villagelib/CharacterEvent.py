class CharacterEvent:
    def __init__(self):
        pass


class CharacterCollidedEvent(CharacterEvent):
    def __init__(self, collided_by, delta_x, delta_y):
        self.collided_by = collided_by
        self.delta_x = delta_x
        self.delta_y = delta_y


class CharacterTouchedEvent(CharacterEvent):
    def __init__(self, touched_by):
        self.touched_by = touched_by


class CharacterSpeakEvent(CharacterEvent):
    def __init__(self, source, message):
        self.source = source
        self.message = message
