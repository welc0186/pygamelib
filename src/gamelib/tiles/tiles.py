from typing import Tuple


class TileMap:
    def __init__(self, tilesize: int = 16) -> None:
        self.tilesize = tilesize
        self.tiles: dict[Tuple[int,int], list] = {}