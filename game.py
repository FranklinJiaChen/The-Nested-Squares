import pygame
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

# Variables
X_SPEED = 10

JUMP_HEIGHT = 100
cur_frame = 0

# big frame jumps

# when jumping go left to right. When falling go right to left
# (subtracting adjacent values to get frame difference)
jump_frames = [38, 72, 102, 128, 150, 168, 182, 192, 198, 200]

x = 50
y = screen_height-40-80
cur_size = 80

jumping = False
falling = False

cur_colour = PURPLE
push_blocks = []
old_block = []
obstacles = []

first_space = True
outside_parent = True

font = pygame.font.SysFont('freesansbold.ttf', 30)
smallerfont = pygame.font.SysFont('freesansbold.ttf', 27)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# level 1 environment
floor_area = pygame.Rect(0, screen_height-40, screen_width, 40)
left_wall = pygame.Rect(0, 0, 20, screen_height)
right_wall = pygame.Rect(screen_width-20, 0, 20, screen_height)
obstacles.append(floor_area)
obstacles.append(left_wall)
obstacles.append(right_wall)

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

        if cur_frame > 0:
            cur_frame -= 1

        y_prev_bottom = y + cur_size
        y += cur_jump_size
        player_area =  pygame.Rect(x, y, cur_size, cur_size)
        for obstacle in push_blocks + obstacles:
            if obstacle.colliderect(player_area) and y_prev_bottom <= obstacle[1]:
                y = obstacle[1]-cur_size
                falling = False
                cur_frame = 0


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x_prev_left = x
        x -= X_SPEED
        player_area =  pygame.Rect(x, y, cur_size, cur_size)
        for obstacle in obstacles:
            if obstacle.colliderect(player_area) and x_prev_left >= obstacle[0] + obstacle[2]:
                x = obstacle[0] + obstacle[2]
        for push_block in push_blocks:
            if push_block.colliderect(player_area) and x_prev_left >= push_block[0] + push_block[2]:
                push_block_prev_left = push_block[0]
                push_block[0] -= X_SPEED
                for obstacle in obstacles:
                    if obstacle.colliderect(push_block) and push_block_prev_left >= obstacle[0] + obstacle[2]:
                        push_block[0] = obstacle[0] + obstacle[2]
                        x = obstacle[0] - obstacle[0] + obstacle[2] + push_block[3]
            for push_block2 in push_blocks:
                if push_block.colliderect(push_block2) and push_block2 != push_block: # does not check prev left
                    push_block2[0] -= X_SPEED
                    for obstacle in obstacles:
                        if obstacle.colliderect(push_block2): # does not check prev left
                            push_block2[0] = obstacle[0] + obstacle[2]
                            push_block[0] = obstacle[0] + obstacle[2] + push_block2[3]
                            x = obstacle[0] - obstacle[0] + obstacle[2] + push_block2[3] + push_block[3]
    if keys[pygame.K_RIGHT]:
        x_prev_right = x + cur_size
        x += X_SPEED
        player_area =  pygame.Rect(x, y, cur_size, cur_size)
        for obstacle in  obstacles:
            if obstacle.colliderect(player_area) and x_prev_right <= obstacle[0]:
                x = obstacle[0] - cur_size
        for push_block in push_blocks:
            if push_block.colliderect(player_area) and x_prev_right <= obstacle[0]:
                push_block_prev_right = push_block[0] + push_block[2]
                push_block[0] += X_SPEED
                for obstacle in obstacles:
                    if obstacle.colliderect(push_block) and push_block_prev_right <= obstacle[0]:
                        push_block[0] = obstacle[0] - push_block[3]
                        x = obstacle[0] - push_block[3] - cur_size
            for push_block2 in push_blocks:
                if push_block.colliderect(push_block2) and push_block2 != push_block: # does not check prev right
                    push_block2[0] += X_SPEED
                    for obstacle in obstacles:
                        if obstacle.colliderect(push_block2): # does not check prev right
                            push_block2[0] = obstacle[0] - push_block2[3]
                            push_block[0] = obstacle[0] - push_block2[3] - push_block2[3]
                            x = obstacle[0] - obstacle[0] - push_block2[3] - push_block2[3] - cur_size


    if keys[pygame.K_UP] and cur_frame == 0 and not falling:
        jumping = True
    if keys[pygame.K_SPACE] and first_space and outside_parent:
        if cur_size == 80:
            old_block = pygame.Rect(x, y, 80, 80)
            x += 20
            y += 40
            cur_size //= 2
            jump_frames = [x//2 for x in jump_frames]
            cur_colour = BLUE
            outside_parent = False
        elif cur_size == 40:
            old_block = pygame.Rect(x, y, 40, 40)
            x += 10
            y += 20
            cur_size //= 2
            jump_frames = [x//2 for x in jump_frames]
            cur_colour = RED
            outside_parent = False
        first_space = False
    elif not keys[pygame.K_SPACE]:
        first_space = True


    screen.fill(WHITE)
    player_area =  pygame.Rect(x, y, cur_size, cur_size)


    for obstacle in obstacles:
        pygame.draw.rect(screen, GREY, obstacle)
    for push_block in push_blocks:
        pygame.draw.rect(screen, BLACK, push_block)
    if old_block:
        pygame.draw.rect(screen, BLACK, old_block)

    if old_block:
        if not pygame.Rect(old_block).colliderect(player_area):
            outside_parent = True
            push_blocks.append(old_block)
            old_block = []

    # if player feet not on ground
    player_feet_area = pygame.Rect(x, y+cur_size, cur_size, 1)
    if not jumping and not falling and not any([obstacle.colliderect(player_feet_area) for obstacle in push_blocks + obstacles]):
        falling = True
        cur_frame = len(jump_frames) - 1

    pygame.draw.rect(screen, cur_colour, player_area)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
# Close the window and quit.
pygame.quit()
