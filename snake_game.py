import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Window setup
width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption(" Snake Game ")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 200, 0)
YELLOW = (255, 215, 0)
BLUE = (50, 150, 255)
BG_COLOR = (30, 30, 40)
BUTTON_COLOR = (80, 80, 100)
HOVER_COLOR = (100, 100, 150)
HEAD_COLOR = (0, 255, 100)
BODY_COLOR = (255, 255, 0)
FOOD_COLOR = (255, 50, 50)

# Fonts (modern and readable)
TITLE_FONT = pygame.font.SysFont("segoeui", 40, bold=True)
BUTTON_FONT = pygame.font.SysFont("segoeui", 28)
SCORE_FONT = pygame.font.SysFont("segoeui", 22)

# Snake settings
snake_block = 20
clock = pygame.time.Clock()

# Button class
class Button:
    def __init__(self, text, x, y, width, height, action, color=BUTTON_COLOR, hover=HOVER_COLOR):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover = hover
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover, self.rect, border_radius=10)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        text = BUTTON_FONT.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.action

# Draw snake
def draw_snake(snake_list):
    for i, segment in enumerate(snake_list):
        color = HEAD_COLOR if i == len(snake_list)-1 else BODY_COLOR
        pygame.draw.rect(window, color, [segment[0], segment[1], snake_block, snake_block])

def draw_score(score):
    text = SCORE_FONT.render(f"Score: {score}", True, WHITE)
    window.blit(text, [10, 10])

def message_center(text, size, y_offset):
    font = pygame.font.SysFont("segoeui", size, bold=True)
    surface = font.render(text, True, YELLOW)
    rect = surface.get_rect(center=(width // 2, height // 2 + y_offset))
    window.blit(surface, rect)

# Difficulty selection screen
def difficulty_menu():
    beginner_btn = Button("Beginner", 200, 150, 200, 50, action=10)
    inter_btn = Button("Intermediate", 200, 220, 200, 50, action=15)
    adv_btn = Button("Advanced", 200, 290, 200, 50, action=25)
    buttons = [beginner_btn, inter_btn, adv_btn]

    while True:
        window.fill(BG_COLOR)
        title = TITLE_FONT.render("SELECT DIFFICULTY LEVEL", True, BLUE)
        window.blit(title, title.get_rect(center=(width // 2, 80)))

        for button in buttons:
            button.draw(window)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            for button in buttons:
                result = button.check_click(event)
                if result:
                    return result

# Game logic
def game_loop(snake_speed):
    game_over = False
    game_close = False

    x = width // 2
    y = height // 2
    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    foodx = random.randrange(0, width - snake_block, snake_block)
    foody = random.randrange(0, height - snake_block, snake_block)

    while not game_over:
        while game_close:
            window.fill(BG_COLOR)
            message_center(" Game Over!", 40, -40)
            message_center("Press C to Continue or Q to Quit", 22, 20)
            draw_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -snake_block; y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = snake_block; y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -snake_block; x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = snake_block; x_change = 0

        x += x_change
        y += y_change

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        window.fill(BG_COLOR)
        pygame.draw.rect(window, FOOD_COLOR, [foodx, foody, snake_block, snake_block])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_list)
        draw_score(snake_length - 1)
        pygame.display.update()

        if x == foodx and y == foody:
            foodx = random.randrange(0, width - snake_block, snake_block)
            foody = random.randrange(0, height - snake_block, snake_block)
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

# Main function
def main():
    speed = difficulty_menu()
    game_loop(speed)

main()
