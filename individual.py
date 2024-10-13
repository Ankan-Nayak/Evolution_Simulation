import math
import random
import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Individual:
    def __init__(self,hp,vision,speed,mateSelectionProb,color,width,height,indiSize,maxVision):
        self.color = color
        self.hp = hp
        self.vision = vision
        self.speed = speed
        self.mateSelectionProb = mateSelectionProb # Prob of using biased random instead of tournament
        self.maxVision = maxVision
        self.angle = random.uniform(0, 2*math.pi)  # Initial random angle
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.width = width
        self.height = height
        self.indiSize = indiSize
        self.generation = 0

        
    def incerementGeneration(self): # To incrase generation count by 1
        self.generation += 1
        
    def eat(self,food):
        self.hp += food.hp
    
    def die(self):
        self.hp = 0

    def getFitness(self):
        return (self.hp/100)
    
    def seek(self, target_x, target_y):
        desired_velocity = pygame.math.Vector2(target_x - self.x, target_y - self.y).normalize() * self.speed
        steering = desired_velocity - pygame.math.Vector2(self.speed, 0).rotate(-math.degrees(self.angle))
        self.x += steering.x
        self.y += steering.y
        self.check_boundaries()

    def flee(self, target_x, target_y):
        desired_velocity = pygame.math.Vector2(self.x - target_x, self.y - target_y).normalize() * self.speed
        steering = desired_velocity - pygame.math.Vector2(self.speed, 0).rotate(-math.degrees(self.angle))
        self.x += steering.x
        self.y += steering.y
        self.check_boundaries()

    def move_towards(self, target_x, target_y):
        self.seek(target_x, target_y)

    def move_away(self, target_x, target_y):
        self.flee(target_x, target_y)

    def random_movement(self):
        self.angle += random.uniform(-1, 1)  # Add a small random angle change
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.check_boundaries()

    def social_interaction(self, other):
        # Social interaction logic
        distance = math.hypot(self.x - other.x, self.y - other.y)

        if distance < self.indiSize + other.indiSize:
            # Individuals are close enough for social interaction
            self.hp += 5  # Increase health of the current individual
            other.hp += 5  # Increase health of the other individual

    def adaptive_learning(self):
        # Adaptive learning logic
        vision_change = random.uniform(-1, 1)  # Randomly adjust vision
        speed_change = random.uniform(-0.5, 0.5)  # Randomly adjust speed

        self.vision = max(1, min(self.maxVision, self.vision + vision_change))
        self.speed = max(1, self.speed + speed_change)

    def check_boundaries(self):
        # Ensure agents stay within the screen boundaries
        self.x = max(0, min(self.x, self.width))
        self.y = max(0, min(self.y, self.height))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.indiSize)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.vision, width=1)
        # pygame.draw.line(screen,RED, (self.x, self.y), (self.x + self.visionRadius*math.sin(self.angle), self.y + self.visionRadius*math.cos(self.angle)))
        # pygame.draw.line(screen,BLUE, (self.x, self.y), (self.x + self.visionRadius*math.sin(self.angle + self.vision), self.y + self.visionRadius*math.cos(self.angle + self.vision)))
        # pygame.draw.line(screen,BLUE, (self.x, self.y), (self.x + self.visionRadius*math.sin(self.angle), self.y + self.visionRadius*math.cos(self.angle)))


