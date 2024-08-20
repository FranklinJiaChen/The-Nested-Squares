import pygame
from player import Player
from push_block import PushBlock
from random import randint

pygame.init()

screen_width = 1440
screen_height = 810
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Nesting Squares Puzzle Platformer')

#Colours are cool!
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_RED = (139, 0, 0)
RED = (255, 0, 0)
DARK_BLUE = (0, 0, 139)
BLUE = (0, 0, 255)
GREY = (127, 127, 127)
DARK_GREY = (169, 169, 169)
DARK_GREY = (169, 169, 169)
WALL_BROWN = (139, 69, 19)
PURPLE = (127, 0, 127)
MAGENTA = (255, 0, 255)
LIGHT_GREEN = (150, 255, 150)
LIGHTER_GREEN = (200, 255, 200)
GOLD = (255, 215, 0)

LAST_LEVEL = 6

# fonts are less cool
font = pygame.font.SysFont('freesansbold.ttf', 30)
smallerfont = pygame.font.SysFont('freesansbold.ttf', 27)

def text(text, x, y, size, colour = BLACK):
    font = pygame.font.SysFont('freesansbold.ttf', size)
    screen.blit(font.render(text, False, colour), (x, y))

# Variables
X_SPEED = 6

JUMP_HEIGHT = 100


cur_level = 7

def initialize_variables():
    global push_blocks
    global old_block
    global obstacles
    global first_space
    global outside_parent
    global jump_frames
    global win
    # big frame jumps
    # when jumping go left to right. When falling go right to left
    # (subtracting adjacent values to get frame difference)
    # shift by leftmost number when you get smaller
    jump_frames = [38, 72, 102, 128, 150, 168, 182, 192, 198, 200]
    push_blocks = []
    old_block = None
    obstacles = []
    first_space = True
    outside_parent = True
    win = False

def level_1_setup():
    """
    Basic 3 goals
    """
    global obstacles
    global goal_zones
    global player
    player = Player(50, screen_height-40-96, 96, RED)
    obstacles = [
        pygame.Rect(0, screen_height-40, screen_width, 40), # floor
        pygame.Rect(0, 0, 20, screen_height), # left border
        pygame.Rect(screen_width-20, 0, 20, screen_height) # left border
    ]

    goal_zones = [
        pygame.Rect(20, screen_height-40-100, 100, 100), # leftmost
        pygame.Rect((20 + screen_width-20-100)/2, screen_height-40-100, 100, 100), # middle
        pygame.Rect(screen_width-20-100, screen_height-40-100, 100, 100) # rightmost
    ]

def level_2_setup():
    """
    4 goals. 2 close on the right
    """
    global obstacles
    global goal_zones
    global player
    player = Player(50, screen_height-40-96, 96, RED)
    obstacles = [
        pygame.Rect(0, screen_height-40, screen_width, 40), # floor
        pygame.Rect(0, 0, 20, screen_height), # left border
        pygame.Rect(screen_width-20, 0, 20, screen_height) # left border
    ]

    goal_zones = [
        pygame.Rect(20, screen_height-40-100, 100, 100), # leftmost
        pygame.Rect(20+100+120, screen_height-40-100, 100, 100), # 2nd leftmost
        pygame.Rect(screen_width-20-100-100-84, screen_height-40-100, 100, 100), # 2nd rightmost
        pygame.Rect(screen_width-20-100, screen_height-40-100, 100, 100) # rightmost
    ]

def level_3_setup():
    """
    Jump?
    """
    global obstacles
    global goal_zones
    global player
    player = Player(50, screen_height-40-96, 96, RED)
    obstacles = [
        pygame.Rect(0, screen_height-40, screen_width//2 - 80, 40), # left floor
        pygame.Rect(screen_width//2 + 80, screen_height-240, screen_width//2 - 40, 240), # right floor
        pygame.Rect(0, 0, 20, screen_height), # left border
        pygame.Rect(screen_width-20, 0, 20, screen_height) # left border
    ]

    goal_zones = [
        pygame.Rect(20, screen_height-40-100, 100, 100), # leftmost
        pygame.Rect(screen_width-20-100, screen_height-240-100, 100, 100) # rightmost
    ]


def level_4_setup():
    global obstacles
    global goal_zones
    global player
    player = Player(50, screen_height-40-96, 96, RED)
    obstacles = [
        pygame.Rect(0, screen_height-40, screen_width, 40), # floor
        pygame.Rect(0, 0, 20, screen_height), # left border
        pygame.Rect(screen_width-20, 0, 20, screen_height), # left border
        pygame.Rect(0, 0, screen_width, 40), # ceiling
        pygame.Rect(screen_width-20-1000, screen_height-40-72-15, 1200, 20), # first level bottom
        pygame.Rect(screen_width-20-1200, screen_height-40-72-15-72-15, 1200, 20), # first level top
        pygame.Rect(screen_width-20-1000, screen_height-214-200+38+17, 1200, 20), # second level
        pygame.Rect(screen_width-20-800, screen_height-359-84-20, 1200, 20), # second level top
        pygame.Rect(0, screen_height-359-200+19, 400, 20), # left level
        pygame.Rect(screen_width-20-900, screen_height-540-100+19, 1200, 20) # topmost level
    ]

    goal_zones = [
        pygame.Rect(screen_width-20-100, screen_height-40-72-15-72-15, 100, 100), # bottom
        pygame.Rect(screen_width-20-100, screen_height-359-84-20+10, 100, 100), # middle
        pygame.Rect(screen_width-20-100, screen_height-540-100+19-100, 100, 100)
    ]

def level_5_setup():
    global obstacles
    global goal_zones
    global player
    player = Player(50, 600-96, 96, RED)
    obstacles = [
        pygame.Rect(0, screen_height-40, screen_width, 40), # floor
        pygame.Rect(0, 0, 20, screen_height), # left border
        pygame.Rect(screen_width-20, 0, 20, screen_height), # left border
        pygame.Rect(20, 600, 400, screen_height), # left area
        pygame.Rect(screen_width-20-400, 600-70, 400, screen_height) # right area
    ]

    goal_zones = [
        pygame.Rect(20, 600-100, 100, 100), # leftside
        pygame.Rect(screen_width-20-100, 600-70-100, 100, 100) # rightside
    ]

def level_6_setup():
    "weird quadruple"
    global obstacles
    global goal_zones
    global player
    player = Player(50, screen_height-40-96, 96, RED)
    obstacles = [
        pygame.Rect(0, screen_height-40, screen_width, 40),
        pygame.Rect(0, 0, 20, screen_height), # left border
        pygame.Rect(screen_width-20, 0, 20, screen_height) # left border
    ]

    goal_zones = [
        pygame.Rect((20 + screen_width-20-100)/2+30+50, screen_height-40-100, 100, 100), # bottom right
        pygame.Rect((20 + screen_width-20-100)/2-30-50, screen_height-40-100, 100, 100), # bottom left
        pygame.Rect((20 + screen_width-20-100)/2+30+50+100, screen_height-40-100-100, 100, 100), # top right
        pygame.Rect((20 + screen_width-20-100)/2-30-50-100, screen_height-40-100-100, 100, 100) # top left
    ]

def level_7_setup():
    """
    jump
    """
    global obstacles
    global goal_zones
    global player
    player = Player(50, screen_height-40-96, 96, RED)
    obstacles = [
        pygame.Rect(0, screen_height-40, screen_width, 40),
        pygame.Rect(0, 0, 20, screen_height), # left border
        pygame.Rect(screen_width-20, 0, 20, screen_height) # left border
    ]

    goal_zones = [
        pygame.Rect((20 + screen_width-20-100)/2, screen_height-470, 100, 100), # jump goal
    ]



def start_level():
    initialize_variables()
    if cur_level == 1: level_1_setup()
    if cur_level == 2: level_2_setup()
    if cur_level == 3: level_3_setup()
    if cur_level == 4: level_4_setup()
    if cur_level == 5: level_5_setup()
    if cur_level == 6: level_6_setup()
    if cur_level == 7: level_7_setup()

start_level()

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
            cur_jump_size = jump_frames[0]
        else:
            cur_jump_size = jump_frames[player.cur_frame] - jump_frames[player.cur_frame-1]


        if player.cur_frame >= len(jump_frames)-1:
            player.falling = True
            player.jumping = False
        else:
            player.cur_frame += 1

        y_prev_top = player.y
        player.y -= cur_jump_size
        for obstacle in [push_block.get_area() for push_block in push_blocks] + obstacles:
            if obstacle.colliderect(player.get_area()) and y_prev_top >= obstacle[1] + obstacle[3]:
                player.y = obstacle[1] + obstacle[3]
                player.falling = True
                player.jumping = False
                player.cur_frame = len(jump_frames)-1

    # calling fall length jump size :p
    if player.falling:
        if player.cur_frame == 0:
            cur_jump_size = jump_frames[0]
        else:
            cur_jump_size = jump_frames[player.cur_frame] - jump_frames[player.cur_frame-1]

        if player.cur_frame > 0:
            player.cur_frame -= 1

        y_prev_bottom = player.y + player.size
        player.y += cur_jump_size
        for obstacle in [push_block.get_area() for push_block in push_blocks] + obstacles:
            if obstacle.colliderect(player.get_area()) and y_prev_bottom <= obstacle[1]:
                player.y = obstacle[1]-player.size
                player.falling = False
                player.cur_frame = 0

    for push_block in [*push_blocks, old_block]:
        if push_block and push_block.falling:
            if push_block.cur_frame == 0:
                cur_jump_size = jump_frames[0]
            else:
                cur_jump_size = jump_frames[push_block.cur_frame] - jump_frames[push_block.cur_frame-1]

            if push_block.cur_frame > 0:
                push_block.cur_frame -= 1

            y_prev_bottom = push_block.y + push_block.size
            push_block.y += cur_jump_size
            for obstacle in [potential_obstacle.get_area() for potential_obstacle in push_blocks if potential_obstacle != push_block] + obstacles:
                if obstacle.colliderect(push_block.get_area()) and y_prev_bottom <= obstacle[1]:
                    push_block.y = obstacle[1]-push_block.size
                    push_block.falling = False
                    push_block.cur_frame = 0


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x_prev_left = player.x
        player.x -= X_SPEED
        for obstacle in obstacles:
            if obstacle.colliderect(player.get_area()) and x_prev_left >= obstacle[0] + obstacle[2]:
                player.x = obstacle[0] + obstacle[2]
        # gross pushing logic that checks if pushable and if it pushes into
        # a wall/another pushable (hard coded)
        for push_block in push_blocks:
            if push_block.get_area().colliderect(player.get_area()) and x_prev_left >= push_block.x + push_block.size:
                push_block_prev_left = push_block.x
                push_block.x = player.x - push_block.size
                for obstacle in obstacles:
                    if obstacle.colliderect(push_block.get_area()) and push_block_prev_left >= obstacle[0] + obstacle[2]:
                        push_block.x = obstacle[0] + obstacle[2]
                        player.x = obstacle[0] - obstacle[0] + obstacle[2] + push_block.size
            for push_block2 in push_blocks:
                if push_block.get_area().colliderect(push_block2.get_area()) and push_block2 != push_block: # does not check prev left
                    push_block2.x -= X_SPEED
                    for obstacle in obstacles:
                        if obstacle.colliderect(push_block2.get_area()): # does not check prev left
                            push_block2.x = obstacle[0] + obstacle[2]
                            push_block.x = obstacle[0] + obstacle[2] + push_block2.size
                            player.x = obstacle[0] - obstacle[0] + obstacle[2] + push_block2.size + push_block.size
    if keys[pygame.K_RIGHT]:
        x_prev_right = player.x + player.size
        player.x += X_SPEED
        for obstacle in  obstacles:
            if obstacle.colliderect(player.get_area()) and x_prev_right <= obstacle[0]:
                player.x = obstacle[0] - player.size
        for push_block in push_blocks:
            if push_block.get_area().colliderect(player.get_area()) and x_prev_right <= push_block.x:  # get rid of right check
                push_block_prev_right = push_block.x + push_block.size
                push_block.x = player.x + player.size
                for obstacle in obstacles:
                    if obstacle.colliderect(push_block.get_area()) and push_block_prev_right <= obstacle[0]:
                        push_block.x = obstacle[0] - push_block.size
                        player.x = obstacle[0] - push_block.size - player.size
            for push_block2 in push_blocks:
                if push_block.get_area().colliderect(push_block2.get_area()) and push_block2 != push_block: # does not check prev right
                    push_block2.x += X_SPEED
                    for obstacle in obstacles:
                        if obstacle.colliderect(push_block2.get_area()): # does not check prev right
                            push_block2.x = obstacle[0] - push_block2.size
                            push_block.x = obstacle[0] - push_block2.size - push_block.size
                            player.x = obstacle[0] - push_block2.size - push_block.size - player.size


    if keys[pygame.K_UP] and player.cur_frame == 0 and not player.falling:
        player.jumping = True

    if keys[pygame.K_SPACE] and first_space and outside_parent:
        if player.size == 96:
            big_push_block = PushBlock(player.x, player.y, 96, DARK_RED)
            old_block = big_push_block
            player = Player(player.x + 12, player.y + 24, 72, BLUE)
            jump_frames = [x-38 for x in jump_frames]
            _, *jump_frames = jump_frames # codegolf trick to popping last
            outside_parent = False
        elif player.size == 72:
            small_push_block = PushBlock(player.x, player.y, 72, DARK_BLUE)
            old_block = small_push_block
            player = Player(player.x + 12, player.y + 24, 48, MAGENTA)
            jump_frames = [x-32 for x in jump_frames]
            _, *jump_frames = jump_frames
            outside_parent = False
        first_space = False
    if keys[pygame.K_z] and win:
        cur_level += 1
        start_level()
    if not keys[pygame.K_SPACE]:
        first_space = True

    if keys[pygame.K_r]: # restart
        start_level()

    screen.fill(WHITE)
    check_win = True

    for goal_zone in goal_zones:
        if player.get_area().colliderect(goal_zone) or \
            any([push_block.get_area().colliderect(goal_zone) for push_block in push_blocks]) or \
            old_block and old_block.get_area().colliderect(goal_zone):
            pygame.draw.rect(screen, LIGHT_GREEN, goal_zone)
        else:
            pygame.draw.rect(screen, LIGHTER_GREEN, goal_zone)
            check_win = False

    if check_win:
        win = True
    if win:
        text('CONGRATULATIONS!', 410, 110, 80, GOLD)
        if cur_level == LAST_LEVEL:
            text('You Win! Thank you for Playing!', 240, 210, 80, GOLD)
        else:
            text('Press Z to continue', 445, 210, 80, BLACK)


    for obstacle in obstacles:
        pygame.draw.rect(screen, GREY, obstacle)
    for push_block in push_blocks:
        pygame.draw.rect(screen, push_block.colour, push_block.get_area())
    if old_block:
        pygame.draw.rect(screen, old_block.colour, old_block.get_area())

    if old_block:
        if not old_block.get_area().colliderect(player.get_area()):
            outside_parent = True
            push_blocks.append(old_block)
            old_block = None

    # if player feet not on ground
    if not player.jumping and not player.falling and not any([obstacle.colliderect(player.get_feet_area()) for obstacle in [push_block.get_area() for push_block in push_blocks] + obstacles]):
        player.falling = True
        player.cur_frame = len(jump_frames) - 1

    for push_block in [*push_blocks, old_block]:
        if push_block and not push_block.falling and not any([obstacle.colliderect(push_block.get_feet_area()) for obstacle in [push_block.get_area() for push_block in push_blocks] + obstacles]):
            push_block.falling = True
            push_block.cur_frame = len(jump_frames) - 1

    pygame.draw.rect(screen, player.colour, player.get_area())

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
# Close the window and quit.
pygame.quit()
