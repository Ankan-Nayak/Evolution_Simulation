import pygame
import sys
import math
import random
from world import World
import pandas as pd

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define simulation parameters
width, height = 1500, 750

# Define agent parameters
num_preds = 200
num_indis = 400
num_food = 1500
mutationChance = 0.1

fps = 500

pred_speed = 5
indi_speed = 5

food_size = 0.5
pred_size = 1
indi_size = 1

vision = math.radians(90)  # Field of vision angle for both pred and indi
vision = 10  # Field of vision radius for both pred and indi

indiVisionRange = 20
predVisionRange = 20

def saveStats(stats):
    df = pd.DataFrame(stats)
    df.to_csv('Stats.csv')

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("pred-indi Simulation")
    clock = pygame.time.Clock()

    stats = []

    font_big = pygame.font.Font('freesansbold.ttf', 30)
    font_small = pygame.font.Font('freesansbold.ttf', 20)
    # self,indiPop,predPop,foodCount,mutationChance,width,height,predSpeed,indiSpeed,foodSize,predSize,indiSize
    w = World(indiPop = num_indis,
              predPop = num_preds,
              foodCount = num_food,
              mutationChance = mutationChance,
              width=width,
              height=height,
              predSpeed = 2,
              indiSpeed = 2,
              foodSize = 3,
              predSize = 4,
              indiSize = 4,
              indiVisionRange = indiVisionRange,
              predVisionRange = predVisionRange,
              )
    w.spawn(num_indis,num_preds,num_food)
    gen = 0
    is_game_start = True
    
    while is_game_start:
        preds = w.preds
        indis = w.indis
        foods = w.food
        count = 0
        gen+=1
        while is_game_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    saveStats(stats)
                    sys.exit()

            # pred behavior
            for pred in preds.copy():
                if pred.hp <= 0:
                    preds.remove(pred)
                    continue

                found_indi = False
                for indi in indis.copy():
                    dist = math.hypot(indi.x - pred.x, indi.y - pred.y)
                    if dist <= pred.vision:
                        if dist < 10:
                            pred.eat(indi)
                            indis.remove(indi)
                            found_indi = True
                            break
                        pred.move_towards(indi.x, indi.y)
                        found_indi = True
                        break

                if not found_indi:
                    pred.random_movement()

            # Individual behavior
            for indi in indis.copy():
                if indi.hp <= 0:
                    indis.remove(indi)
                    continue

                found_pred = False
                for pred in preds.copy():
                    if math.hypot(pred.x - indi.x, pred.y - indi.y) <= indi.vision:
                        indi.move_away(pred.x, pred.y)
                        found_pred = True
                        break

                for food in foods.copy():
                    dist = math.hypot(food.x - indi.x, food.y - indi.y)
                    if dist <= indi.vision:
                        if dist < 10:
                            indi.eat(food)
                            foods.remove(food)
                            found_pred = True
                            break
                        indi.move_towards(food.x, food.y)
                        found_pred = True
                        break

                if not found_pred:
                    indi.random_movement()

            # Draw everything
            screen.fill(WHITE)
            for food in foods:
                food.draw(screen)
            for pred in preds:
                pred.draw(screen)
                pred.hp-= ((pred.speed**2)*0.05 + pred.vision*0.1)
            for indi in indis:
                indi.draw(screen)
                indi.hp-= ((indi.speed**2)*0.01 + indi.vision*0.1)
            
            indiCount = "No. of Indis left : " + str(len(indis))
            indiCountText = font_small.render(indiCount, True, GREEN)
            indi_text_rect = indiCountText.get_rect(center=(width // 4, 20))
            
            predCount = "No. of Preds left : " + str(len(preds))
            predCountText = font_small.render(predCount, True, RED)
            pred_text_rect = predCountText.get_rect(center=(3*width // 4, 20))

            generation_count = "Genertation : " + str(gen)
            genCountText = font_small.render(generation_count, True, BLACK)
            gen_text_rect = genCountText.get_rect(center=(width//2,20))

            screen.blit(indiCountText, indi_text_rect)
            screen.blit(predCountText, pred_text_rect)
            screen.blit(genCountText, gen_text_rect)
            
            pygame.display.flip()
            count+=1
            # print(count)
            if count == 200:
                is_game_start = False
                break
            clock.tick(fps)
            if len(foods) == 0 or len(indis) == 0 or len(preds) == 0:
                is_game_start = False
        
        if len(indis) == 0 or len(foods) == 0 or len(preds) ==0:
            message = ""
            if len(indis) == 0:
                message = "All Indis dead"
            if len(foods) == 0:
                message = "All Food Eaten"
            if len(preds) == 0:
                message = "All Preds Dead"
            text = font_big.render(message, True, RED)
            text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
            restart_button = pygame.Rect(width // 2 - 60, height // 2 + 20, 120, 40)

            while is_game_start == False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        saveStats(stats)
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and restart_button.collidepoint(event.pos):
                            is_game_start = True
                            stats = []
                            gen = 0
                            w.spawn(num_indis,num_preds,num_food)
                            break

                screen.fill(WHITE)
                screen.blit(text, text_rect)

                pygame.draw.rect(screen, GREEN, restart_button)
                restart_text = font_small.render("Restart", True, WHITE)
                restart_rect = restart_text.get_rect(center=restart_button.center)
                screen.blit(restart_text, restart_rect)

                pygame.display.flip()
                clock.tick(30)
            
        else:
            w.indis = indis
            w.preds = preds
            w.newGeneration()
            indis = w.indis
            preds = w.preds
            if len(w.indis)>1 and len(w.preds) > 1:
                stats.append(w.getStats(gen))
            is_game_start = True
        

if __name__ == "__main__":
    # Initialize Pygame
    # pygame.init()

    # Initialize the mixer
    pygame.mixer.init()

    # Now load the sound
    audio1 = pygame.mixer.Sound("sound/sfx/points.mp3")
    audio2 = pygame.mixer.Sound("sound/sfx/dead.mp3")
    audio3 = pygame.mixer.Sound("sound/sfx/jump.mp3")

    audio1.play()
    audio2.play()
    audio3.play()
    main()
    