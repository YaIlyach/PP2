import pygame
import time
import random
import psycopg2

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

# Set font
font_style = pygame.font.SysFont("bahnschrift", 50)
score_font = pygame.font.SysFont("comicsansms", 40)

# Database connection settings
CONFIG: dict = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()

# Display score and level func
def message(msg, color, x, y):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [x, y])

def get_user(username):
    cursor.execute("SELECT id FROM public.user WHERE username = %s", (username,))
    return cursor.fetchone()

def create_user(username):
    cursor.execute("INSERT INTO public.user (username) VALUES (%s) RETURNING id", (username,))
    conn.commit()
    return cursor.fetchone()[0]

def get_user_score(user_id):
    cursor.execute("SELECT level, score FROM public.user_score WHERE user_id = %s", (user_id,))
    return cursor.fetchone()

def save_score(user_id, level, score):
    cursor.execute("""
        INSERT INTO public.user_score (user_id, level, score)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET level = EXCLUDED.level, score = EXCLUDED.score
    """, (user_id, level, score))
    conn.commit()

# Function to handle the user input for the username
def enter_username():
    username = ""
    input_active = True
    while input_active:
        screen.fill(BLUE)
        message("Enter your username: ", WHITE, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3)
        message(username, WHITE, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3 + 100)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

    return username

# Game Loop
def gameLoop():
    i = 0
    game_over = False
    game_close = False

    # Get user information
    username = enter_username()
    user = get_user(username)
    if user:
        user_id = user[0]
        user_score = get_user_score(user_id)
        print(f"Welcome back, {username}! Your current level is {user_score[0]} and your score is {user_score[1]}")
    else:
        print("User not found. Creating a new user...")
        user_id = create_user(username)
        print(f"User created! Welcome, {username}!")

    # Get user score and level
    user_score = get_user_score(user_id)
    score = user_score[1] if user_score else 0
    level = user_score[0] if user_score else 1
    speed = 15  # Initial speed of snake

    # Snake starting position
    x1 = ((SCREEN_WIDTH // SNAKE_BLOCK)//2) * SNAKE_BLOCK
    y1 = ((SCREEN_HEIGHT // SNAKE_BLOCK)//2) * SNAKE_BLOCK
    x1_change = 0
    y1_change = 0

    # Snake body and length
    snake_List = []
    Length_of_snake = 1

    # Food position
    foodx = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
    foody = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
    food_is_drawn = True

    # Clock to control game speed
    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            screen.fill(BLUE)
            save_score(user_id, level, score)
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
                    if len(snake_List) > 1:
                        if x1-SNAKE_BLOCK == snake_List[-2][0]:
                            break
                    
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    if len(snake_List) > 1:
                        if x1+SNAKE_BLOCK == snake_List[-2][0]:
                            break

                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    if len(snake_List) > 1:
                        if y1-SNAKE_BLOCK == snake_List[-2][1]:
                            break

                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    if len(snake_List) > 1:
                        if y1+SNAKE_BLOCK == snake_List[-2][1]:
                            break
                    
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

                # Implement pause with 'P' key
                elif event.key == pygame.K_p:
                    save_score(user_id, level, score)
                    print("Game saved! Press Q to quit.")
                    pygame.display.update()
                    game_over = True

        # Check for border collision
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLUE)

        if i > 50 and not food_is_drawn:
            foodx = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
            foody = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
            food_is_drawn = True
            i = 0
        
        if i > 150 and food_is_drawn:
            food_is_drawn = False
            i = 0

        if food_is_drawn:
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
        message("Score: " + str(score), GREEN, 20, 20)
        message("Level: " + str(level), GREEN, SCREEN_WIDTH - 200, 20)

        pygame.display.update()

        # Check if snake eats food
        if abs(x1 - foodx) < SNAKE_BLOCK//2 and abs(y1 - foody) < SNAKE_BLOCK//2:
            food_is_drawn = False
            i = 0
            Length_of_snake += 1
            score += 10

            if score % 30 == 0:  # Level up after 30 points
                level += 1
                speed += 5

        # Control the speed of the game
        clock.tick(speed)
        i+=1

    pygame.quit()
    quit()

gameLoop()
