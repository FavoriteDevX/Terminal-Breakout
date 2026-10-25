import sys
import os
import time
import random

# Enable ANSI escape characters natively inside Windows PowerShell/CMD
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# --- Game Configuration ---
SCREEN_WIDTH = 60
SCREEN_HEIGHT = 20
PADDLE_WIDTH = 8
FPS = 12

def get_keyboard_input():
    """Non-blocking keyboard input listener for Windows and Linux/macOS"""
    if os.name == 'nt':
        import msvcrt
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):  # Arrow keys handling
                ch = msvcrt.getch()
                if ch == b'K': return 'LEFT'
                if ch == b'M': return 'RIGHT'
            try:
                return ch.decode('utf-8').lower()
            except:
                return None
    else:
        import select
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select.select([sys.stdin], [], [], 0.0)
            if rlist:
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    ch2 = sys.stdin.read(1)
                    if ch2 == '[':
                        ch3 = sys.stdin.read(1)
                        if ch3 == 'D': return 'LEFT'
                        if ch3 == 'C': return 'RIGHT'
                return ch.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

def main():
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - 2

    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 3
    ball_dx = random.choice([-1, 1])
    ball_dy = 1

    # Generate bricks layer rows
    bricks = []
    for r in range(2, 5):
        for c in range(2, SCREEN_WIDTH - 2, 2):
            bricks.append([r, c])
            bricks.append([r, c + 1])

    score = 0
    lives = 3
    game_over = False
    victory = False

    # Hide the blinking terminal cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    # Clear terminal screen before start
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        while True:
            # Build screen frame buffer using optimized cursor jumping (\033[H)
            buffer = "\033[H"
            buffer += f" Score: {score}  |  Lives: {lives}  |  Press 'Q' to Quit\n"

            if game_over:
                buffer += "\n" * (SCREEN_HEIGHT // 2)
                buffer += " " * ((SCREEN_WIDTH - 11) // 2) + "GAME OVER!!\n"
                buffer += " " * ((SCREEN_WIDTH - 26) // 2) + "Press 'R' to Restart or 'Q'\n"
                buffer += "\n" * (SCREEN_HEIGHT // 2 - 2)
            elif victory:
                buffer += "\n" * (SCREEN_HEIGHT // 2)
                buffer += " " * ((SCREEN_WIDTH - 13) // 2) + "YOU WIN!!!!\n"
                buffer += " " * ((SCREEN_WIDTH - 26) // 2) + "Press 'R' to Restart or 'Q'\n"
                buffer += "\n" * (SCREEN_HEIGHT // 2 - 2)
            else:
                for y in range(SCREEN_HEIGHT):
                    for x in range(SCREEN_WIDTH):
                        if x == 0 or x == SCREEN_WIDTH - 1 or y == 0 or y == SCREEN_HEIGHT - 1:
                            buffer += '#'
                        elif [y, x] in bricks:
                            buffer += '='
                        elif y == paddle_y and paddle_x <= x < paddle_x + PADDLE_WIDTH:
                            buffer += '_'
                        elif y == ball_y and x == ball_x:
                            buffer += 'O'
                        else:
                            buffer += ' '
                    buffer += '\n'

            sys.stdout.write(buffer)
            sys.stdout.flush()
            time.sleep(1.0 / FPS)

            # Keyboard polling controller
            key = get_keyboard_input()
            if key == 'q':
                break
            elif key == 'r':
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
            elif key in ('a', 'LEFT'):
                if paddle_x > 1: paddle_x -= 2
            elif key in ('d', 'RIGHT'):
                if paddle_x < SCREEN_WIDTH - PADDLE_WIDTH - 1: paddle_x += 2

            # Physics engine simulation updates
            if not game_over and not victory:
                ball_x += ball_dx
                ball_y += ball_dy

                # Side wall bounces
                if ball_x <= 1:
                    ball_x = 1
                    ball_dx *= -1
                elif ball_x >= SCREEN_WIDTH - 2:
                    ball_x = SCREEN_WIDTH - 2
                    ball_dx *= -1

                # Ceiling bounce
                if ball_y <= 1:
                    ball_y = 1
                    ball_dy *= -1

                # Paddle collision hitboxes
                if ball_y == paddle_y:
                    if paddle_x <= ball_x < paddle_x + PADDLE_WIDTH:
                        ball_dy = -1
                        if ball_x < paddle_x + (PADDLE_WIDTH // 2):
                            ball_dx = -1
                        else:
                            ball_dx = 1

                # Brick physics impact detection
                for brick in bricks:
                    if ball_y == brick[0] and ball_x == brick[1]:
                        bricks.remove(brick)
                        ball_dy *= -1
                        score += 10
                        break

                if not bricks:
                    victory = True

                # Out of bounds floor detection
                if ball_y >= SCREEN_HEIGHT - 1:
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                    else:
                        ball_x = SCREEN_WIDTH // 2
                        ball_y = SCREEN_HEIGHT // 3
                        ball_dx = random.choice([-1, 1])
                        ball_dy = 1
                        paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    finally:
        # Show the cursor again when exiting the script execution context
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
