"""
PONG Template for Lab2 (Introduction to Programming)
---------------------------------------------------------
Didactic objectives (focus on functions):
- Practice defining and using functions using parameters and return values.
- Avoid global variables.
- Chain functions that transform the game state (positions and velocities).
- DO NOT use classes, lists, or dictionaries.
- Fill the code where needed. Keep functions' names and signatures EXACT.

Submission:
- Through your team's GitHub repository (see Section 9 of the Lab 2 instructions).
- Save this file in the repository as: pong.py
- Must run locally with: `python pong.py` (macOS: `python3 pong.py`)
- Requires pygame-ce (install with `python -m pip install pygame-ce`).
  Your code still uses `import pygame`.

Restrictions / Style rules:
- No `class`, no `list`, no `dict` (tuples are allowed for multiple returns).
- Do not use `assert` or define classes. Simple string methods such as
  `.lower()` or `.strip()` are allowed.
- Define and use the functions marked TODO. Do not rename them.
- Constants can be read but NOT modified at runtime.
- The main loop and rendering section are provided; do not change or move them,
  except where an optional feature requires it (explain any change in your report).

Anti-AI-copy/paste control:
- You must be able to explain to the professor what each function does
- You must be able to explain specific sections of your program to the professor to verify your understanding
- If you used AI tools, explain how in your report (section "Use of AI tools")
"""

import sys      # Used only for sys.exit(0): ensures clean program termination on all OSs
import pygame   # essential for all the game rendering and play
import random   # useful for randomising things a little bit (e.g. ball's initial direction)

# ==============
# Game constants
# ==============

# Modify them here if you want to change the board size 
WIDTH = 900     # pixels   
HEIGHT = 600    # idem
FPS = 60        # Frames per Second - No need to change - for changing paddles/ball speeds change the following ->

# Speeds (pixels per frame approx.) (all 3 values can be changed in get_config() )
SPEED_PADDLE = 7
SPEED_BALL_X = 6
SPEED_BALL_Y = 5

# Background and Foreground RGB default colors (can be changed in change_colors() )
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Geometry: paddle and ball default values (some can be changed in get_config() )
PADDLE_W = 14       # pixels
PADDLE_H = 110      # 110 pixels - can be changed in get_config()
PADDLE_MARGIN = 30  # pixels - distance from border
BALL_RADIUS = 9     # pixels - can be changed in get_config()
POINTS_END = 5      # score for ending a match
SERVE_PAUSE = 300   # ms between each serve

# Player keys: Change here if other keys are preferred
KEY_UP_LEFT = pygame.K_a            # a
KEY_DOWN_LEFT = pygame.K_z          # z
KEY_UP_RIGHT = pygame.K_UP          # arrow UP
KEY_DOWN_RIGHT = pygame.K_DOWN      # arrow DOWN

# Play against machine (optional feature): set to True once compute_ai_direction() is implemented
PLAY_AGAINST_MACHINE = True     # True = play against the computer, False = two players

# ==============================================================================
# Functions to complete by the students : configuration/setup before game starts
# ==============================================================================

def get_config() -> tuple[int, int, int, int, int]:
    """
    Ask the player whether they want to customise the game settings.
    Returns a tuple with (paddle height, paddle speed, ball X speed,
    ball Y speed, ball radius).
    """

    # If the player answers "no", keep the default values defined as constants
    if not ask_yes_no("Do you want to change the game parameters?"):
        return PADDLE_H, SPEED_PADDLE, SPEED_BALL_X, SPEED_BALL_Y, BALL_RADIUS

    # Otherwise, ask for each parametre one by one.
    # Each value must be witin the given range (min, max);
    # if the player just presses Enter, the default value is used.
    paddle_h = read_int_in_range_w_default("Paddle height", 60, 160, PADDLE_H) # height of the paddles in pixels
    paddle_speed = read_int_in_range_w_default("Paddle speed", 3, 15, SPEED_PADDLE) # pixels the paddle moves per frame
    ball_vx = read_int_in_range_w_default("Ball X speed", 2, 12, SPEED_BALL_X) # horizontal speed of the ball
    ball_vy = read_int_in_range_w_default("Ball Y speed", 2, 12, SPEED_BALL_Y) # vertical speed of the ball
    ball_radius = read_int_in_range_w_default("Ball radius", 4, 20, BALL_RADIUS) # size of the ball in pixels

    # Return all the chosen values so the game can use them
    return paddle_h, paddle_speed, ball_vx, ball_vy, ball_radius

def change_colors() -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """
    Ask the player whether they want to customise the game colors.
    Returns a tuple with (background color, foreground color),
    where each color is an (R, G, B) tuple.
    """

    # If the player answers "no", keep the default colors:
    # black background and white foreground (paddles, ball, text)
    if not ask_yes_no("Do you want to change the colors?"):
        return BLACK, WHITE

    # Otherwise, ask the player to choose each color
    backg_col = read_color("background") # color of the game window background
    foreg_col = read_color("foreground") # color of the paddles, ball and score

    # Return both colors so the game can use them when drawing
    return backg_col, foreg_col

def read_color(prompt: str) -> tuple[int, int, int]:
    """
    Ask the player to enter a color as its RGB components.
    'prompt' is the name of the element being colored
    ("background" or "foreground").
    Returns the color as an (R, G, B) tuple.
    """

    # Tell the player which color they are choosing
    print(f"Enter the {prompt} color:")

    # Ask for each RGB component; each must be between 0 and 255
    r = read_int_in_range("Red", 0, 255) # amount of red
    g = read_int_in_range("Green", 0, 255) # amount of green
    b = read_int_in_range("Blue", 0, 255) # amount of blue

    # Return the three values together as one color
    return r, g, b

def read_int_in_range(prompt: str, low: int, high: int) -> int:
    """
    Ask the player for a whole number between 'low' and 'high' (both included).
    Keeps asking until a valid number is entered, then returns it.
    """

    # Repeat until the player enters a valid value
    while True:
        # Show the question with the allowed range and remove extra spaces
        text = input(f"{prompt} from {low} to {high}: ").strip()

        # Try to convert the text to an integer
        try:
            value = int(text)
        except ValueError:
            # The input was not a whole number (e.g. "abc" or "3.5")
            print("Please enter a whole number.")
            continue # go back to the start of the loop and ask again

        # If the number is inside the range, it is valid: return it
        if low <= value <= high:
            return value

        # The number is outside the range: tell the player and ask again
        print(f"The value must be between {low} and {high}.")

def read_int_in_range_w_default(prompt: str, low: int, high: int, default_val: int) -> int:
    """
    Ask the player for a whole number between 'low' and 'high' (both included).
    If the player just presses ENTER, 'default_val' is returned instead.
    Keeps asking until a valid number (or ENTER) is entered.
    """

    # Repeat until the player enters a valid value or presses ENTER
    while True:
        # Show the question with the allowed range and the default value,
        # and remove extra spaces from the answer
        text = input(f"{prompt} from {low} to {high} (ENTER = {default_val}): ").strip()

        # Empty answer (only ENTER pressed): use the default value
        if text == "":
            return default_val

        # Try to convert the text to an integer
        try:
            value = int(text)
        except ValueError:
            # The input was not an integer number ( "abc" or "3.5")
            print("Please enter a whole number.")
            continue # go back to the start of the loop and ask again

        # If the number is inside the range, it is valid: return it
        if low <= value <= high:
            return value

        # The number is outside the range: tell the player and ask again
        print(f"The value must be between {low} and {high}.")

def ask_yes_no(prompt: str) -> bool:
    """
    Ask the player a yes/no question.
    Returns True if the answer is yes and False if it is no.
    Keeps asking until a valid answer is entered.
    """

    # Repeat until the player gives a valid answer
    while True:
        # Show the question, remove extra spaces and convert to lowercase
        # so "Y", "YES" or " yes " are also accepted
        answer = input(f"{prompt} (y/n): ").strip().lower()

        # Accept "y" or "yes" as a positive answer
        if answer == "y" or answer == "yes":
            return True

        # Accept "n" or "no" as a negative answer
        if answer == "n" or answer == "no":
            return False

        # Any other answer is invalid: tell the player and ask again
        print("Please answer y/n.")

# ================================
# Functions to complete: main game
# ================================

def move_paddle(current_y: int, direction: int, speed: int, height: int, paddle_h: int) -> int:
    """
    Calculate the new vertical position of a paddle.
    'current_y' is the top edge of the paddle, 'direction' is -1 (up),
    1 (down) or 0 (no movement), 'speed' is how many pixels it moves,
    'height' is the window height and 'paddle_h' is the paddle height.
    Returns the new y position, kept inside the screen.
    """

    # Move the paddle: direction decides up/down, speed decides how far
    new_y = current_y + (direction * speed)

    # If the paddle goes above the top of the screen, stop it at the top
    if new_y < 0:
        new_y = 0
    # If the bottom of the paddle goes below the screen, stop it at the bottom
    elif new_y > height - paddle_h:
        new_y = height - paddle_h # guarantee that the whole paddle stays visible on the screen

    # Return the corrected position
    return new_y

def move_ball(x: int, y: int, vx: int, vy: int) -> tuple[int, int]:
    """
    Calculate the new position of the ball after one frame.
    'x' and 'y' are the current position of the ball,
    'vx' and 'vy' are its horizontal and vertical speeds.
    Returns the new (x, y) position.
    """

    # Move the ball horizontally: positive vx = right, negative vx = left
    new_x = x + vx
    # Move the ball vertically: positive vy = down, negative vy = up
    new_y = y + vy

    # Return the new position
    return new_x, new_y


def collide_ball_walls(x: int, y: int, vx: int, vy: int, radius: int, width: int, height: int) -> tuple[int, int, int, int]:
    """
    Make the ball bounce off the top and bottom walls of the screen.
    'x' and 'y' are the center of the ball, 'vx' and 'vy' its speeds,
    'radius' its size, and 'width' and 'height' the window size.
    Returns the updated (x, y, vx, vy).
    """

    # The top edge of the ball (y - radius) has reached or passed the top wall
    if y - radius <= 0:
        y = radius # put the ball back just inside the screen
        vy = -vy # reverse vertical direction so it bounces down
    # The bottom edge of the ball (y + radius) has reached or passed the bottom wall
    elif y + radius >= height:
        y = height - radius # put the ball back just inside the screen
        vy = -vy # reverse vertical direction so it bounces up

    # x and vx are not changed here: the left and right sides are not walls,
    # they are where points are scored
    return x, y, vx, vy

def collide_ball_paddle(x: int, y: int, vx: int, vy: int, paddle_x: int, paddle_y: int, paddle_w: int, paddle_h: int, radius: int) -> tuple[int, int, int, int, bool]:
    """
    Check if the ball hits a paddle and, if so, make it bounce.
    'x' and 'y' are the center of the ball, 'vx' and 'vy' its speeds,
    'paddle_x' and 'paddle_y' the top-left corner of the paddle,
    'paddle_w' and 'paddle_h' its size, and 'radius' the ball's radius.
    Returns the updated (x, y, vx, vy) and 'hit' (True if there was a collision).
    """

    # No collision yet
    hit = False

    # Ball's bounding box: we use the radius to calculate the 4 edges of the ball
    ball_left = x - radius
    ball_right = x + radius
    ball_top = y - radius
    ball_bottom = y + radius

    # Paddle's box: calculated from its top-left corner, width and height
    pad_left = paddle_x
    pad_right = paddle_x + paddle_w
    pad_top = paddle_y
    pad_bottom = paddle_y + paddle_h

    # The two boxes overlap (they touch horizontally AND vertically)
    if ball_right >= pad_left and ball_left <= pad_right and ball_bottom >= pad_top and ball_top <= pad_bottom:
        hit = True
        # The ball collided with the paddle, so we adjust its position and direction
        if vx < 0:  # moving left: it hit the left paddle, so we put it on the paddle's right side
            x = pad_right + radius
        else: # moving right: it hit the right paddle, so we put it on the paddle's left side
            x = pad_left - radius
        vx = -vx # reverse horizontal direction so it bounces back

    # vy is not changed: the ball keeps its vertical direction after the bounce
    return x, y, vx, vy, hit

def reset_ball(center_x: int, center_y: int, vx0: int, vy0: int, to_right: bool) -> tuple[int, int, int, int]:
    """
    Put the ball back in the center of the screen after a point is scored.
    'center_x' and 'center_y' are the center of the window,
    'vx0' and 'vy0' are the starting speeds of the ball,
    and 'to_right' decides which side the ball moves towards.
    Returns the new (x, y, vx, vy) of the ball.
    """

    # Horizontal direction depends on the Boolean parameter to_right
    if to_right:
        vx = vx0 # if True, the ball moves to the right
    else:
        vx = -vx0 # if False, the ball moves to the left

    # Random vertical direction so that the game is not predictable
    if random.random() < 0.5: # 50% chance to go down or up
        vy = vy0
    else:
        vy = -vy0

    # The ball starts again from the center with its new speeds
    return center_x, center_y, vx, vy



def compute_ai_direction(ball_y: int, paddle_y: int, paddle_h: int) -> int:
    """
    Decide which way the computer-controlled paddle should move.
    'ball_y' is the vertical position of the ball, 'paddle_y' the top
    of the paddle and 'paddle_h' its height.
    Returns -1 (move up), 1 (move down) or 0 (stay still).
    """

    # Vertical center of the paddle
    paddle_center = paddle_y + paddle_h / 2

    # Small margin in pixels so the paddle stays still when the ball is
    # close to its center, instead of shaking up and down every frame
    tolerance = 10

    if ball_y < paddle_center - tolerance:
        return -1 # ball is above the paddle -> move up
    elif ball_y > paddle_center + tolerance:
        return 1 # ball is below the paddle -> move down

    # Ball is within the tolerance zone -> don't move
    return 0

# =============================================
# Checking KEYS UP/DOWN (given to the students)
# =============================================

def read_player_direction(keys, key_up: int, key_down: int) -> int:
    """Return -1, 0, or +1 based on pressed keys."""
    if keys[key_up]:
        return -1
    elif keys[key_down]:
        return 1
    return 0

# =================================
# Rendering (given to the students)
# =================================

def draw_scene(screen: pygame.Surface,
               x: int, y: int,
               p1y: int, p2y: int,
               score_left: int, score_right: int,
               paddle_h: int, ball_radius: int,
               backg_col, foreg_col) -> None:
    
    screen.fill(backg_col)
    # center line
    pygame.draw.line(screen, foreg_col, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 1)
    # paddles
    pygame.draw.rect(screen, foreg_col, pygame.Rect(PADDLE_MARGIN, int(p1y), PADDLE_W, paddle_h))
    pygame.draw.rect(screen, foreg_col, pygame.Rect(WIDTH - PADDLE_MARGIN - PADDLE_W, int(p2y), PADDLE_W, paddle_h))
    # ball
    pygame.draw.circle(screen, foreg_col, (int(x), int(y)), ball_radius)
    # score (simple)
    font = pygame.font.Font(None, 48)
    text = font.render(f"{score_left}   {score_right}", True, foreg_col)
    rect = text.get_rect(center=(WIDTH//2, 40))
    screen.blit(text, rect)
    pygame.display.flip()

def show_message(screen: pygame.Surface,message: str,backg_col, foreg_col, show_time_ms) -> None:
    """Display 'message' centered on the game screen.
    Used at the end of the game"""
    # Choose font and text color
    font = pygame.font.Font(None, 96)     # default pygame font, size 96
    text = font.render(message, True, foreg_col)

    # Center the text in the middle of the screen
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Fill the screen with the background color and draw the text
    screen.fill(backg_col)
    screen.blit(text, rect)
    pygame.display.flip()

    # Pause for show_time_ms milliseconds so players can see it
    pygame.time.wait(show_time_ms)



# =================================
# Main loop (given to the students)
# =================================

def main() -> None:
    paddle_h, paddle_speed, speed_ball_x, speed_ball_y, ball_radius = get_config()
    backg_col, foreg_col = change_colors()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab 2 - Pong")
    clock = pygame.time.Clock()

    # Initial state (no lists or objects)
    p1_y = (HEIGHT - paddle_h) / 2
    p2_y = (HEIGHT - paddle_h) / 2
    ball_x, ball_y, ball_vx, ball_vy = reset_ball(WIDTH//2, HEIGHT//2, speed_ball_x, speed_ball_y, to_right=True)

    score_left = 0
    score_right = 0

    running = True

    while running:
        # 1) Events (close window + input)
        direction_left = 0
        direction_right = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()

        # Left paddle always human
        direction_left = read_player_direction(keys, KEY_UP_LEFT, KEY_DOWN_LEFT)

        # Right paddle can be human or AI
        if PLAY_AGAINST_MACHINE:
            direction_right = compute_ai_direction(ball_y, p2_y, paddle_h)
        else:
            direction_right = read_player_direction(keys, KEY_UP_RIGHT, KEY_DOWN_RIGHT)


        # 2) Update state (ONLY by calling functions)
        p1_y = move_paddle(p1_y, direction_left, paddle_speed, HEIGHT, paddle_h)
        p2_y = move_paddle(p2_y, direction_right, paddle_speed, HEIGHT, paddle_h)

        ball_x, ball_y = move_ball(ball_x, ball_y, ball_vx, ball_vy)
        ball_x, ball_y, ball_vx, ball_vy = collide_ball_walls(ball_x, ball_y, ball_vx, ball_vy, ball_radius, WIDTH, HEIGHT)

        # Collision with left paddle
        ball_x, ball_y, vx_tmp, vy_tmp, hit_left = collide_ball_paddle(
            ball_x, ball_y, ball_vx, ball_vy,
            PADDLE_MARGIN, p1_y, PADDLE_W, paddle_h, ball_radius
        )
        if hit_left:
            ball_vx, ball_vy = vx_tmp, vy_tmp

        # Collision with right paddle
        ball_x, ball_y, vx_tmp, vy_tmp, hit_right = collide_ball_paddle(
            ball_x, ball_y, ball_vx, ball_vy,
            WIDTH - PADDLE_MARGIN - PADDLE_W, p2_y, PADDLE_W, paddle_h, ball_radius
        )
        if hit_right:
            ball_vx, ball_vy = vx_tmp, vy_tmp

        # 3) Scoring (if ball leaves screen): reset ball
        if ball_x < -ball_radius:
            score_right += 1
            pygame.time.wait(SERVE_PAUSE)  # short pause before re-serve
            ball_x, ball_y, ball_vx, ball_vy = reset_ball(WIDTH//2, HEIGHT//2, speed_ball_x, speed_ball_y, to_right=True)
        elif ball_x > WIDTH + ball_radius:
            score_left += 1
            pygame.time.wait(SERVE_PAUSE)  # short pause before re-serve
            ball_x, ball_y, ball_vx, ball_vy = reset_ball(WIDTH//2, HEIGHT//2, speed_ball_x, speed_ball_y, to_right=False)
        
        if score_left == POINTS_END or score_right == POINTS_END:
            show_message(screen,"Game Over!",backg_col, foreg_col,2000)
            running = False

        # 4) Render
        draw_scene(screen, ball_x, ball_y, p1_y, p2_y, score_left, score_right, 
                   paddle_h, ball_radius, backg_col, foreg_col)

        clock.tick(FPS)

    # exiting the main loop
    pygame.quit()
    sys.exit(0)   # Ensures complete and clean exit from the program (avoids hanging processes)

# ADVANCED NOTE:   
# The following 2 lines, start the program by calling the main() function
# When you run: python pong.py, Python sets a built-in variable: __name__ = "__main__"
# So the condition is to make sure that this main() function runs only when you execute this file directly, 
# and not when it is imported from another file.
if __name__ == "__main__":
    main()