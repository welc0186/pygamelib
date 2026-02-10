from pytmx.util_pygame import pygame_image_loader
from pytmx import TiledMap
import pygame


class TmxImageTileMap(TiledMap):
    def __init__(self, filename: str):
        super().__init__(filename, image_loader=pygame_image_loader)

    def generate_surface(self) -> pygame.Surface:
        surface = pygame.Surface(
            (self.width * self.tilewidth, self.height * self.tileheight),
            pygame.SRCALPHA,
        )

        for layer in self.layers:
            for x, y, image in layer.tiles():
                if isinstance(image, pygame.Surface):
                    surface.blit(image, (x * self.tilewidth, y * self.tileheight))

        return surface
