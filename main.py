import pygame 
import os

# for displaying health we need text
pygame.font.init()

# for sound effect
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACESHIP")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

FPS = 60
VELOCITY = 5  #
BULLET_VEL = 7

MAX_BULLETS = 3

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

# to indicate health
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Loading spaceship images into our file known as surfaces as we use this above background
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
SPACE = pygame.image.load(os.path.join("Assets", "space.png"))

# SCALING down the images
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (50, 40)
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
SPACE = pygame.transform.scale(SPACE, (900,500))

# ROTATING the images
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90)
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, -90)

# BORDER in the middle of the window
# starting coordinates then width and height of the border
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10,HEIGHT)

# Creating user event so that we can came to know if the bullet collides, diff number indicates diff events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT +  2

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # ORDER IN WHICH DRAW THINGS MATTER REMEMBER
    WIN.blit(SPACE, (0,0))

    # Adding border created above 
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Displaying Health by font
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # to load surfaces we use blit
    # WIN.blit(YELLOW_SPACESHIP, (300,100))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    
    # WIN.blit(RED_SPACESHIP, (600,300))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
  

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    # and checking that it remains in the screen and dont cross the border
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:   # LEFT
        yellow.x -= VELOCITY
    elif keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x:   # RIGHT
        yellow.x += VELOCITY
    elif keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:   # UP
        yellow.y -= VELOCITY
    elif keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT-15:   # DOWN
        yellow.y += VELOCITY


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width + 8 :   # LEFT
        red.x -= VELOCITY
    elif keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:   # RIGHT
        red.x += VELOCITY
    elif keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:   # UP
        red.y -= VELOCITY
    elif keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT-15:   # DOWN
        red.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # To check wether the bullet hit red or yellow spaceship or they fly through the skin
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL

        # colliddirect only works if both are rectangle
        if red.colliderect(bullet):
            # Now we are going to post a event then check in the main function for the event
            # it will indicate us that the bullet hit the spaceship
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL

        # colliddirect only works if both are rectangle
        if yellow.colliderect(bullet):
            # Now we are going to post a event then check in the main function for the event
            # it will indicate us that the bullet hit the spaceship
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
        
def winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

        
def main():
    # Making two rectangles so that we can control where our spaceship are moving
    red = pygame.Rect(700,250, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,250, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    # To making our game refresh at a constant interval
    clock = pygame.time.Clock()
    
    yellow_bullets = []
    red_bullets = []

    red_health = 10
    yellow_health = 10

    run = True
    
    while run:
        # Capped frame rate so it remains consistent on diff computers
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # checking if key pressed for firing bullet 
            if event.type == pygame.KEYDOWN:

                # CHECKING if we press LCTRL and we have 3 bullets at a time on a screen
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # 10, 5 width, height of bullet and others are location
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()      
        
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!!"
        if yellow_health <= 0:
            winner_text = "Red Wins!!"
        if winner_text!="":
            winner(winner_text)
            break    

        # Checking which keys are pressed while the game is running it also checks if the keys are pressed and remain down
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # print(yellow_bullets, red_bullets)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)        

    main()

if __name__ == "__main__":
    main()

            
