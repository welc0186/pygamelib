from typing import Any, Tuple, Callable, Optional, Union
import csv

import pygame

T_TileMap = dict[Tuple[int, int], Any]


class TileMap:
    def __init__(self, tilesize: int = 16) -> None:
        self.tilesize = tilesize
        self.tiles: dict[Tuple[int, int], Any] = {}

    @classmethod
    def from_csv(
        cls,
        csv_path: str,
        tilesize: int = 16,
        mapper: Optional[Union[dict[int, Any], Callable[[int], Any]]] = None,
        delimiter: str = ",",
        start_pos: Tuple[int, int] = (0, 0),
        ignore_values: Optional[set[int]] = None,
    ) -> "TileMap":
        """Load a tilemap from a CSV file of integers.

        - Each CSV row becomes a Y row (0 = top) and each column becomes X (0 = left).
        - `start_pos` offsets the coordinates written into `self.tiles`.
        - `mapper` may be a dict mapping int->object or a callable taking an int and
          returning an object. If `mapper` does not provide an object for a value,
          that tile is skipped.
        - `ignore_values` can be used to skip specific integer values (e.g. {0}).
        Returns the internal tiles dict.
        """
        sx, sy = start_pos
        tilemap = cls(tilesize=tilesize)
        with open(csv_path, newline="") as fh:
            reader = csv.reader(fh, delimiter=delimiter)
            for y, row in enumerate(reader):
                for x, cell in enumerate(row):
                    cell = cell.strip()
                    if cell == "":
                        continue
                    try:
                        val = int(cell)
                    except ValueError:
                        continue
                    if ignore_values and val in ignore_values:
                        continue

                    obj: Any
                    if mapper is None:
                        obj = val
                    elif callable(mapper):
                        obj = mapper(val)
                    else:
                        # dict-like
                        if val not in mapper:
                            continue
                        obj = mapper[val]

                    if obj is None:
                        continue

                    coord = (sx + x, sy + y)
                    tilemap.add_to_tile(coord, obj)

        return tilemap

    def add_to_tile(self, tile: Tuple[int, int], object: Any) -> T_TileMap:
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
