from car import Car
from utils import image_util

class PoliceCar(Car):
    
    def __init__(self, image, x, y, game):
        super(PoliceCar, self).__init__(image, x, y, game)
        self.driving = True
        self.accel_change = 0.03
        self.drag = 0.2
        
        self.images = image_util.load_sliced_sprites(32, 64, "police_car.png")
        self.current_image = self.images[0]
    
    def handle_input(self):
        
        if not self.game.player.isInCar:
            self.forward_acceleration = 0
            self.side_acceleration = 0
            return
        
        dx = self.game.player.x - self.x
        dy = self.game.player.y - self.y

        if dx > 0:
            self.side_acceleration = min(self.max_side_acceleration, self.side_acceleration + self.accel_change)
        elif dx < 0:
            self.side_acceleration = max(-self.max_side_acceleration, self.side_acceleration - self.accel_change)
            
        if dy > 0:
            self.forward_acceleration = min(self.max_forward_acceleration, self.forward_acceleration + self.accel_change)
        elif dy < 0:
            self.forward_acceleration = max(-self.max_forward_acceleration, self.forward_acceleration - self.accel_change)

        
        
        