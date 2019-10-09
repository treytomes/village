import pygame
from villagelib import SCREEN_WIDTH, SCREEN_HEIGHT, RENDER_SCALE, TileSet

FONT_TEXT: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?/:\"'-.,…;#+()%~ <>="

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
    #TINY_FONT = pygame.font.SysFont("Comic Sans MS", 8, bold=True)

    def __init__(self, player, key):
        self.player = player # TODO: I may later regret having a strong coupling here.
        self.is_blit_initialized = False
        hotkey_size = 18 * RENDER_SCALE
        self.rect = pygame.Rect(0, 0, hotkey_size, hotkey_size)
        self.key = key
        self.is_selected = False

        self.font_tiles: TileSet = TileSet("./assets/font.png", 16, 8)
        self.font_tiles.scale(RENDER_SCALE)
        self.font_tiles.recolor_image((
            (0, 0, 0, 0), # This one will be transparent.
            (0, 0, 0, 255),
            (0, 0, 0, 255),
            HUDHotKeySlot.TEXT))

    def update(self):
        self.is_selected = (self.player.selected_slot == self.key)

    def blit(self, dst_surface):
        if not self.is_blit_initialized:
            num_hotkeys = 10
            index = (self.key - 1) % 10
            screen_width = dst_surface.get_width()
            screen_height = dst_surface.get_height()
            offset = (screen_width - num_hotkeys * (self.rect.width + RENDER_SCALE)) // 2
            self.rect.x = offset + index * (self.rect.width + RENDER_SCALE)
            self.rect.y = screen_height - (self.rect.height + RENDER_SCALE)
            self.is_blit_initialized = True

        if self.is_selected:
            pygame.draw.rect(dst_surface, HUDHotKeySlot.BORDER_SELECTED,
                             self.rect.inflate(-RENDER_SCALE, -RENDER_SCALE))
            pygame.draw.rect(dst_surface, HUDHotKeySlot.BACKGROUND_SELECTED, self.rect, RENDER_SCALE)
        else:
            pygame.draw.rect(dst_surface, HUDHotKeySlot.BACKGROUND,
                             self.rect.inflate(-RENDER_SCALE, -RENDER_SCALE))
            pygame.draw.rect(dst_surface, HUDHotKeySlot.BORDER, self.rect, RENDER_SCALE)
        
        #dst_surface.blit(HUDHotKeySlot.TINY_FONT.render(str(self.key), True, HUDHotKeySlot.TEXT), (self.rect.x + 3, self.rect.y + 1))
        tile_index = int(self.key) + 16 * 7
        self.font_tiles.blit(dst_surface, tile_index, self.rect.x + 3, self.rect.y + 1)


class HUDLabel(HUDElement):
    #FONT = pygame.font.SysFont("Comic Sans MS", 16)  # , bold=True)

    def __init__(self, x, y, text):
        super().__init__()

        self.__text = None
        #self.__text_surface = None
        #self.__shadow_surface = None

        self.position = (x, y)
        self.__color = pygame.Color(255, 255, 255, 255)
        self.__shadow_color = pygame.Color(64, 64, 64, 255)
        self.set_text(text)

        self.font_tiles: TileSet = TileSet("./assets/font.png", 16, 8)
        self.font_tiles.scale(RENDER_SCALE)
        self.font_tiles.recolor_image((
            (0, 0, 0, 0), # This one will be transparent.
            self.__shadow_color,
            (127, 127, 127, 255),
            self.__color))

    def blit(self, dst_surface):
        #dst_surface.blit(self.__shadow_surface, (self.position[0] + 1, self.position[1] + 1))
        #dst_surface.blit(self.__text_surface, self.position)
        x = self.position[0]
        for ch in self.__text:
            try:
                tile_index = FONT_TEXT.index(ch)
                self.font_tiles.blit(dst_surface, tile_index, x, self.position[1])
            except:
                # The character might not be in the font set.
                pass
            x += self.font_tiles.tile_width

    def set_text(self, text):
        self.__text = text
        #self.__text_surface = HUDLabel.FONT.render(self.__text, True, self.color)
        #self.__shadow_surface = HUDLabel.FONT.render(self.__text, True, self.shadow_color)


class HUDMessageBox(HUDElement):
    MESSAGEBOX_WIDTH = 15 #SCREEN_WIDTH // RENDER_SCALE // 18
    MESSAGEBOX_HEIGHT = 6
    TEXT_COLOR = pygame.Color(255, 255, 255)
    TEXT_ANIMATE_SPEED = 50
    BLINK_ANIMATE_SPEED = 500
    CONTINUE_COLOR = pygame.Color(255, 255, 128)  # Was 255,255,192; does it look right?
    CONTINUE_KEY = pygame.K_SPACE
    CONTINUE_TEXT = f"Press <{pygame.key.name(CONTINUE_KEY)}> to continue."

    def __init__(self):
        self.window_tiles = TileSet("./assets/ui/window_tiles.png", 3, 3)
        self.window_tiles.scale(RENDER_SCALE)
        self.window_position = (0, 0)

        #self.font = pygame.font.SysFont("Comic Sans MS", 16)  # , bold=True)
        #self.continue_text = self.font.render(HUDMessageBox.CONTINUE_TEXT, True, HUDMessageBox.CONTINUE_COLOR)
        self.is_focused = False
        self.is_paused = False
        self.message = ""
        self.displayed_message = ""
        self.show_continue_message = False
        self.last_animate_time = 0
        self.__key_state = dict()
        self.__last_key_state = dict()

        self.message_tiles: TileSet = TileSet("./assets/font.png", 16, 8)
        self.message_tiles.scale(RENDER_SCALE)
        self.message_tiles.recolor_image((
            (0, 0, 0, 0), # This one will be transparent.
            (64, 64, 64, 255),
            (127, 127, 127, 255),
            HUDMessageBox.TEXT_COLOR))

        self.prompt_tiles: TileSet = TileSet("./assets/font.png", 16, 8)
        self.prompt_tiles.scale(RENDER_SCALE)
        self.prompt_tiles.recolor_image((
            (0, 0, 0, 0), # This one will be transparent.
            (64, 64, 64, 255),
            (127, 127, 127, 255),
            HUDMessageBox.CONTINUE_COLOR))

        self.text_position = (self.window_position[0] + self.window_tiles.tile_width - self.message_tiles.tile_width,
                              self.window_position[1] + self.window_tiles.tile_height - self.message_tiles.tile_height)

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
        if self.is_paused:
            self.__last_key_state = self.__key_state
            self.__key_state = pygame.key.get_pressed()
            if self.__get_key_released(HUDMessageBox.CONTINUE_KEY):
                self.is_paused = False
                self.displayed_message = ""
                if len(self.message) == 0:
                    self.is_focused = False

        # Animate the text.
        if not self.is_paused:
            if len(self.message) > 0:
                if pygame.time.get_ticks() - self.last_animate_time > HUDMessageBox.TEXT_ANIMATE_SPEED:
                    self.last_animate_time = pygame.time.get_ticks()
                    self.displayed_message = self.displayed_message + self.message[0]
                    self.message = self.message[1:]
            if len(self.message) == 0:
                self.is_paused = True
        else:
            if pygame.time.get_ticks() - self.last_animate_time > HUDMessageBox.BLINK_ANIMATE_SPEED:
                self.last_animate_time = pygame.time.get_ticks()
                self.show_continue_message = not self.show_continue_message

    def blit(self, dst_surface):
        if not self.is_focused:
            return

        self.blit_frame(dst_surface, self.window_position)

        x = self.text_position[0]
        y = self.text_position[1]
        row = 0
        column = 0
        for n in range(len(self.displayed_message)):
            ch = self.displayed_message[n]
            if ch == '\n':
                x = self.text_position[0]
                y += self.message_tiles.tile_height
                column = 0
            elif (column == 0) and (ch == ' '):
                pass
            else:
                try:
                    self.message_tiles.blit(dst_surface, FONT_TEXT.index(ch), x, y)
                except:
                    pass
                x += self.message_tiles.tile_width
                column += 1
                if column >= 30:
                    x = self.text_position[0]
                    y += self.message_tiles.tile_height
                    column = 0
                    row += 1
                    if row == 6:
                        row = 0
                        self.is_paused = True

        if self.show_continue_message:
            x = self.text_position[0]
            y = self.window_position[1] + self.window_tiles.tile_height * HUDMessageBox.MESSAGEBOX_HEIGHT
            for ch in HUDMessageBox.CONTINUE_TEXT:
                try:
                    self.prompt_tiles.blit(dst_surface, FONT_TEXT.index(ch), x, y)
                except:
                    pass
                x += self.prompt_tiles.tile_width

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
    def __init__(self, screen, player):
        self.screen = screen

        self.map_name_label = HUDLabel(16, 16, "Map Name")
        self.messagebox = HUDMessageBox()

        # This list is also the render order.
        self.elements = list()
        self.elements.append(self.map_name_label)
        self.elements.append(HUDHotKeySlot(player, 1))
        self.elements.append(HUDHotKeySlot(player, 2))
        self.elements.append(HUDHotKeySlot(player, 3))
        self.elements.append(HUDHotKeySlot(player, 4))
        self.elements.append(HUDHotKeySlot(player, 5))
        self.elements.append(HUDHotKeySlot(player, 6))
        self.elements.append(HUDHotKeySlot(player, 7))
        self.elements.append(HUDHotKeySlot(player, 8))
        self.elements.append(HUDHotKeySlot(player, 9))
        self.elements.append(HUDHotKeySlot(player, 0))
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
