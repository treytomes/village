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

# TODO: Rename npc_male_1.py to npc_templates.py?
import sprites

SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
SCREEN_CENTER_X: int = SCREEN_WIDTH // 2
SCREEN_CENTER_Y: int = SCREEN_HEIGHT // 2
FRAMES_PER_SECOND: float = 60.0
GAME_TITLE: str = "Village Simulator"
GAME_ICON: str = ASSETS_PATH + "icon.png"
INITIAL_MAP: str = "Village Mist - Rydia's House"
BACKGROUND_COLOR: pygame.Color = pygame.Color(48, 48, 48)


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
    global SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER_X, BACKGROUND_COLOR, FRAMES_PER_SECOND
    CURTAIN_SPEED: int = 8
    offset: int = 0
    while offset < SCREEN_WIDTH // 2:
        screen.fill(BACKGROUND_COLOR)
        map_manager.render_under_sprites(screen, player_rect.x, player_rect.y)
        map_manager.render_over_sprites(screen, player_rect.x, player_rect.y)
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, SCREEN_CENTER_X - offset, SCREEN_HEIGHT), 0)
        pygame.draw.rect(screen, BACKGROUND_COLOR, (SCREEN_CENTER_X + offset, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
        pygame.display.flip()
        frame_timer.tick(FRAMES_PER_SECOND)
        offset += CURTAIN_SPEED


pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(GAME_TITLE)
pygame.display.set_icon(pygame.image.load(GAME_ICON))

map_manager = MapManager(INITIAL_MAP)


class Player(Character):
    def __init__(self, spawn_point):
        super().__init__(spawn_point)
        self.name = "Player"
        # self.load_sprite(sprites.npc_male_1)
        self.load_sprite(sprites.rydia_old)
        self.can_slide = True
        self.is_pushable = False


class PlayerController(CharacterController):
    def __init__(self, spawn_point):
        super().__init__(Player(spawn_point))
        self.walking_speed = 1
        self.running_speed = 2
        self.selected_slot = 0

    def update(self, map_manager: MapManager):
        super().update(map_manager)

        key_state = pygame.key.get_pressed()

        if key_state[pygame.K_LSHIFT] == 1:
            self.character.speed = self.running_speed
        else:
            self.character.speed = self.walking_speed

        if key_state[pygame.K_w] == 1:
            self.character.move_north(map_manager)
        elif key_state[pygame.K_s] == 1:
            self.character.move_south(map_manager)
        elif key_state[pygame.K_a] == 1:
            self.character.move_west(map_manager)
        elif key_state[pygame.K_d] == 1:
            self.character.move_east(map_manager)
        elif key_state[pygame.K_z] == 1:
            self.character.sprite.animations.set_current(ANIM_RAISE_HAND)
        elif key_state[pygame.K_x] == 1:
            self.character.sprite.animations.set_current(ANIM_WAVE)
        elif key_state[pygame.K_c] == 1:
            self.character.sprite.animations.set_current(ANIM_SAD)
        elif key_state[pygame.K_v] == 1:
            self.character.sprite.animations.set_current(ANIM_NOD)
        elif key_state[pygame.K_b] == 1:
            self.character.sprite.animations.set_current(ANIM_DIE)
        elif key_state[pygame.K_SPACE] == 1:
            self.touch(map_manager, self.character.facing_direction)

        elif key_state[pygame.K_1] == 1:
            self.selected_slot = 1
        elif key_state[pygame.K_2] == 1:
            self.selected_slot = 2
        elif key_state[pygame.K_3] == 1:
            self.selected_slot = 3
        elif key_state[pygame.K_4] == 1:
            self.selected_slot = 4
        elif key_state[pygame.K_5] == 1:
            self.selected_slot = 5
        elif key_state[pygame.K_6] == 1:
            self.selected_slot = 6
        elif key_state[pygame.K_7] == 1:
            self.selected_slot = 7
        elif key_state[pygame.K_8] == 1:
            self.selected_slot = 8
        elif key_state[pygame.K_9] == 1:
            self.selected_slot = 9
        elif key_state[pygame.K_0] == 1:
            self.selected_slot = 0

        else:
            # No key was pressed, so no longer moving.
            self.character.stop_moving()

    def touch(self, map_manager, direction):
        TOUCH_DISTANCE = 1
        TILE_SIZE = 16
        PIXEL_DISTANCE = int(RENDER_SCALE * TILE_SIZE * TOUCH_DISTANCE)

        delta_x = 0
        delta_y = 0
        if self.character.facing_direction == NORTH:
            delta_y = -1
        elif self.character.facing_direction == SOUTH:
            delta_y = 1
        elif self.character.facing_direction == WEST:
            delta_x = -1
        elif self.character.facing_direction == EAST:
            delta_x = 1

        center_x = self.character.rect.x + self.character.rect.width // 2
        center_y = self.character.rect.y + self.character.rect.height // 2

        start_x = center_x + delta_x * (self.character.rect.width // 2)
        start_y = center_y + delta_y * (self.character.rect.height // 2)

        for n in range(0, PIXEL_DISTANCE, 8):
            touchpoint_found = False
            for npc in map_manager.characters:
                test_x = start_x + delta_x * n
                test_y = start_y + delta_y * n
                if npc.character.rect.inflate(-1, -1).collidepoint(test_x, test_y):
                    npc.character.events.append(CharacterTouchedEvent(self.character))
                    touchpoint_found = True
                    break
            if touchpoint_found:
                break


player = PlayerController(map_manager.spawn_point)

hud_font = pygame.font.SysFont("Comic Sans MS", 16)  # , bold=True)
tiny_font = pygame.font.SysFont("Comic Sans MS", 8)

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

    player.update(map_manager)

    # Check for player intersection with transition objects.
    for transition in map_manager.transitions:
        if player.character.rect.colliderect(transition.bounds):
            map_manager.load_map(transition.target_map)
            player.character.rect.x = transition.target_x
            player.character.rect.y = transition.target_y
            scroll_into_view(screen, frame_timer, map_manager, player.character.rect)

    map_manager.update_animations()

    # Draw the game board.
    screen.fill(BACKGROUND_COLOR)
    map_manager.render_under_sprites(screen, player.character.rect.x, player.character.rect.y)

    for npc in map_manager.characters:
        npc.update(map_manager)
        npc.character.blit(screen, map_manager, player.character.rect)

    player.character.blit(screen, map_manager, player.character.rect)

    map_manager.render_over_sprites(screen, player.character.rect.x, player.character.rect.y)

    # Draw the user interface.
    screen.blit(hud_font.render(map_manager.map_name, True, [255, 255, 255]), (16, 16))
    hotkey_size = 18 * RENDER_SCALE
    hotkeys = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
    offset = (SCREEN_WIDTH - len(hotkeys) * (hotkey_size + RENDER_SCALE)) // 2
    for n in range(len(hotkeys)):
        hotkey_rect = pygame.Rect(offset + n * (hotkey_size + RENDER_SCALE), SCREEN_HEIGHT - hotkey_size - RENDER_SCALE,
                                  hotkey_size, hotkey_size)
        if player.selected_slot == hotkeys[n]:
            pygame.draw.rect(screen, [0, 0, 127], hotkey_rect.inflate(-RENDER_SCALE, -RENDER_SCALE))
            pygame.draw.rect(screen, [255, 0, 0], hotkey_rect, RENDER_SCALE)
        else:
            pygame.draw.rect(screen, [0, 0, 0], hotkey_rect.inflate(-RENDER_SCALE, -RENDER_SCALE))
            pygame.draw.rect(screen, [255, 255, 255], hotkey_rect, RENDER_SCALE)
        screen.blit(tiny_font.render(str(hotkeys[n]), True, [255, 255, 192]), (hotkey_rect.x + 3, hotkey_rect.y + 1))

    pygame.display.flip()

    frame_timer.tick(FRAMES_PER_SECOND)

pygame.quit()
