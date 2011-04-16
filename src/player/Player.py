from game_objects.GameObject import GameObject

class Player(GameObject):
    
    def __init__(self, game, x, y):
        self.game = game
        
        return
    
    def draw(self):
        return