import pygame
import time
import random

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)

# Screen dimensions
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1200

# Snake dimensions
SNAKE_BLOCK = 30

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Set font for score and level
font_style = pygame.font.SysFont("bahnschrift", 50)
score_font = pygame.font.SysFont("comicsansms", 40)


# Function to display the current score and level
def message(msg, color, x, y):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [x, y])


def gameLoop():
    # Game settings
    game_over = False
    game_close = False

    # Snake starting position
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2
    x1_change = 0
    y1_change = 0

    # Snake body and length
    snake_List = []
    Length_of_snake = 1

    # Food position
    foodx = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    food_spawn_time = time.time()

    # Initial score and level
    score = 0
    level = 1
    speed = 15  # Initial speed of snake

    # Clock to control game speed
    clock = pygame.time.Clock()

    # Game loop
    while not game_over:

        while game_close:
            screen.fill(BLUE)
            message("You Lost! Press Q-Quit or C-Play Again", RED, SCREEN_WIDTH // 2.5, SCREEN_HEIGHT // 3)
            message("Score: " + str(score), GREEN, SCREEN_WIDTH / 2.2, SCREEN_HEIGHT / 2)
            message("Level: " + str(level), GREEN, SCREEN_WIDTH / 2.2, SCREEN_HEIGHT / 2 + 40)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Check for border collision
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLUE)

        if time.time() - food_spawn_time > 5:
            # Reset food to a new random position
            foodx = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            food_spawn_time = time.time()  

        # Draw food
        pygame.draw.rect(screen, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        # Snake body logic
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check for collision with itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw snake
        for block in snake_List:
            pygame.draw.rect(screen, WHITE, [block[0], block[1], SNAKE_BLOCK, SNAKE_BLOCK])

        # Display score and level
        message("Score: " + str(score), GREEN, 0, 0)
        message("Level: " + str(level), GREEN, SCREEN_WIDTH - 100, 0)

        # Update the screen
        pygame.display.update()

        # Check if snake eats food
        if abs(x1 - foodx) < SNAKE_BLOCK and abs(y1 - foody) < SNAKE_BLOCK:
            foodx = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1
            score += 10

            # Check if the snake reaches the next level
            if score % 30 == 0:  # Level up after 3 foods (30 points)
                level += 1
                speed += 5  # Increase speed when level up

        # Control the speed of the game
        clock.tick(speed)

    pygame.quit()
    quit()


# Start the game loop
gameLoop()
