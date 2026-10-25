import curses
import random
import time

# --- Game Configuration ---
SCREEN_WIDTH = 60
SCREEN_HEIGHT = 20
PADDLE_WIDTH = 8
FPS = 15

def main(stdscr):
    # Setup curses environment
    curses.curs_set(0)          # Hide the blinking cursor
    stdscr.nodelay(True)        # Make getch() non-blocking
    stdscr.timeout(1000 // FPS) # Set input timeout based on FPS

    # Initial Game Positions
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - 2

    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 3
    ball_dx = random.choice([-1, 1])
    ball_dy = 1

    # Generate Bricks (3 rows)
    bricks = []
    for r in range(2, 5):
        for c in range(2, SCREEN_WIDTH - 2):
            bricks.append([r, c])

    score = 0
    lives = 3
    game_over = False
    victory = False

    while True:
        stdscr.clear()

        # Draw Game Borders
        for x in range(SCREEN_WIDTH):
            stdscr.addch(0, x, '#')
            stdscr.addch(SCREEN_HEIGHT - 1, x, '#')
        for y in range(SCREEN_HEIGHT):
            stdscr.addch(y, 0, '#')
            stdscr.addch(y, SCREEN_WIDTH - 1, '#')

        # Draw HUD (Heads-Up Display)
        hud_text = f" Score: {score}  |  Lives: {lives}  |  Press 'Q' to Quit "
        stdscr.addstr(0, 2, hud_text)

        # Game States Screens
        if game_over:
            stdscr.addstr(SCREEN_HEIGHT // 2, (SCREEN_WIDTH - 11) // 2, "GAME OVER!!")
            stdscr.addstr(SCREEN_HEIGHT // 2 + 1, (SCREEN_WIDTH - 26) // 2, "Press 'R' to Restart or 'Q'")
        elif victory:
            stdscr.addstr(SCREEN_HEIGHT // 2, (SCREEN_WIDTH - 13) // 2, "YOU WIN!!!!")
            stdscr.addstr(SCREEN_HEIGHT // 2 + 1, (SCREEN_WIDTH - 26) // 2, "Press 'R' to Restart or 'Q'")
        else:
            # Draw Bricks
            for brick in bricks:
                stdscr.addch(brick[0], brick[1], '=')

            # Draw Paddle
            for i in range(PADDLE_WIDTH):
                if 0 < paddle_x + i < SCREEN_WIDTH - 1:
                    stdscr.addch(paddle_y, paddle_x + i, '_')

            # Draw Ball
            stdscr.addch(ball_y, ball_x, 'O')

            # Ball Movement Logic
            ball_x += ball_dx
            ball_y += ball_dy

            # Wall Collisions (Left & Right)
            if ball_x <= 1 or ball_x >= SCREEN_WIDTH - 2:
                ball_dx *= -1

            # Ceiling Collision
            if ball_y <= 1:
                ball_dy *= -1

            # Paddle Collision
            if ball_y == paddle_y:
                if paddle_x <= ball_x < paddle_x + PADDLE_WIDTH:
                    ball_dy = -1
                    # Add variance based on where the ball hits the paddle
                    if ball_x < paddle_x + (PADDLE_WIDTH // 2):
                        ball_dx = -1
                    else:
                        ball_dx = 1

            # Brick Collisions
            for brick in bricks:
                if ball_y == brick[0] and ball_x == brick[1]:
                    bricks.remove(brick)
                    ball_dy *= -1
                    score += 10
                    break

            # Victory Condition
            if not bricks:
                victory = True

            # Floor Collision (Lose a Life)
            if ball_y >= SCREEN_HEIGHT - 1:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    # Reset positions for next life
                    ball_x = SCREEN_WIDTH // 2
                    ball_y = SCREEN_HEIGHT // 3
                    ball_dx = random.choice([-1, 1])
                    ball_dy = 1
                    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2

        stdscr.refresh()

        # Handle Keyboard Inputs
        try:
            key = stdscr.getch()
        except Exception:
            key = -1

        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('r') or key == ord('R'):
            # Full Restart Game
            paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 3
            ball_dx = random.choice([-1, 1])
            ball_dy = 1
            bricks = [[r, c] for r in range(2, 5) for c in range(2, SCREEN_WIDTH - 2)]
            score = 0
            lives = 3
            game_over = False
            victory = False
        elif key == curses.KEY_LEFT or key == ord('a') or key == ord('A'):
            if paddle_x > 1:
                paddle_x -= 2
        elif key == curses.KEY_RIGHT or key == ord('d') or key == ord('D'):
            if paddle_x < SCREEN_WIDTH - PADDLE_WIDTH - 1:
                paddle_x += 2

if __name__ == "__main__":
    curses.wrapper(main)
