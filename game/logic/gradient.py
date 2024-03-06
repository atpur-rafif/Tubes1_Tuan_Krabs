from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from game.util import get_direction

MAX_DIAMOND = 5
def manhattan_distance(a: Position, b: Position):
    return abs(a.x - b.x) + abs(a.y - b.y)

class GradientLogic(BaseLogic):
    bot: GameObject
    bot_pos: Position
    board: Board
    inventory_size: int

    def __init__(self):
        self.inventory_size = 0;
        self.directions: list[Position] = [
            Position(1, 0),
            Position(0, 1),
            Position(-1, 0),
            Position(0, -1)
        ]

    def fn(self, inp: Position):
        total = 0
        for diamond in self.board.diamonds:
            pos = diamond.position
            points = diamond.properties.points
            if self.inventory_size - self.bot.properties.diamonds < points:
                continue
            rep = max(manhattan_distance(inp, pos), 0.1) * points
            total += 1/(rep * rep)

        for bot in self.board.bots:
            pos = bot.position
            if pos == self.bot_pos:
                continue
            distance = max(manhattan_distance(inp, pos), 1)
            if distance > 2:
                continue
            total += (3 * (self.bot.properties.diamonds/self.inventory_size)) / (distance * distance)

        return total

    def next_move(self, board_bot: GameObject, board: Board):
        self.board = board
        self.bot = board_bot
        self.bot_pos = board_bot.position

        bot_provider = next(filter(lambda v: v.name == "BotProvider", board.features))
        if hasattr(bot_provider, "config") and hasattr(bot_provider.config, "inventory_size"):
            inv = bot_provider.config.inventory_size
            if type(inv) == int:
                self.inventory_size = inv

        if board_bot.properties.diamonds == self.inventory_size:
            base = board_bot.properties.base
            return get_direction(self.bot_pos.x, self.bot_pos.y, base.x, base.y)

        bot_dir = max(self.directions, key=lambda dir: self.fn(
            Position(
                self.bot_pos.y + dir.y,
                self.bot_pos.x + dir.x 
            )
        ))
        # for i in range(15):
        #     for j in range(15):
        #         print(f"{self.fn(j, i):02f}", end=" ")
        #     print('')
        return (bot_dir.x, bot_dir.y)
