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
SCREEN_WIDTH = 62
SCREEN_HEIGHT = 20
PADDLE_WIDTH = 10
FPS = 30  # High refresh rate for instant controls response

# ANSI Color Codes
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

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
    ball_y = SCREEN_HEIGHT // 2
    ball_dx = random.choice([-1, 1])
    ball_dy = -1

    # Generate distinct retro bricks layers with safe spacing
    bricks = []
    brick_width = 6
    
    for row_idx, color in [(2, RED), (3, GREEN), (4, YELLOW)]:
        for col_x in range(4, SCREEN_WIDTH - 6, brick_width):
            bricks.append({
                "y": row_idx, 
                "x_start": col_x, 
                "x_end": col_x + brick_width - 1, 
                "color": color
            })

    score = 0
    lives = 3
    game_over = False
    victory = False

    # Frame decoupling counter for ball physics ticks
    frame_count = 0
    ball_speed_divider = 3 # Moves the ball every 3 frames, keeping controls fast

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
                buffer += " " * ((SCREEN_WIDTH - 11) // 2) + RED + "GAME OVER!!" + RESET + "\n"
                buffer += " " * ((SCREEN_WIDTH - 26) // 2) + "Press 'R' to Restart or 'Q'\n"
                buffer += "\n" * (SCREEN_HEIGHT // 2 - 2)
            elif victory:
                buffer += "\n" * (SCREEN_HEIGHT // 2)
                buffer += " " * ((SCREEN_WIDTH - 13) // 2) + GREEN + "YOU WIN!!!!" + RESET + "\n"
                buffer += " " * ((SCREEN_WIDTH - 26) // 2) + "Press 'R' to Restart or 'Q'\n"
                buffer += "\n" * (SCREEN_HEIGHT // 2 - 2)
            else:
                # Render screen line by line
                for y in range(SCREEN_HEIGHT):
                    x = 0
                    while x < SCREEN_WIDTH:
                        if x == 0 or x == SCREEN_WIDTH - 1 or y == 0 or y == SCREEN_HEIGHT - 1:
                            buffer += '#'
                            x += 1
                        elif y == paddle_y and paddle_x <= x < paddle_x + PADDLE_WIDTH:
                            buffer += CYAN + "=" + RESET
                            x += 1
                        elif y == ball_y and x == ball_x:
                            buffer += "O"
                            x += 1
                        else:
                            matched_brick = None
                            for b in bricks:
                                if b["y"] == y and b["x_start"] <= x <= b["x_end"]:
                                    matched_brick = b
                                    break
                            
                            if matched_brick:
                                buffer += matched_brick["color"] + "[" + "=" * (brick_width - 2) + "]" + RESET
                                x += brick_width
                            else:
                                buffer += ' '
                                x += 1
                    buffer += '\n'

            sys.stdout.write(buffer)
            sys.stdout.flush()
            time.sleep(1.0 / FPS)
            frame_count += 1

            # Keyboard polling controller (Runs at max FPS for absolute responsiveness)
            key = get_keyboard_input()
            if key == 'q':
                break
            elif key == 'r':
                paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
                ball_x = SCREEN_WIDTH // 2
                ball_y = SCREEN_HEIGHT // 2
                ball_dx = random.choice([-1, 1])
                ball_dy = -1
                bricks = []
                for row_idx, color in [(2, RED), (3, GREEN), (4, YELLOW)]:
                    for col_x in range(4, SCREEN_WIDTH - 6, brick_width):
                        bricks.append({"y": row_idx, "x_start": col_x, "x_end": col_x + brick_width - 1, "color": color})
                score = 0
                lives = 3
                game_over = False
                victory = False
            elif key in ('a', 'LEFT'):
                if paddle_x > 1: paddle_x -= 3
            elif key in ('d', 'RIGHT'):
                if paddle_x < SCREEN_WIDTH - PADDLE_WIDTH - 1: paddle_x += 3

            # Decoupled Ball Physics Simulation Tick
            if not game_over and not victory and (frame_count % ball_speed_divider == 0):
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

                # Paddle collision hitboxes detection
                if ball_y == paddle_y:
                    if paddle_x <= ball_x < paddle_x + PADDLE_WIDTH:
                        ball_dy = -1
                        if ball_x < paddle_x + (PADDLE_WIDTH // 2):
                            ball_dx = -1
                        else:
                            ball_dx = 1

                # Robust bounding-box brick hit logic
                for b in bricks:
                    if ball_y == b["y"] and b["x_start"] <= ball_x <= b["x_end"]:
                        bricks.remove(b)
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
                        ball_y = SCREEN_HEIGHT // 2
                        ball_dx = random.choice([-1, 1])
                        ball_dy = -1
                        paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
                        time.sleep(1)
    finally:
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
