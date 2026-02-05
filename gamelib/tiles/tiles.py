from typing import Any, Tuple

import pygame

T_TileMap = dict[Tuple[int, int], list]


class TileMap:
    def __init__(self, tilesize: int = 16) -> None:
        self.tilesize = tilesize
        self.tiles: dict[Tuple[int, int], Any] = {}

    def add_to_tile(self, tile: Tuple[int, int], object: Any) -> T_TileMap:
        if tile not in self.tiles:
            self.tiles[tile] = []
        self.tiles[tile] = object
        return self.tiles

    def add_to_tiles(self, tiles: list[Tuple[int, int]], object: Any) -> T_TileMap:
        for tile in tiles:
            self.add_to_tile(tile, object)
        return self.tiles

    @property
    def min_x(self) -> int:
        xs = [x for x, _ in self.tiles.keys()]
        return min(xs)

    @property
    def min_y(self) -> int:
        ys = [y for _, y in self.tiles.keys()]
        return min(ys)

    @property
    def max_x(self) -> int:
        xs = [x for x, _ in self.tiles.keys()]
        return max(xs)

    @property
    def max_y(self) -> int:
        ys = [y for _, y in self.tiles.keys()]
        return max(ys)

    def get_unit_size(self) -> Tuple[int, int]:
        width = self.max_x - self.min_x + 1
        height = self.max_y - self.min_y + 1

        return width, height


class SpriteTileMap(TileMap):
    def generate_surface(self) -> pygame.Surface:
        # determine bounds so negative coordinates are supported
        width, height = self.get_unit_size()

        surface = pygame.Surface(
            (self.tilesize * width, self.tilesize * height), pygame.SRCALPHA
        )
        for coords, tile_sprite in self.tiles.items():
            if not isinstance(tile_sprite, pygame.Surface):
                continue
            pos = (
                (coords[0] - self.min_x) * self.tilesize,
                (coords[1] - self.min_y) * self.tilesize,
            )
            surface.blit(tile_sprite, pos)
        return surface
