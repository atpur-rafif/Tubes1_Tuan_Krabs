from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from game.util import get_direction


MAX_DIAMOND = 5

class TestLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def goto(self, bot_position: tuple[int, int], target_position: tuple[int, int]):
        return get_direction(bot_position.x, bot_position.y, target_position.x, target_position.y)

    def next_move(self, board_bot: GameObject, board: Board):
        bot_properties = board_bot.properties
        bot_positions = board_bot.position
        if bot_properties == None:
            raise

        target = None
        base = bot_properties.base
        if bot_properties.diamonds == 5:
            return self.goto(bot_positions, base)

        diamond_target: list[GameObject] = list(filter(lambda v: v.properties.points <= MAX_DIAMOND - bot_properties.diamonds, board.diamonds))

        if len(diamond_target) == 0:
            return self.goto(bot_positions, base)
        else:
            diamond_positions = list(map(lambda v: v.position, diamond_target))
            target = min(diamond_positions, key=lambda pos: abs(bot_positions.x - pos.x) + abs(bot_positions.y - pos.y))

        return get_direction(bot_positions.x, bot_positions.y, target.x, target.y)
