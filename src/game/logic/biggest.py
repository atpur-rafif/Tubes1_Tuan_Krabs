from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

MAX_DIAMOND = 5

class BiggestLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.target = None

    def goto(self, bot_position: tuple[int, int], target_position: tuple[int, int]):
        return get_direction(bot_position.x, bot_position.y, target_position.x, target_position.y)

    def jarak(self, bot_position: tuple[int, int], target_position: tuple[int, int]):
        return abs(bot_position.x-target_position.x) + abs(bot_position.y-target_position.y)

    def next_move(self, board_bot: GameObject, board: Board):
        bot_properties = board_bot.properties
        bot_positions = board_bot.position
        base = board_bot.properties.base
        boardObj = board.game_objects
        # Analyze new state
        if bot_properties.diamonds == 5:
            # Move to base
            return self.goto(bot_positions,base)
        
        teleport_target: list[GameObject] = list(filter(lambda x: x.type == "TeleportGameObject" and x.type != None, boardObj))
        teleport_positions = list(map(lambda x: x.position, teleport_target))
        targetTeleportIn = min(teleport_positions, key=lambda pos: abs(bot_positions.x - pos.x) + abs(bot_positions.y - pos.y))
        targetTeleportOut = max(teleport_positions, key=lambda pos: abs(bot_positions.x - pos.x) + abs(bot_positions.y - pos.y))

        red_button_list : list[GameObject] = list(filter(lambda x: x.type == "DiamondButtonGameObject" and x.type != None, boardObj)) 
        red_button_pos = list(map(lambda x: x.position, red_button_list))

        diamond_target: list[GameObject] = list(filter(lambda v: v.properties.points <= MAX_DIAMOND - bot_properties.diamonds, board.diamonds))
        diamond_positions = list(map(lambda v: v.position, diamond_target))

        if len(diamond_target) == 0:
            self.target = None

        if bot_properties.diamonds == 5 or len(diamond_target) == 0:
            return self.goto(bot_positions,base)

        if self.target != None and self.jarak(bot_positions, self.target) == 0:
            self.target = None

        n = 5
        diamond_count = 0
        biggest_diamond = 0
        temp_biggest_diamond = []
        list_biggest_diamond = []
        for i in range (board.width-n):     #column
            for j in range (board.width-n): #row
                for k in range (n+1):         #column
                    for l in range (n+1):     #row
                        for element in (diamond_positions):
                            if i+k == element.x and j+l == element.y:
                                diamond_count += 1
                                temp_biggest_diamond.append(element)
                if diamond_count > biggest_diamond:
                    biggest_diamond = diamond_count
                    list_biggest_diamond = temp_biggest_diamond
                diamond_count = 0
                temp_biggest_diamond = []
            diamond_count = 0
            temp_biggest_diamond = []

        target = min(list_biggest_diamond, key=lambda pos: abs(bot_positions.x - pos.x) + abs(bot_positions.y - pos.y))
        
        if self.target == None:
            self.target = target
        else:
            nearest_target = min(diamond_positions, key=lambda pos: abs(bot_positions.x - pos.x) + abs(bot_positions.y - pos.y))
            if self.jarak(bot_positions, self.target) <= 3 :
                if self.jarak(bot_positions, nearest_target) <= 3:
                    self.target = nearest_target
                else:
                    self.target = target
            else:
                self.target = target

        if self.jarak(bot_positions, self.target) > self.jarak(bot_positions, red_button_pos[0]):
            self.target = red_button_pos[0]

        if self.jarak(targetTeleportOut, self.target) + self.jarak(targetTeleportIn, bot_positions) < self.jarak(bot_positions, self.target):
            self.target = targetTeleportIn
            
        delta_x, delta_y = get_direction(
            bot_positions.x,
            bot_positions.y,
            self.target.x,
            self.target.y,
        )

        return delta_x, delta_y
