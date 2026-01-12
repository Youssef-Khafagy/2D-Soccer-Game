import sys
import math
import pygame

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Soccer Game")

# Set up colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up the ball
ball_radius = 10
ball_x = width // 2
ball_y = height // 2
ball_speed_x = 0
ball_speed_y = 0
ball_acceleration = 0.2
max_ball_speed = 6

# Set up the players
player_size = 40
player1_x = (width - player_size) // 4
player1_y = (height - player_size) // 2
player2_x = (3 * width - player_size) // 4
player2_y = (height - player_size) // 2
player_speed = 3
player_acceleration = 0.1

# Set up the nets
net_width = 15
net_height = 100
net1_x = 10
net2_x = width - 10 - net_width
net_y = (height - net_height) // 2

# Set up the scores
score1 = 0
score2 = 0
score_font = pygame.font.Font(None, 36)

# Set up the timer
timer_font = pygame.font.Font(None, 36)
timer_duration = 1 * 60  # 3 minutes in seconds
timer_start_ticks = pygame.time.get_ticks()

# Set up game over screen
game_over_font = pygame.font.Font(None, 72)

# Load images
bg = pygame.image.load("field.png").convert_alpha()
bg = pygame.transform.scale(bg, (width, height))
player1_img = pygame.image.load("player1.png").convert_alpha()
player1_img = pygame.transform.scale(player1_img, (player_size, player_size))
player2_img = pygame.image.load("player2.png").convert_alpha()
player2_img = pygame.transform.scale(player2_img, (player_size, player_size))

clock = pygame.time.Clock()

# Game states
MENU = 0
INSTRUCTIONS = 1
GAME = 2
GAME_OVER = 3
current_state = MENU

def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = width // 2
    ball_y = height // 2
    ball_speed_x = 0
    ball_speed_y = 0

def reset_players():
    global player1_x, player1_y, player2_x, player2_y
    player1_x = (width - player_size) // 4
    player1_y = (height - player_size) // 2
    player2_x = (3 * width - player_size) // 4
    player2_y = (height - player_size) // 2

def draw_elements():
    screen.blit(bg, (0, 0))
    # Draw the ball
    pygame.draw.circle(screen, GREEN, (int(ball_x), int(ball_y)), ball_radius)

    # Draw the players
    screen.blit(player1_img, (player1_x, player1_y))
    screen.blit(player2_img, (player2_x, player2_y))

    # Draw the nets
    pygame.draw.rect(screen, BLUE, (net1_x, net_y, net_width, net_height))
    pygame.draw.rect(screen, RED, (net2_x, net_y, net_width, net_height))  # Right goal is red

    # Draw the scores
    score_text = f"Player 1: {score1}     Player 2: {score2}"
    score_render = score_font.render(score_text, True, BLACK)
    screen.blit(score_render, (10, 10))

    # Draw the timer
    time_left = max(0, timer_duration - (pygame.time.get_ticks() - timer_start_ticks) // 1000)
    minutes = time_left // 60
    seconds = time_left % 60
    timer_text = f"Time: {minutes:02d}:{seconds:02d}"
    timer_render = timer_font.render(timer_text, True, BLACK)
    screen.blit(timer_render, (width // 2 - 50, 10))

def check_goal():
    global ball_speed_x, score1, score2
    if ball_x < net1_x + net_width and (net_y < ball_y < net_y + net_height):
        ball_speed_x *= -1
        reset_ball()
        score1 += 1
        reset_players()
    elif ball_x > net2_x and (net_y < ball_y < net_y + net_height):
        ball_speed_x *= -1
        reset_ball()
        score2 += 1
        reset_players()

def update_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y

    # Update ball position based on velocity
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Apply acceleration to the ball's velocity
    ball_speed_x *= 0.96  # Slow down the ball horizontally
    ball_speed_y *= 0.96  # Slow down the ball vertically

    # Limit the ball's speed
    ball_speed_x = max(-max_ball_speed, min(max_ball_speed, ball_speed_x))
    ball_speed_y = max(-max_ball_speed, min(max_ball_speed, ball_speed_y))

    # Check ball collisions with walls
    if ball_x < ball_radius:
        ball_x = ball_radius
        ball_speed_x *= -1
    elif ball_x > width - ball_radius:
        ball_x = width - ball_radius
        ball_speed_x *= -1

    # Check ball collision with players
    if (player1_x < ball_x < player1_x + player_size) and (player1_y < ball_y < player1_y + player_size):
        angle = math.atan2(ball_y - (player1_y + player_size // 2), ball_x - (player1_x + player_size // 2))
        ball_speed_x = math.cos(angle) * max_ball_speed
        ball_speed_y = math.sin(angle) * max_ball_speed
    if (player2_x < ball_x < player2_x + player_size) and (player2_y < ball_y < player2_y + player_size):
        angle = math.atan2(ball_y - (player2_y + player_size // 2), ball_x - (player2_x + player_size // 2))
        ball_speed_x = math.cos(angle) * max_ball_speed
        ball_speed_y = math.sin(angle) * max_ball_speed

    # Check ball screen boundaries
    if ball_y < ball_radius + 75 or ball_y > height - 75:
        reset_ball()

    # Check for goals
    check_goal()

def update_players():
    global player1_x, player1_y, player2_x, player2_y

    keys = pygame.key.get_pressed()

    # Update player 1 position
    if keys[pygame.K_a]:
        player1_x -= player_speed
    if keys[pygame.K_d]:
        player1_x += player_speed
    if keys[pygame.K_w]:
        player1_y -= player_speed
    if keys[pygame.K_s]:
        player1_y += player_speed

    # Update player 2 position
    if keys[pygame.K_LEFT]:
        player2_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player2_x += player_speed
    if keys[pygame.K_UP]:
        player2_y -= player_speed
    if keys[pygame.K_DOWN]:
        player2_y += player_speed

    # Limit player positions within the screen

    if player1_x < 0:
        player1_x = 0
    if player1_x > 970:
        player1_x = 970
    if player1_y < 0:
        player1_y = 0
    if player1_y > 750:
        player1_y = 750

    if player2_x < 0:
        player2_x = 0
    if player2_x > 970:
        player2_x = 970
    if player2_y < 0:
        player2_y = 0
    if player2_y > 750:
        player2_y = 750


def game_loop():
    menu_loop = True

    while menu_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_menu()

        pygame.display.flip()
        clock.tick(60)

def draw_menu():
    title_font = pygame.font.Font(None, 72)
    menu_font = pygame.font.Font(None, 36)

    title_text = title_font.render("2D Soccer Game", True, BLACK)
    start_text = menu_font.render("Start Game", True, BLACK)
    instructions_text = menu_font.render("View Instructions", True, BLACK)
    exit_text = menu_font.render("Exit", True, BLACK)

    title_rect = title_text.get_rect(center=(width // 2, height // 4))
    start_rect = start_text.get_rect(center=(width // 2, height // 2))
    instructions_rect = instructions_text.get_rect(center=(width // 2, height // 2 + 50))
    exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 100))

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(instructions_text, instructions_rect)
    screen.blit(exit_text, exit_rect)

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if start_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
        game_start()

    if instructions_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
        show_instructions()

    if exit_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
        pygame.quit()
        sys.exit()

def show_instructions():
    instructions_screen = True

    while instructions_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        instructions_font = pygame.font.Font(None, 36)
        back_font = pygame.font.Font(None, 24)

        instructions_text = instructions_font.render("Instructions:", True, BLACK)
        instruction1_text = instructions_font.render("- Player 1:", True, BLACK)
        instruction2_text = instructions_font.render("  Move: A, D, W, S", True, BLACK)
        instruction3_text = instructions_font.render("- Player 2:", True, BLACK)
        instruction4_text = instructions_font.render("  Move: Arrow Keys", True, BLACK)
        back_text = back_font.render("Back to Menu", True, BLACK)

        instructions_rect = instructions_text.get_rect(center=(width // 2, height // 4))
        instruction1_rect = instruction1_text.get_rect(center=(width // 2, height // 4 + 50))
        instruction2_rect = instruction2_text.get_rect(center=(width // 2, height // 4 + 100))
        instruction3_rect = instruction3_text.get_rect(center=(width // 2, height // 4 + 150))
        instruction4_rect = instruction4_text.get_rect(center=(width // 2, height // 4 + 200))
        back_rect = back_text.get_rect(center=(width // 2, height - 50))

        screen.blit(instructions_text, instructions_rect)
        screen.blit(instruction1_text, instruction1_rect)
        screen.blit(instruction2_text, instruction2_rect)
        screen.blit(instruction3_text, instruction3_rect)
        screen.blit(instruction4_text, instruction4_rect)
        screen.blit(back_text, back_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if back_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
            menu_loop = True
            instructions_screen = False

        pygame.display.flip()
        clock.tick(60)

def game_start():
    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_elements()
        update_players()
        update_ball()

        pygame.display.flip()
        clock.tick(60)

# Start the game
game_loop()
