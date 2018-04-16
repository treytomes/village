# Useful references:
#   https://www.pygame.org/docs/ref/display.html
#   https://www.pygame.org/project-Tiled+TMX+Loader-2036-.html
#   Final Fantasy 6 Sprites: https://www.spriters-resource.com/snes/ff6/
#   Final Fantasy 4 Sprites: https://www.spriters-resource.com/snes/ff4
#   More Final Fantasy 4 Sprites: http://www.videogamesprites.net/FinalFantasy4/
#   https://docs.python.org/3/library/enum.html
#
#   Tiled Map Editor documentation: http://docs.mapeditor.org/en/latest/
#   PyTMX GitHub: https://github.com/bitcraft/PyTMX
# Also:
#   pip install pytmx
# Note: Rather than using the pytmx package, I copied the source files locally.
# The package was missing some features that I needed.

from villagelib import *

import sprites

pygame.init()

SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
SCREEN_CENTER_X: int = SCREEN_WIDTH // 2
SCREEN_CENTER_Y: int = SCREEN_HEIGHT // 2
FRAMES_PER_SECOND: float = 60.0
GAME_TITLE: str = "Village Simulator"
GAME_ICON: str = ASSETS_PATH + "icon.png"
INITIAL_MAP: str = "Village Mist - Inn"

class Colors:
    BACKGROUND: pygame.Color = pygame.Color(48, 48, 48)


def scroll_into_view(screen: pygame.Surface, frame_timer: pygame.time.Clock, map_manager: MapManager, player_rect: pygame.Rect):
    """Open the screen with a stage-curtain effect.

    :param screen: A reference to the screen the game is being rendered on.
    :param frame_timer: The clock object used to throttle the framerate.
    :param map_manager: The map being rendered.
    :param player_rect: The location and size of the player to center the map on.

    :type screen: pygame.Surface
    :type frame_timer: pygame.time.Clock
    :type map_manager: MapManager
    :type player_rect: pygame.Rect
    """
    global SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER_X, FRAMES_PER_SECOND
    CURTAIN_SPEED: int = 8
    offset: int = 0
    while offset < SCREEN_WIDTH // 2:
        screen.fill(Colors.BACKGROUND)
        map_manager.render_under_sprites(screen, player_rect.x, player_rect.y)
        map_manager.render_over_sprites(screen, player_rect.x, player_rect.y)
        pygame.draw.rect(screen, Colors.BACKGROUND, (0, 0, SCREEN_CENTER_X - offset, SCREEN_HEIGHT), 0)
        pygame.draw.rect(screen, Colors.BACKGROUND, (SCREEN_CENTER_X + offset, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
        pygame.display.flip()
        frame_timer.tick(FRAMES_PER_SECOND)
        offset += CURTAIN_SPEED


def blit_map():
    """Draw the game board."""
    global screen, hud, map_manager, player

    screen.fill(Colors.BACKGROUND)
    map_manager.render_under_sprites(screen, player.character.rect.x, player.character.rect.y)

    for npc in map_manager.characters:
        npc.character.blit(screen, map_manager, player.character.rect)

    player.character.blit(screen, map_manager, player.character.rect)

    map_manager.render_over_sprites(screen, player.character.rect.x, player.character.rect.y)

    hud.blit()


class Player(Character):
    def __init__(self, spawn_point):
        super().__init__(spawn_point)
        self.name = "Player"
        self.load_sprite(sprites.npc_male_3)
        self.can_slide = True
        self.is_pushable = False


class PlayerController(CharacterController):
    def __init__(self, spawn_point):
        super().__init__(Player(spawn_point))
        self.walking_speed = 1
        self.running_speed = 2
        self.selected_slot = 0

    def update(self, map_manager: MapManager, hud):
        super().update(map_manager, hud)

        key_state = pygame.key.get_pressed()

        if key_state[pygame.K_LSHIFT]:
            self.character.speed = self.running_speed
        else:
            self.character.speed = self.walking_speed

        if key_state[pygame.K_w]:
            self.character.move_north(map_manager)
        elif key_state[pygame.K_s]:
            self.character.move_south(map_manager)
        elif key_state[pygame.K_a]:
            self.character.move_west(map_manager)
        elif key_state[pygame.K_d]:
            self.character.move_east(map_manager)
        elif key_state[pygame.K_z]:
            self.character.sprite.animations.set_current(ANIM_RAISE_HAND)
        elif key_state[pygame.K_x]:
            self.character.sprite.animations.set_current(ANIM_WAVE)
        elif key_state[pygame.K_c]:
            self.character.sprite.animations.set_current(ANIM_SAD)
        elif key_state[pygame.K_v]:
            self.character.sprite.animations.set_current(ANIM_NOD)
        elif key_state[pygame.K_b]:
            self.character.sprite.animations.set_current(ANIM_DIE)
        elif key_state[pygame.K_SPACE]:
            self.touch(map_manager)

        elif key_state[pygame.K_1]:
            self.selected_slot = 1
        elif key_state[pygame.K_2]:
            self.selected_slot = 2
        elif key_state[pygame.K_3]:
            self.selected_slot = 3
        elif key_state[pygame.K_4]:
            self.selected_slot = 4
        elif key_state[pygame.K_5]:
            self.selected_slot = 5
        elif key_state[pygame.K_6]:
            self.selected_slot = 6
        elif key_state[pygame.K_7]:
            self.selected_slot = 7
        elif key_state[pygame.K_8]:
            self.selected_slot = 8
        elif key_state[pygame.K_9]:
            self.selected_slot = 9
        elif key_state[pygame.K_0]:
            self.selected_slot = 0

        else:
            # No key was pressed, so no longer moving.
            self.character.stop_moving()

    def touch(self, map_manager: MapManager):
        TOUCH_DISTANCE: int = 1.5
        TILE_SIZE: int = 16
        PIXEL_DISTANCE: int = int(RENDER_SCALE * TILE_SIZE * TOUCH_DISTANCE)

        delta_x: int = 0
        delta_y: int = 0
        if self.character.facing_direction == NORTH:
            delta_y = -1
        elif self.character.facing_direction == SOUTH:
            delta_y = 1
        elif self.character.facing_direction == WEST:
            delta_x = -1
        elif self.character.facing_direction == EAST:
            delta_x = 1

        center_x: int = self.character.rect.x + self.character.rect.width // 2
        center_y: int = self.character.rect.y + self.character.rect.height // 2

        start_x: int = center_x + delta_x * (self.character.rect.width // 2)
        start_y: int = center_y + delta_y * (self.character.rect.height // 2)

        for n in range(0, PIXEL_DISTANCE, 8):
            touchpoint_found: bool = False
            for npc in map_manager.characters:
                test_x: int = start_x + delta_x * n
                test_y: int = start_y + delta_y * n
                if npc.character.rect.inflate(-1, -1).collidepoint(test_x, test_y):
                    npc.character.events.append(CharacterTouchedEvent(self.character))
                    touchpoint_found = True
                    break
            if touchpoint_found:
                break


class HUDElement:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)

    def update(self):
        pass

    def blit(self, dst_surface):
        pass


# TODO: Make the hotkey slots hold something.
class HUDHotKeySlot(HUDElement):
    TEXT: pygame.Color = pygame.Color(255, 255, 192)
    BORDER: pygame.Color = pygame.Color(255, 255, 255)
    BACKGROUND: pygame.Color = pygame.Color(0, 0, 0)
    BORDER_SELECTED: pygame.Color = pygame.Color(0, 0, 127)
    BACKGROUND_SELECTED: pygame.Color = pygame.Color(255, 0, 0)
    TINY_FONT = pygame.font.SysFont("Comic Sans MS", 8, bold=True)

    def __init__(self, key):
        hotkey_size = 18 * RENDER_SCALE
        num_hotkeys = 10
        offset = (SCREEN_WIDTH - num_hotkeys * (hotkey_size + RENDER_SCALE)) // 2
        index = (key - 1) % 10
        self.rect = pygame.Rect(offset + index * (hotkey_size + RENDER_SCALE),
                                SCREEN_HEIGHT - hotkey_size - RENDER_SCALE,
                                hotkey_size, hotkey_size)
        self.key = key
        self.is_selected = False

    def update(self):
        global player
        self.is_selected = (player.selected_slot == self.key)

    def blit(self, dst_surface):
        if self.is_selected:
            pygame.draw.rect(dst_surface, HUDHotKeySlot.BORDER_SELECTED,
                             self.rect.inflate(-RENDER_SCALE, -RENDER_SCALE))
            pygame.draw.rect(dst_surface, HUDHotKeySlot.BACKGROUND_SELECTED, self.rect, RENDER_SCALE)
        else:
            pygame.draw.rect(dst_surface, HUDHotKeySlot.BACKGROUND,
                             self.rect.inflate(-RENDER_SCALE, -RENDER_SCALE))
            pygame.draw.rect(dst_surface, HUDHotKeySlot.BORDER, self.rect, RENDER_SCALE)
        dst_surface.blit(HUDHotKeySlot.TINY_FONT.render(str(self.key), True, HUDHotKeySlot.TEXT), (self.rect.x + 3, self.rect.y + 1))


class HUDLabel(HUDElement):
    FONT = pygame.font.SysFont("Comic Sans MS", 16)  # , bold=True)

    def __init__(self, x, y, text):
        super().__init__()

        self.__text = None
        self.__text_surface = None

        self.position = (x, y)
        self.color = pygame.Color(255, 255, 255)
        self.set_text(text)

    def update(self):
        global map_manager
        self.set_text(map_manager.map_name)

    def blit(self, dst_surface):
        dst_surface.blit(self.__text_surface, self.position)

    def set_text(self, text):
        self.__text = text
        self.__text_surface = HUDLabel.FONT.render(self.__text, True, self.color)


class HUDMessageBox(HUDElement):
    MESSAGEBOX_WIDTH = 19
    MESSAGEBOX_HEIGHT = 6
    TEXT_COLOR = pygame.Color(255, 255, 255)
    TEXT_ANIMATE_SPEED = 50
    BLINK_ANIMATE_SPEED = 500
    CONTINUE_COLOR = pygame.Color(255, 255, 192)
    CONTINUE_KEY = pygame.K_SPACE
    CONTINUE_TEXT = f"Press <{pygame.key.name(CONTINUE_KEY)}> to continue."

    def __init__(self):
        self.window_tiles = TileSet("./assets/ui/window_tiles.png", 3, 3)
        self.window_tiles.scale(RENDER_SCALE)
        self.window_position = (0, 0)
        self.text_position = (self.window_position[0] + self.window_tiles.tile_width,
                              self.window_position[1] + self.window_tiles.tile_height)
        self.font = pygame.font.SysFont("Comic Sans MS", 16)  # , bold=True)
        self.continue_text = self.font.render(HUDMessageBox.CONTINUE_TEXT, True, HUDMessageBox.CONTINUE_COLOR)
        self.is_focused = False
        self.message = ""
        self.displayed_message = ""
        self.show_continue_message = False
        self.last_animate_time = 0
        self.__key_state = dict()
        self.__last_key_state = dict()

    def __get_key_released(self, key):
        try:
            was_key_pressed = self.__last_key_state[key]
        except KeyError:
            was_key_pressed = False
        try:
            is_key_pressed = self.__key_state[key]
        except KeyError:
            is_key_pressed = False
        return was_key_pressed and (not is_key_pressed)

    def update(self):
        if not self.is_focused:
            return

        # Check for key press.
        if len(self.message) == 0:
            self.__last_key_state = self.__key_state
            self.__key_state = pygame.key.get_pressed()
            if self.__get_key_released(HUDMessageBox.CONTINUE_KEY):
                self.is_focused = False

        # Animate the text.
        if len(self.message) > 0:
            if pygame.time.get_ticks() - self.last_animate_time > HUDMessageBox.TEXT_ANIMATE_SPEED:
                self.last_animate_time = pygame.time.get_ticks()
                self.displayed_message = self.displayed_message + self.message[0]
                self.message = self.message[1:]
        else:
            if pygame.time.get_ticks() - self.last_animate_time > HUDMessageBox.BLINK_ANIMATE_SPEED:
                self.last_animate_time = pygame.time.get_ticks()
                self.show_continue_message = not self.show_continue_message

    def blit(self, dst_surface):
        if not self.is_focused:
            return

        self.blit_frame(dst_surface, self.window_position)
        dst_surface.blit(self.font.render(self.displayed_message, True, HUDMessageBox.TEXT_COLOR), self.text_position)
        if self.show_continue_message:
            dst_surface.blit(self.continue_text, (
                self.window_position[0] + self.window_tiles.tile_width * HUDMessageBox.MESSAGEBOX_WIDTH - self.continue_text.get_width(),
                self.window_position[1] + self.window_tiles.tile_height * HUDMessageBox.MESSAGEBOX_HEIGHT - self.continue_text.get_height()
            ))

    def blit_frame(self, dst_surface, window_position):
        window_left: int = window_position[0]
        window_right: int = window_left + self.window_tiles.tile_width * HUDMessageBox.MESSAGEBOX_WIDTH
        window_top: int = window_position[1]
        window_bottom: int = window_top + self.window_tiles.tile_height * HUDMessageBox.MESSAGEBOX_HEIGHT

        self.window_tiles.blit(dst_surface, 0, window_left, window_top)
        self.window_tiles.blit(dst_surface, 2, window_right, window_top)
        self.window_tiles.blit(dst_surface, 6, window_left, window_bottom)
        self.window_tiles.blit(dst_surface, 8, window_right, window_bottom)
        for x in range(HUDMessageBox.MESSAGEBOX_WIDTH - 1):
            offset = self.window_tiles.tile_width * (1 + x)
            self.window_tiles.blit(dst_surface, 1, window_left + offset, window_top)
            self.window_tiles.blit(dst_surface, 7, window_left + offset, window_bottom)
        for y in range(HUDMessageBox.MESSAGEBOX_HEIGHT - 1):
            offset = self.window_tiles.tile_height * (1 + y)
            self.window_tiles.blit(dst_surface, 3, window_left, window_top + offset)
            self.window_tiles.blit(dst_surface, 5, window_right, window_top + offset)
        for y in range(1, HUDMessageBox.MESSAGEBOX_HEIGHT):
            for x in range(1, HUDMessageBox.MESSAGEBOX_WIDTH):
                offset_x = self.window_tiles.tile_width * x
                offset_y = self.window_tiles.tile_height * y
                self.window_tiles.blit(dst_surface, 4, window_left + offset_x, window_top + offset_y)

    def show_message(self, message):
        print(f"[MESSAGE] {message}")
        self.__key_state = dict()
        self.__last_key_state = dict()
        self.message = message
        self.displayed_message = ""
        self.is_focused = True


class HUDManager:
    def __init__(self, screen):
        self.screen = screen
        self.messagebox = HUDMessageBox()

        self.elements = list()
        self.elements.append(HUDLabel(16, 16, "Map Name"))
        self.elements.append(HUDHotKeySlot(1))
        self.elements.append(HUDHotKeySlot(2))
        self.elements.append(HUDHotKeySlot(3))
        self.elements.append(HUDHotKeySlot(4))
        self.elements.append(HUDHotKeySlot(5))
        self.elements.append(HUDHotKeySlot(6))
        self.elements.append(HUDHotKeySlot(7))
        self.elements.append(HUDHotKeySlot(8))
        self.elements.append(HUDHotKeySlot(9))
        self.elements.append(HUDHotKeySlot(0))
        self.elements.append(self.messagebox)

    def update(self):
        for element in self.elements:
            element.update()

    def blit(self):
        """Draw the heads-up display."""
        for element in self.elements:
            element.blit(self.screen)

    # I don't like how this disables the main loop.
    def show_message(self, text: str):
        self.messagebox.show_message(text)


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(GAME_TITLE)
pygame.display.set_icon(pygame.image.load(GAME_ICON))

map_manager = MapManager(INITIAL_MAP)

hud = HUDManager(screen)
player = PlayerController(map_manager.spawn_point)

frame_timer = pygame.time.Clock()

is_paused = False
is_playing = True
while is_playing:
    # Respond to events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_playing = False
        elif event.type == pygame.KEYUP:
            pass

    is_paused = not pygame.key.get_focused()

    hud.update()

    if not hud.messagebox.is_focused:
        player.update(map_manager, hud)

    # Check for player intersection with transition objects.
    for transition in map_manager.transitions:
        if player.character.rect.colliderect(transition.bounds):
            map_manager.load_map(transition.target_map)
            player.character.rect.x = transition.target_x
            player.character.rect.y = transition.target_y
            scroll_into_view(screen, frame_timer, map_manager, player.character.rect)
            break  # New map loaded == stop checking transitions on the old map.

    map_manager.update_animations()

    for npc in map_manager.characters:
        npc.update(map_manager, hud)

    blit_map()

    pygame.display.flip()

    frame_timer.tick(FRAMES_PER_SECOND)

pygame.quit()
