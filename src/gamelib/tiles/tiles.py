from typing import Any, Tuple

import pygame

T_TileMap = dict[Tuple[int, int], list]


class TileMap:
    def __init__(self, tilesize: int = 16) -> None:
        self.tilesize = tilesize
        self.tiles: dict[Tuple[int, int], Any] = {}

    def add_to_tile(self, tile: Tuple[int, int], object: Any) -> T_TileMap:
        if not tile in self.tiles:
            self.tiles[tile] = []
        self.tiles[tile] = object
        return self.tiles

    def add_to_tiles(self, tiles: list[Tuple[int, int]], object: Any) -> T_TileMap:
        for tile in tiles:
            self.add_to_tile(tile, object)
        return self.tiles

    def get_unit_size(self) -> Tuple[int, int]:
        xs = [x for x, _ in self.tiles.keys()]
        ys = [y for _, y in self.tiles.keys()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        return width, height


class SpriteTileMap(TileMap):
    def generate_surface(self) -> pygame.Surface:
        surface = pygame.Surface([self.tilesize * dim for dim in self.get_unit_size()])
        for coords in self.tiles:
            tile_sprite = self.tiles[coords]
            if not isinstance(tile_sprite, pygame.Surface):
                continue
            surface.blit(tile_sprite, [self.tilesize * coord for coord in coords])
        return surface
