import pygame
from sys import exit
from random import randint

pygame.init()
pygame.mouse.set_visible(False)  # Hide the PC cursor
screen = pygame.display.set_mode((1366, 768))
pygame.display.set_caption("Rescue Turtles, Elevate Minds")
game_font = pygame.font.Font("font/SuperFoods-2OxXo.ttf", 28)
start_font = pygame.font.Font("font/SuperFoods-2OxXo.ttf", 65)
clock = pygame.time.Clock()
game_active = False  # Set the game state to inactive initially
darkgrey = pygame.Color("#505050")
lightgrey = pygame.Color("#b7c3d0")
babyblue = pygame.Color("#74a3d6")

score = 0
score_x, score_y = 1200, 30  # Coordinates for the score display
score_bg_color = lightgrey  # Background color for the score display
score_border_color = darkgrey  # Border color for the score display
score_padding = 10  # Padding around the score text
score_surface = None

sky_surface = pygame.image.load('graphics/sky.png').convert_alpha()
sea2_surface = pygame.image.load('graphics/sea2.png').convert_alpha()
sea1_surface = pygame.image.load('graphics/sea1.png').convert_alpha()
sea3_surface = pygame.image.load('graphics/sea3.png').convert_alpha()

start_surface = pygame.image.load('graphics/start.jpg').convert_alpha()
start_surface = pygame.transform.scale(start_surface, (1366, 768))

cursor_surface = pygame.image.load('graphics/cursor.png').convert_alpha()
cursor_surface = pygame.transform.scale(cursor_surface, (110, 90))

Turtle1_norm_surface = pygame.image.load('graphics/Turtle1/Turtle1_norm.png').convert_alpha()
Turtle1_norm_surface = pygame.transform.scale(Turtle1_norm_surface, (200, 200))
Turtle1_norm_rect = Turtle1_norm_surface.get_rect(midbottom=(600, 400))

Turtle1_trash_surface = pygame.image.load('graphics/Turtle1/Turtle1_trash.png').convert_alpha()
Turtle1_trash_surface = pygame.transform.scale(Turtle1_trash_surface, (200, 200))
Turtle1_trash_rect = Turtle1_trash_surface.get_rect(midbottom=(600, 400))

Turtle2_norm_surface = pygame.image.load('graphics/Turtle2/Turtle2_norm.png').convert_alpha()
Turtle2_norm_surface = pygame.transform.scale(Turtle2_norm_surface, (200, 200))
Turtle2_norm_rect = Turtle2_norm_surface.get_rect(midbottom=(600, 400))

Turtle2_trash_surface = pygame.image.load('graphics/Turtle2/Turtle2_trash.png').convert_alpha()
Turtle2_trash_surface = pygame.transform.scale(Turtle1_trash_surface, (200, 200))
Turtle2_trash_rect = Turtle2_trash_surface.get_rect(midbottom=(600, 400))

turtle_spawn_frequency = 80  # Controls how often a new turtle should spawn (smaller values mean faster spawning)
turtle_spawn_timer = 0
turtles = []  # List to hold all active turtles
spawn_line_y = 400


class Turtle:
    def __init__(self):
        self.turtle_type = randint(1, 2)  # Randomly choose the turtle type (1 or 2)
        if self.turtle_type == 1:
            self.is_trash = randint(0, 1)  # Randomly choose whether it's a trash turtle or not
            if self.is_trash:
                self.surface = Turtle1_trash_surface
            else:
                self.surface = Turtle1_norm_surface
        else:
            self.is_trash = randint(0, 1)  # Randomly choose whether it's a trash turtle or not
            if self.is_trash:
                self.surface = Turtle2_trash_surface
            else:
                self.surface = Turtle2_norm_surface

        self.rect = self.surface.get_rect(midbottom=(0, spawn_line_y))
        self.clicked = False  # Flag to track if the turtle has been clicked in the current frame



def update_score():
    global score_surface
    score_text = game_font.render(f"Score: {score}", True, score_border_color)
    score_bg_rect = score_text.get_rect(topleft=(score_x - score_padding, score_y - score_padding))
    score_bg_surface = pygame.Surface(
        (score_bg_rect.width + 2 * score_padding, score_bg_rect.height + 2 * score_padding), pygame.SRCALPHA)
    pygame.draw.rect(score_bg_surface, score_bg_color, score_bg_rect, border_radius=10)  # Draw rounded rectangle
    score_bg_surface.blit(score_text, (score_padding, score_padding))
    score_surface = score_bg_surface


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_active:  # Check for mouse click only when the game is inactive
            game_active = True  # Set the game state to active when the player clicks to play
            score = 0  # Reset the score

    if not game_active:  # Display the start screen when the game is inactive
        screen.blit(start_surface, (0,0))
        # Display the "Click to Play" text
        start_text = start_font.render("Click to Play", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(start_text, start_text_rect)

        pygame.display.update()
        continue

    screen.blit(sky_surface, (0, 0))
    screen.blit(sea2_surface, (0, 170))

    # Move and blit all active turtles
    for turtle in turtles:
        turtle.rect.x += 4
        screen.blit(turtle.surface, turtle.rect)

        if turtle.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
                if turtle.is_trash:
                    score += 1
                    turtles.remove(turtle)  # Remove the turtle from the list if it's a trash turtle
                else:
                    if not turtle.clicked:  # Check if the turtle has already been clicked in the current frame
                        score -= 1  # Subtract points if a normal turtle is clicked
                        turtle.clicked = True  # Set the clicked flag to True
        else:
            turtle.clicked = False  # Reset the clicked flag if the mouse is not over the turtle

    # Spawn new turtles at regular intervals
    turtle_spawn_timer += 1
    if turtle_spawn_timer >= turtle_spawn_frequency:
        new_turtle = Turtle()
        if turtles:  # Ensure there is at least one turtle before copying its y-coordinate
            new_turtle.rect.y = turtles[-1].rect.y
        turtles.append(new_turtle)
        turtle_spawn_timer = 0

    screen.blit(sea3_surface, (0, 300))
    screen.blit(sea1_surface, (0, 410))

    # Update the score and blit it on the screen
    update_score()
    screen.blit(score_surface, (score_x, score_y))

    # Update the position of the cursor to follow the mouse
    cursor_pos = pygame.mouse.get_pos()
    cursor_rect = cursor_surface.get_rect(center=cursor_pos)
    screen.blit(cursor_surface, cursor_rect)

    pygame.display.update()
    clock.tick(60)