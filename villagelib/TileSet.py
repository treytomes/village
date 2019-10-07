import pygame


class TileSet:
    """Break an image into a series of tiles."""

    def __init__(self, filename, columns, rows):
        self.filename = filename
        self.rows = rows
        self.columns = columns
        self.image = pygame.image.load(filename).convert_alpha()
        self.image.set_colorkey((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.tile_width = self.rect.w // self.columns
        self.tile_height = self.rect.h // self.rows

    def clone(self):
        tiles = TileSet(self.filename, self.columns, self.rows)
        tiles.image = pygame.Surface((self.image.get_width(), self.image.get_height()), self.image.get_flags(),
                                     self.image.get_bitsize(), self.image.get_masks())
        tiles.image.blit(self.image, (0, 0))  # copy any changes made to the source tileset
        tiles.rect = self.image.get_rect()
        tiles.tile_width = self.tile_width
        tiles.tile_height = self.tile_height
        tiles.image.set_colorkey(self.image.get_colorkey())
        return tiles

    def scale(self, factor):
        """Resize the width and height by a scalar value."""
        self.image = pygame.transform.scale(self.image, (self.rect.w * factor, self.rect.h * factor))
        self.rect = self.image.get_rect()
        self.tile_width *= factor
        self.tile_height *= factor

    def blit(self, target_surface, tile_index, x, y):
        tile_column = tile_index % self.columns
        tile_row = tile_index // self.columns
        tile_x = tile_column * self.tile_width
        tile_y = tile_row * self.tile_height
        target_surface.blit(self.image, [x, y], [tile_x, tile_y, self.tile_width, self.tile_height])

    def blit_top(self, target_surface, tile_index, x, y):
        """Only blit the top half of the tile.  This is useful when rendering on top of "tall" tiles."""
        tile_column = tile_index % self.columns
        tile_row = tile_index // self.columns
        tile_x = tile_column * self.tile_width
        tile_y = tile_row * self.tile_height
        target_surface.blit(self.image, [x, y], [tile_x, tile_y, self.tile_width, self.tile_height // 2])

    def get_rect(self):
        """Create a new Rect to represent a tile from this TileSet."""
        return pygame.Rect(0, 0, self.tile_width, self.tile_height)

    def recolor_image(self, dst_colors):
        """
        Do a direct replacement of the src_colors set with dst_colors.
        
        This method will take the source color, then divide it by (256 / len(dst_colors)), then pick that color from the dst_colors array.
        Sort of like what Minicraft does to color it's tiles.
        """

        src_colors = ((0, 0, 0), (81, 81, 81), (173, 173, 173), (255, 255, 255))
        pixels = pygame.PixelArray(self.image)
        for n in range(0, len(dst_colors)):
            pixels.replace(src_colors[n], dst_colors[n])
        
        # This bit would be necessary if it were a palette-based image.
        #divisor = 256 // len(dst_colors)
        #palette = self.image.get_palette()
        #for n in range(len(palette)):
        #    dst_index = palette[n][0] // divisor
        #    self.image.set_palette_at(n, dst_colors[dst_index])
