import pygame
pygame.init()

FACTOR = 90
screen = pygame.display.set_mode((16*FACTOR, 9*FACTOR))
pygame.display.set_caption('Penguin')

#Colours are cool!
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (127, 127, 127)
PURPLE = (127, 0, 127)

# Variables
X_SPEED = 10

JUMP_HEIGHT = 100
cur_jump = 0
cur_frame = 0

# big frame jumps
# jump_frames = [53, 98, 135, 163, 184, 196, 200]
jump_frames = [38, 72, 102, 128, 150, 168, 182, 192, 198, 200]

x = 50
y = 350
jumping = False
falling = False
cur_size = 80
cur_colour = PURPLE

first_space = True

font = pygame.font.SysFont('freesansbold.ttf', 30)
smallerfont = pygame.font.SysFont('freesansbold.ttf', 27)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
#     --- Drawing code should go here
    if jumping:
        if cur_frame == 0:
            cur_jump_size = jump_frames[0]
        else:
            cur_jump_size = jump_frames[cur_frame] - jump_frames[cur_frame-1]
        y -= cur_jump_size

        if cur_frame >= len(jump_frames)-1:
            falling = True
            jumping = False
        else:
            cur_frame += 1

    if falling:
        if cur_frame == 0:
            cur_jump_size = jump_frames[0]
        else:
            cur_jump_size = jump_frames[cur_frame] - jump_frames[cur_frame-1]

        y += cur_jump_size

        if cur_frame <= 0:
            falling = False
        else:
            cur_frame -= 1

    screen.fill(WHITE)
    pygame.draw.rect(screen, PURPLE, [50, 350-90, 4*10, 4*10])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= X_SPEED
    if keys[pygame.K_RIGHT]:
        x += X_SPEED
    if keys[pygame.K_UP] and cur_frame == 0 and not falling:
        jumping = True
    if keys[pygame.K_SPACE] and first_space:
        if cur_size == 80:
            x += 20
            y += 40
            cur_size //= 2
            jump_frames = [x//2 for x in jump_frames]
            cur_colour = BLUE
        elif cur_size == 40:
            x += 10
            y += 20
            cur_size //= 2
            jump_frames = [x//2 for x in jump_frames]
            cur_colour = RED
        first_space = False
    elif not keys[pygame.K_SPACE]:
        first_space = True

    pygame.draw.rect(screen, GREY, [1000, 350, 80, 80])
    pygame.draw.rect(screen, GREY, [50, 350, 80, 80])
    pygame.draw.rect(screen, GREY, [600, 330, 100, 100])
    pygame.draw.rect(screen, GREY, [0, 330+80, 1500, 100])
    pygame.draw.rect(screen, GREY, [400, 200, 100, 100])
    player_hitbox =  pygame.Rect(x, y, cur_size, cur_size)

    if pygame.Rect(1000, 350, 80, 80).colliderect(player_hitbox):
        x = 1000-cur_size
    if pygame.Rect(50, 350, 80, 80).colliderect(player_hitbox):
        x = 50+80
    if pygame.Rect(600, 330, 100, 100).colliderect(player_hitbox):
        y = 330-cur_size
    if pygame.Rect(0, 330+80, 1500, 100).colliderect(player_hitbox):
        y = 330+80-cur_size
    if pygame.Rect(400, 200, 100, 100).colliderect(player_hitbox):
        y = 200+100
        falling = True
        jumping = False

    pygame.draw.rect(screen, cur_colour, [x, y, cur_size, cur_size])


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
# Close the window and quit.
pygame.quit()
