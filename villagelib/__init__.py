import pygame

RENDER_SCALE = 3
ASSETS_PATH = "./assets/"

SCREEN_WIDTH: int = 256 * RENDER_SCALE
SCREEN_HEIGHT: int = 224 * RENDER_SCALE
SCREEN_CENTER_X: int = SCREEN_WIDTH // 2
SCREEN_CENTER_Y: int = SCREEN_HEIGHT // 2
FRAMES_PER_SECOND: float = 60.0

NORTH = 1
SOUTH = 2
EAST = 3
WEST = 4

from .AnimationSet import *
from .Character import *
from .CharacterController import *
from .CharacterEvent import *
from .MapTransition import *
from .MapManager import *
from .ScriptedCharacter import *
from .ScriptedCharacterController import *
from .Sprite import *
from .TiledRenderer import *
from .TileSet import *
from .extramath import *

# TODO: Make sure you know how to use this correctly.
#__all__ = ["extramath"]
