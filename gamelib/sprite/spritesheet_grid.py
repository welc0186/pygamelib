import pygame


class SpriteSheetGrid:
    def __init__(self, image_path: str, cell_width: int, cell_height: int):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.cell_width = cell_width
        self.cell_height = cell_height

        self.sheet_width, self.sheet_height = self.image.get_size()
        self.cols = self.sheet_width // cell_width
        self.rows = self.sheet_height // cell_height

        self.sprites: list[list[pygame.Surface]] = []
        self._slice()

    def _slice(self):
        """Slice the spritesheet into a 2D grid."""
        self.sprites = []

        for y in range(self.rows):
            row = []
            for x in range(self.cols):
                rect = pygame.Rect(
                    x * self.cell_width,
                    y * self.cell_height,
                    self.cell_width,
                    self.cell_height,
                )
                surface = pygame.Surface(
                    (self.cell_width, self.cell_height), pygame.SRCALPHA
                )
                surface.blit(self.image, (0, 0), rect)
                row.append(surface)
            self.sprites.append(row)

    def get(self, x: int, y: int) -> pygame.Surface:
        """Get sprite at grid coordinate (x, y)."""
        return self.sprites[y][x]

    def get_by_index(self, index: int) -> pygame.Surface:
        """Get sprite by linear index (row-major order).

        Index 0 is the upper-left cell; the last index is the lower-right.
        """
        total = self.rows * self.cols
        if index < 0 or index >= total:
            raise IndexError(f"Sprite index out of range: {index}")
        x = index % self.cols
        y = index // self.cols
        return self.get(x, y)

    def make_key_image(self, font_size: int = 14) -> pygame.Surface:
        """
        Returns a debug image showing the spritesheet with grid lines
        and (x,y) coordinates in each cell.
        """
        key_image = self.image.copy()
        overlay = pygame.Surface(key_image.get_size(), pygame.SRCALPHA)

        font = pygame.font.SysFont(None, font_size)

        # Draw grid + coordinates
        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(
                    x * self.cell_width,
                    y * self.cell_height,
                    self.cell_width,
                    self.cell_height,
                )

                # Grid
                pygame.draw.rect(overlay, (0, 255, 0, 120), rect, 1)

                # Label
                label = font.render(f"{x},{y}", True, (255, 0, 0))
                overlay.blit(label, (rect.x + 2, rect.y + 2))

        key_image.blit(overlay, (0, 0))
        return key_image

    def save_key_image(self, filename: str):
        """Generate and save the key image to disk."""
        img = self.make_key_image()
        pygame.image.save(img, filename)
