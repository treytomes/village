import pygame

RENDER_SCALE = 2
ASSETS_PATH = "./assets/"

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
