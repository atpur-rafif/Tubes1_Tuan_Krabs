from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from game.util import get_direction


MAX_DIAMOND = 5

class NearestLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def goto(self, bot_position: tuple[int, int], target_position: tuple[int, int]):
        return get_direction(bot_position.x, bot_position.y, target_position.x, target_position.y)
    
    def intJarak (self, Asal: Position, Tujuan: Position):
        return (abs(Asal.x - Tujuan.x) + abs(Asal.y - Tujuan.y))

    def next_move(self, board_bot: GameObject, board: Board):
        mybot_props = board_bot.properties
        mybot_position = board_bot.position
        base_position = mybot_props.base
        gameOBJ = board.game_objects


        #mencari koordinat semua diamond
        diamond_target: list[GameObject] = list(filter(lambda x: x.properties.points <= MAX_DIAMOND - mybot_props.diamonds, board.diamonds))
        diamond_positions = list(map(lambda x: x.position, diamond_target))

        #mencari koordinat semua teleport
        teleport_target: list[GameObject] = list(filter(lambda x: x.type == "TeleportGameObject" and x.type != None, gameOBJ))
        teleport_positions = list(map(lambda x: x.position, teleport_target))
        targetTeleportIn = min(teleport_positions, key=lambda pos: abs(mybot_position.x - pos.x) + abs(mybot_position.y - pos.y))
        targetTeleportOut = max(teleport_positions, key=lambda pos: abs(mybot_position.x - pos.x) + abs(mybot_position.y - pos.y))

        redButton_target: list[GameObject] = list(filter(lambda x: x.type == "DiamondButtonGameObject" and x.type != None, gameOBJ)) 
        redButton_positions = list(map(lambda x: x.position, redButton_target))



        if mybot_props == None:
            raise

        #KEMBALI KE BASE
        if mybot_props.diamonds == 5:
            jarakToBase = self.intJarak(mybot_position, base_position)
            jarakToBase_withTeleport = self.intJarak(mybot_position,targetTeleportIn) + self.intJarak(targetTeleportOut,base_position)

            if jarakToBase <= jarakToBase_withTeleport:
                return get_direction(mybot_position.x, mybot_position.y, base_position.x, base_position.y)
            else:
                if self.intJarak(mybot_position,targetTeleportIn) == 0:
                    if mybot_position.x == 14:
                        return get_direction(mybot_position.x, mybot_position.y, mybot_position.x - 1, mybot_position.y)
                    else:  
                        return get_direction(mybot_position.x, mybot_position.y, mybot_position.x + 1, mybot_position.y)

                return get_direction(mybot_position.x, mybot_position.y, targetTeleportIn.x, targetTeleportIn.y)
            # return self.goto(mybot_position, base)
        

        #ALGORITMA MENCARI DIAMOND
        if len(diamond_target) == 0:
            return self.goto(mybot_position, base_position)
        else:
            #cari diamond yang bisa diambil
            targetDiamonds = min(diamond_positions, key=lambda pos: abs(mybot_position.x - pos.x) + abs(mybot_position.y - pos.y))
            targetDiamondsWithTeleport = min(diamond_positions, key=lambda pos: abs(targetTeleportOut.x - pos.x) + abs(targetTeleportOut.y - pos.y))

            jarakToDiamond = self.intJarak(mybot_position,targetDiamonds) #jarak ke diamond terdekat tanpa teleport
            jarakWithTeleport = self.intJarak(mybot_position,targetTeleportIn) + self.intJarak(targetTeleportOut,targetDiamondsWithTeleport) #jarak ke diamond terdekat pakai teleport

            jarakToButton = self.intJarak(mybot_position, redButton_positions[0])

            if jarakToButton < jarakToDiamond and jarakToButton < jarakWithTeleport:
                return get_direction(mybot_position.x, mybot_position.y, redButton_positions[0].x, redButton_positions[0].y)  
            #cari jarak ke diamond terdekat
            if jarakToDiamond <= jarakWithTeleport:
                return get_direction(mybot_position.x, mybot_position.y, targetDiamonds.x, targetDiamonds.y)  
            else:  
                if self.intJarak(mybot_position,targetTeleportIn) == 0:
                    if mybot_position.x == 14:
                        return get_direction(mybot_position.x, mybot_position.y, mybot_position.x - 1, mybot_position.y)
                    else:  
                        return get_direction(mybot_position.x, mybot_position.y, mybot_position.x + 1, mybot_position.y)

                return get_direction(mybot_position.x, mybot_position.y, targetTeleportIn.x, targetTeleportIn.y)  




        
