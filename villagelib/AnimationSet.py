import pygame

# Standard animations to be used as keys in AnimationSet.
ANIM_STAND_SOUTH = 0
ANIM_STAND_NORTH = 1
ANIM_STAND_WEST = 2
ANIM_STAND_EAST = 3
ANIM_WALK_SOUTH = 4
ANIM_WALK_NORTH = 5
ANIM_WALK_WEST = 6
ANIM_WALK_EAST = 7
ANIM_RAISE_HAND = 8
ANIM_WAVE = 9
ANIM_SAD = 10
ANIM_NOD = 11
ANIM_DIE = 12

class AnimationSet:
    def __init__(self, sets = None):
        """sets: an optional dictionary of pre-defined animations, or an AnimationSet to copy from."""
        self.__sets = dict() # The dictionary of animation sets.
        self.__current = None # The current animation key.
        self.speed = 0 # Animation speed in milliseconds.
        self.__last_animate_time = 0 # Last time in milliseconds that the animation was updated.
        self.__animation_index = 0 # Index into the current animation.
        self.tile_index = 0 # Current tile index based on the current animation.

        if (sets != None) and (type(sets) is dict):
            for key in sets:
                self.add(key, sets[key])

    def get_current(self):
        """Get the current animation key."""
        return self.__current

    def set_current(self, key):
        if key not in self.__sets:
            raise Exception(f"The animation key is not defined: {key}")
        elif key != self.__current:
            self.__current = key
            self.__last_animate_time = 0
            self.__animation_index = 0

    def add(self, key, index_list):
        self.__sets[key] = index_list

    def clone(self):
        """Create a new AnimationSet based off this instance."""
        anims = AnimationSet(self.__sets)
        anims.speed = self.speed
        return anims

    def update(self):
        """Animate the player sprite, potentially setting tile_index to a new value."""
        if pygame.time.get_ticks() - self.__last_animate_time > self.speed:
            self.__animation_index += 1
            self.tile_index = self.__sets[self.__current][self.__animation_index % len(self.__sets[self.__current])]
            self.__last_animate_time = pygame.time.get_ticks()
