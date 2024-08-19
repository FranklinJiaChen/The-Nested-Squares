import pygame
from player import Player
pygame.init()

screen_width = 1440
screen_height = 810
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Nesting Squares Puzzle Platformer')

#Colours are cool!
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (127, 127, 127)
PURPLE = (127, 0, 127)
LIGHT_GREEN = (150, 255, 150)
LIGHTER_GREEN = (200, 255, 200)
GOLD = (255, 215, 0)

# fonts are less cool
font = pygame.font.SysFont('freesansbold.ttf', 30)
smallerfont = pygame.font.SysFont('freesansbold.ttf', 27)

def text(text, x, y, size, colour = BLACK):
    font = pygame.font.SysFont('freesansbold.ttf', size)
    screen.blit(font.render(text, False, colour), (x, y))

# Variables
X_SPEED = 10

JUMP_HEIGHT = 100

# big frame jumps
# when jumping go left to right. When falling go right to left
# (subtracting adjacent values to get frame difference)
JUMP_FRAMES = [38, 72, 102, 128, 150, 168, 182, 192, 198, 200]


def initialize_variables():
    global push_blocks
    global old_block
    global obstacles
    global first_space
    global outside_parent
    push_blocks = []
    old_block = []
    obstacles = []
    first_space = True
    outside_parent = True

# level 1 variables
def level_1_setup():
    global x
    global y
    global obstacles
    global goal_zones
    global player
    player = Player(50, screen_height-40-80, 80, PURPLE)
    obstacles = [
        pygame.Rect(0, screen_height-40, screen_width, 40), # floor
        pygame.Rect(0, 0, 20, screen_height), # left wall
        pygame.Rect(screen_width-20, 0, 20, screen_height) # right wall
    ]

    goal_zones = [
        pygame.Rect(20, screen_height-40-100, 100, 100), # leftmost
        pygame.Rect((20 + screen_width-20-100)/2 - 50, screen_height-40-100, 100, 100), # middle
        pygame.Rect(screen_width-20-100, screen_height-40-100, 100, 100) # rightmost
    ]

initialize_variables()
level_1_setup()

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
    if player.jumping:
        if player.cur_frame == 0:
            cur_jump_size = JUMP_FRAMES[0]
        else:
            cur_jump_size = JUMP_FRAMES[player.cur_frame] - JUMP_FRAMES[player.cur_frame-1]
        player.y -= cur_jump_size

        if player.cur_frame >= len(JUMP_FRAMES)-1:
            player.falling = True
            player.jumping = False
        else:
            player.cur_frame += 1

    if player.falling:
        if player.cur_frame == 0:
            cur_jump_size = JUMP_FRAMES[0]
        else:
            cur_jump_size = JUMP_FRAMES[player.cur_frame] - JUMP_FRAMES[player.cur_frame-1]

        if player.cur_frame > 0:
            player.cur_frame -= 1

        y_prev_bottom = player.y + player.size
        player.y += cur_jump_size
        for obstacle in push_blocks + obstacles:
            if obstacle.colliderect(player.get_area()) and y_prev_bottom <= obstacle[1]:
                player.y = obstacle[1]-player.size
                player.falling = False
                player.cur_frame = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x_prev_left = player.x
        player.x -= X_SPEED
        for obstacle in obstacles:
            if obstacle.colliderect(player.get_area()) and x_prev_left >= obstacle[0] + obstacle[2]:
                player.x = obstacle[0] + obstacle[2]
        for push_block in push_blocks:
            if push_block.colliderect(player.get_area()) and x_prev_left >= push_block[0] + push_block[2]:
                push_block_prev_left = push_block[0]
                push_block[0] -= X_SPEED
                for obstacle in obstacles:
                    if obstacle.colliderect(push_block) and push_block_prev_left >= obstacle[0] + obstacle[2]:
                        push_block[0] = obstacle[0] + obstacle[2]
                        player.x = obstacle[0] - obstacle[0] + obstacle[2] + push_block[3]
            for push_block2 in push_blocks:
                if push_block.colliderect(push_block2) and push_block2 != push_block: # does not check prev left
                    push_block2[0] -= X_SPEED
                    for obstacle in obstacles:
                        if obstacle.colliderect(push_block2): # does not check prev left
                            push_block2[0] = obstacle[0] + obstacle[2]
                            push_block[0] = obstacle[0] + obstacle[2] + push_block2[3]
                            player.x = obstacle[0] - obstacle[0] + obstacle[2] + push_block2[3] + push_block[3]
    if keys[pygame.K_RIGHT]:
        x_prev_right = player.x + player.size
        player.x += X_SPEED
        for obstacle in  obstacles:
            if obstacle.colliderect(player.get_area()) and x_prev_right <= obstacle[0]:
                player.x = obstacle[0] - player.size
        for push_block in push_blocks:
            if push_block.colliderect(player.get_area()) and x_prev_right <= obstacle[0]:
                push_block_prev_right = push_block[0] + push_block[2]
                push_block[0] += X_SPEED
                for obstacle in obstacles:
                    if obstacle.colliderect(push_block) and push_block_prev_right <= obstacle[0]:
                        push_block[0] = obstacle[0] - push_block[3]
                        player.x = obstacle[0] - push_block[3] - player.size
            for push_block2 in push_blocks:
                if push_block.colliderect(push_block2) and push_block2 != push_block: # does not check prev right
                    push_block2[0] += X_SPEED
                    for obstacle in obstacles:
                        if obstacle.colliderect(push_block2): # does not check prev right
                            push_block2[0] = obstacle[0] - push_block2[3]
                            push_block[0] = obstacle[0] - push_block2[3] - push_block[3]
                            player.x = obstacle[0] - push_block2[3] - push_block[3] - player.size


    if keys[pygame.K_UP] and player.cur_frame == 0 and not player.falling:
        player.jumping = True
    if keys[pygame.K_SPACE] and first_space and outside_parent:
        if player.size == 80:
            old_block = pygame.Rect(player.x, player.y, 80, 80)
            player.x += 20
            player.y += 40
            player.size //= 2
            JUMP_FRAMES = [x//2 for x in JUMP_FRAMES]
            cur_colour = BLUE
            outside_parent = False
        elif player.size == 40:
            old_block = pygame.Rect(player.x, player.y, 40, 40)
            player.x += 10
            player.y += 20
            player.size //= 2
            JUMP_FRAMES = [x//2 for x in JUMP_FRAMES]
            cur_colour = RED
            outside_parent = False
        first_space = False
    elif not keys[pygame.K_SPACE]:
        first_space = True

    if keys[pygame.K_r]: # restart
        initialize_variables()
        level_1_setup()

    screen.fill(WHITE)
    win = True

    for goal_zone in goal_zones:
        if player.get_area().colliderect(goal_zone) or \
            any([push_block.colliderect(goal_zone) for push_block in push_blocks]) or \
            old_block and old_block.colliderect(goal_zone):
            pygame.draw.rect(screen, LIGHT_GREEN, goal_zone)
        else:
            pygame.draw.rect(screen, LIGHTER_GREEN, goal_zone)
            win = False

    if win:
        text('CONGRATULATIONS!', 410, 100, 80, GOLD)
        text('You Win! Thank you for Playing!', 240, 200, 80, GOLD)


    for obstacle in obstacles:
        pygame.draw.rect(screen, GREY, obstacle)
    for push_block in push_blocks:
        pygame.draw.rect(screen, BLACK, push_block)
    if old_block:
        pygame.draw.rect(screen, BLACK, old_block)

    if old_block:
        if not pygame.Rect(old_block).colliderect(player.get_area()):
            outside_parent = True
            push_blocks.append(old_block)
            old_block = []

    # if player feet not on ground
    if not player.jumping and not player.falling and not any([obstacle.colliderect(player.get_feet_area()) for obstacle in push_blocks + obstacles]):
        player.falling = True
        player.cur_frame = len(JUMP_FRAMES) - 1

    pygame.draw.rect(screen, player.colour, player.get_area())

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
# Close the window and quit.
pygame.quit()
