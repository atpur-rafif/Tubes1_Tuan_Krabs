from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from game.util import get_direction, position_equals

MAX_DIAMOND = 5
def manhattan_distance(a: Position, b: Position):
    return abs(a.x - b.x) + abs(a.y - b.y)

def add_position(a: Position, b: Position):
    return Position(a.y + b.y, a.x + b.x)

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

    def base_fn(self, inp: Position, distance_offset: int):
        total = 0.0
        inventory_filled = float(self.bot.properties.diamonds) / float(self.inventory_size)

        bots = self.board.bots
        diamonds = self.board.diamonds
        redButton_target: list[GameObject] = list(filter(lambda x: x.type == "DiamondButtonGameObject", self.board.game_objects)) 

        for diamond in diamonds:
            pos = diamond.position
            points = diamond.properties.points
            if self.inventory_size - self.bot.properties.diamonds < points:
                continue

            distance = manhattan_distance(inp, pos) + distance_offset
            if distance == 0:
                total += points * 100;
            elif points == 1:
                total += distance ** -2
            else:
                total += (distance ** -1) * points

        for button in redButton_target:
            pos = button.position
            distance = manhattan_distance(inp, pos) + distance_offset
            if distance == 0:
                total -= 1;

        for bot in bots:
            pos = bot.position
            if pos == self.bot_pos:
                continue
            distance = max(manhattan_distance(inp, pos) + distance_offset, 1)
            if distance > 2: 
                continue
            if inventory_filled > 3/4:
                total -= (2 * inventory_filled) * (distance ** -2)
            elif inventory_filled < 1/4:
                other_base_distance = manhattan_distance(bot.properties.base, pos)
                if other_base_distance < 8:
                    other_inventory = float(bot.properties.diamonds) / float(self.inventory_size)
                    total += (other_inventory * 2) * (distance ** -2)

        base = self.bot.properties.base
        distance = max(manhattan_distance(inp, base) + distance_offset, 0.1)
        total += (2 * inventory_filled) * (distance ** -2)

        return total

    def fn(self, inp: Position):
        base_value = self.base_fn(inp, 0) 
        teleporter: list[GameObject] = list(filter(lambda x: x.type == "TeleportGameObject", self.board.game_objects))
        tel0 = teleporter[0].position
        tel1 = teleporter[1].position
        if manhattan_distance(tel0, tel1) < 5:
            if position_equals(inp, tel0) or position_equals(inp, tel1):
                return 0
            return base_value

        tel0_value = self.base_fn(tel1, manhattan_distance(tel0, inp))
        tel1_value = self.base_fn(tel0, manhattan_distance(tel1, inp))
        return base_value + tel0_value + tel1_value

    def next_move(self, board_bot: GameObject, board: Board):
        self.board = board
        self.bot = board_bot
        self.bot_pos = board_bot.position

        bot_provider = next(filter(lambda v: v.name == "BotProvider", board.features))
        if hasattr(bot_provider, "config") and hasattr(bot_provider.config, "inventory_size"):
            inv = bot_provider.config.inventory_size
            if type(inv) == int:
                self.inventory_size = inv

        possible_next_pos = list(
                filter(
                    lambda pos: 0 <= pos.x and pos.x < board.width and 0 <= pos.y and pos.y < board.height,
                    map(lambda dir: add_position(self.bot_pos, dir), self.directions)
                )
            )

        next_pos = max(possible_next_pos, key=lambda pos: self.fn(pos))

        return get_direction(self.bot_pos.x, self.bot_pos.y, next_pos.x, next_pos.y)

