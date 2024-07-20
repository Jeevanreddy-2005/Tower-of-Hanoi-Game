import pygame
import sys
import time

pygame.init()
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

# game vars:
remaining_moves = 0
n_disks = 3
disks = []
towers_midx = [256, 512, 768]
pointing_at = 0
floating = False
floater = 0
player_name = ""
lives = 3
start_time = 0
elapsed_time = 0

# colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (255, 215, 0)
blue = (0, 191, 255)
grey = (169, 169, 169)
green = (50, 205, 50)
purple = (128, 0, 128)
orange = (255, 165, 0)

def blit_text(surface, text, midtop, aa=True, font=None, font_name=None, size=None, color=(255, 0, 0)):
    if font is None:
        font = pygame.font.SysFont(font_name, size)
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    surface.blit(font_surface, font_rect)

def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_player_name():
    global player_name, screen
    input_box = pygame.Rect(362, 400, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    start_button = pygame.Rect(412, 500, 200, 50)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                elif start_button.collidepoint(event.pos) and text:
                    player_name = text
                    done = True
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and text:
                        player_name = text
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((173, 216, 230))  # Light blue background

        # Welcome message
        blit_text(screen, 'Welcome to', (512, 100), font_name='sans serif', size=60, color=(0, 0, 139))  # Dark blue text
        blit_text(screen, 'The Tower of Hanoi', (512, 170), font_name='sans serif', size=80, color=(0, 0, 139))  # Dark blue text

        blit_text(screen, 'Please enter your name:', (512, 350), font_name='sans serif', size=40, color=(0, 0, 139))  # Dark blue text
        txt_surface = pygame.font.Font(None, 50).render(text, True, (0, 0, 0))  # Black text for input
        width = max(300, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.draw.rect(screen, (0, 128, 0), start_button)  # Green button
        pygame.draw.rect(screen, (255, 255, 255), start_button, 2)  # White border
        blit_text(screen, 'Start Playing', start_button.center, font_name='sans serif', size=30, color=(255, 255, 255))

        pygame.display.flip()
        clock.tick(30)
        
def calculate_max_moves(n):
    return 2**n - 1

def difficulty_selection():
    global n_disks, game_done, remaining_moves, start_time
    menu_done = False
    while not menu_done:
        # Create a gradient background
        for y in range(768):
            r = int(50 + (150 * y / 768))
            g = int(205 + (50 * y / 768))
            b = int(50 + (150 * y / 768))
            pygame.draw.line(screen, (r, g, b), (0, y), (1024, y))
        
        blit_text(screen, 'Towers of Hanoi', (512, 50), font_name='sans serif', size=80, color=(255, 255, 255))  # White text
        blit_text(screen, 'Select Difficulty Level:', (512, 150), font_name='sans serif', size=40, color=(0, 100, 0))  # Dark green text

        buttons = [
            ('Very Easy', (412, 200), (200, 60), (0, 255, 0)),  # Bright green
            ('Easy', (412, 280), (200, 60), (144, 238, 144)),  # Light green
            ('Medium', (412, 360), (200, 60), (255, 255, 0)),  # Yellow
            ('Hard', (412, 440), (200, 60), (255, 165, 0)),  # Orange
            ('Very Hard', (412, 520), (200, 60), (255, 0, 0)),  # Red
            ('More coming soon...', (412, 600), (200, 60), (169, 169, 169))  # Grey
        ]

        for text, (x, y), (w, h), color in buttons:
            button = pygame.Rect(x, y, w, h)
            pygame.draw.rect(screen, color, button)
            pygame.draw.rect(screen, white, button, 2)
            blit_text(screen, text, button.center, font_name='sans serif', size=24, color=black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (text, (x, y), (w, h), _) in enumerate(buttons):
                    button = pygame.Rect(x, y, w, h)
                    if button.collidepoint(event.pos):
                        if i < 5:  # Exclude the "More coming soon..." option
                            n_disks = i + 3  # 3 to 7 disks
                            remaining_moves = calculate_max_moves(n_disks)
                            start_time = time.time()  # Start the timer when difficulty is selected
                            menu_done = True
                        elif i == 5:
                            show_popup_message("More levels coming soon!", 2000)

        pygame.display.flip()
        clock.tick(60)

def show_rules():
    rules = [
        "Rules of Tower of Hanoi:",
        "1. Only one disk can be moved at a time.",
        "2. Each move consists of taking the upper disk",
        "   from one of the stacks and placing it on",
        "   top of another stack or on an empty rod.",
        "3. No larger disk may be placed on top of",
        "   a smaller disk. If done it will cost you a life",
        "",
        f"You have {remaining_moves} moves to complete the puzzle.",
        "",
        f"Running out of moves and Lives Exits the Game",
        "Press any key to start the game."
    ]
    rules_done = False
    while not rules_done:
        screen.fill((245, 245, 220))  # Beige background
        y = 150
        for line in rules:
            blit_text(screen, line, (512, y), font_name='sans serif', size=30, color=(101, 67, 33))  # Dark brown text
            y += 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                rules_done = True

        pygame.display.flip()
        clock.tick(30)

def game_over(won):
    global screen, remaining_moves, lives, player_name, elapsed_time
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    screen.fill((0, 0, 51))  # Dark navy blue background
    if won:
        blit_text(screen, f'Congratulations, {player_name}!', (512, 150), font_name='sans serif', size=60, color=gold)
        blit_text(screen, 'You Won!', (512, 250), font_name='sans serif', size=60, color=gold)
        blit_text(screen, f'You completed the puzzle in {calculate_max_moves(n_disks) - remaining_moves} moves.', (512, 330), font_name='mono', size=30, color=(192, 192, 192))
        blit_text(screen, f'Time taken: {format_time(elapsed_time)}', (512, 380), font_name='mono', size=30, color=(192, 192, 192))
    else:
        blit_text(screen, f'Game Over, {player_name}!', (512, 150), font_name='sans serif', size=60, color=red)
        if lives <= 0:
            blit_text(screen, 'You ran out of lives!', (512, 250), font_name='sans serif', size=40, color=red)
        else:
            blit_text(screen, 'You ran out of moves!', (512, 250), font_name='sans serif', size=40, color=red)
        blit_text(screen, 'Better luck next time!', (512, 330), font_name='sans serif', size=30, color=(192, 192, 192))

    blit_text(screen, f'Moves Used: {calculate_max_moves(n_disks) - remaining_moves}', (512, 400), font_name='mono', size=30, color=(192, 192, 192))
    blit_text(screen, f'Maximum Moves: {calculate_max_moves(n_disks)}', (512, 450), font_name='mono', size=30, color=(192, 192, 192))
    blit_text(screen, f'Lives Remaining: {lives}', (512, 500), font_name='mono', size=30, color=(192, 192, 192))
    blit_text(screen, f'Time taken: {format_time(elapsed_time)}', (512, 550), font_name='mono', size=30, color=(192, 192, 192))

    replay_button = pygame.Rect(262, 600, 150, 60)
    restart_button = pygame.Rect(437, 600, 150, 60)
    exit_button = pygame.Rect(612, 600, 150, 60)

    pygame.draw.rect(screen, green, replay_button)
    pygame.draw.rect(screen, orange, restart_button)
    pygame.draw.rect(screen, red, exit_button)
    pygame.draw.rect(screen, white, replay_button, 2)
    pygame.draw.rect(screen, white, restart_button, 2)
    pygame.draw.rect(screen, white, exit_button, 2)

    blit_text(screen, 'Replay', replay_button.center, font_name='sans serif', size=30, color=black)
    blit_text(screen, 'Restart', restart_button.center, font_name='sans serif', size=30, color=black)
    blit_text(screen, 'Exit', exit_button.center, font_name='sans serif', size=30, color=black)

    pygame.display.flip()
    game_done = False
    while not game_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    game_done = True
                    reset(same_level=True)
                elif restart_button.collidepoint(event.pos):
                    game_done = True
                    reset(same_level=False)
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def draw_towers():
    global screen
    tower_width = 180
    tower_height = 300
    base_y = 668
    for xpos in towers_midx:
        pygame.draw.rect(screen, green, pygame.Rect(xpos - tower_width // 2, base_y, tower_width, 20))
        pygame.draw.rect(screen, grey, pygame.Rect(xpos - 5, base_y - tower_height, 10, tower_height))
    blit_text(screen, 'Start', (towers_midx[0], base_y + 25), font_name='mono', size=20, color=white)
    blit_text(screen, 'Finish', (towers_midx[2], base_y + 25), font_name='mono', size=20, color=white)

def make_disks():
    global n_disks, disks
    disks = []
    height = 30
    ypos = 638 - height
    width = n_disks * 25
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (towers_midx[0], ypos)
        disk['val'] = n_disks - i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height + 3
        width -= 25

def draw_disks():
    global screen, disks
    for disk in disks:
        pygame.draw.rect(screen, blue, disk['rect'])
        pygame.draw.rect(screen, white, disk['rect'], 2)

def draw_ptr():
    ptr_points = [(towers_midx[pointing_at] - 10, 718),
                  (towers_midx[pointing_at] + 10, 718),
                  (towers_midx[pointing_at], 698)]
    pygame.draw.polygon(screen, red, ptr_points)

def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(0.2)
        game_over(True)

def reset(same_level=False):
    global remaining_moves, pointing_at, floating, floater, lives, start_time
    pointing_at = 0
    floating = False
    floater = 0
    lives = 3
    if not same_level:
        difficulty_selection()
    else:
        remaining_moves = calculate_max_moves(n_disks)
    start_time = time.time()  # Reset the timer
    show_rules()
    make_disks()

def show_popup_message(message, duration=2000):
    popup_surface = pygame.Surface((400, 100))
    popup_surface.fill(white)
    pygame.draw.rect(popup_surface, black, popup_surface.get_rect(), 3)
    blit_text(popup_surface, message, (200, 50), font_name='sans serif', size=24, color=black)
    popup_rect = popup_surface.get_rect(center=(512, 384))
    screen.blit(popup_surface, popup_rect)
    pygame.display.flip()
    pygame.time.wait(duration)

get_player_name()
difficulty_selection()
show_rules()
make_disks()

# main game loop:
game_done = False
while not game_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset()
            if event.key == pygame.K_q:
                game_done = True
            if event.key == pygame.K_RIGHT:
                pointing_at = (pointing_at + 1) % 3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_LEFT:
                pointing_at = (pointing_at - 1) % 3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_UP and not floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at:
                        floating = True
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers_midx[pointing_at], 100)
                        break
            if event.key == pygame.K_DOWN and floating:
                valid_move = True
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk) != floater:
                        if disk['val'] < disks[floater]['val']:
                            valid_move = False
                            lives -= 1
                            mistake_message = f"Mistake: Can't place larger disk on smaller one. Lives left: {lives}"
                            show_popup_message(mistake_message)
                            if lives <= 0:
                                game_over(False)
                            break
                        else:
                            floating = False
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top - 33)
                            remaining_moves -= 1
                            break
                else:
                    floating = False
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 638)
                    remaining_moves -= 1
                
                if valid_move:
                    screen.fill((0, 0, 51))  # Dark navy blue background
                    draw_towers()
                    draw_disks()
                    draw_ptr()
                    blit_text(screen, f'Moves Left: {remaining_moves}', (512, 20), font_name='mono', size=40, color=(192, 192, 192))  # Silver text
                    blit_text(screen, f'Lives: {lives}', (512, 70), font_name='mono', size=40, color=(192, 192, 192))  # Silver text
                    pygame.display.flip()

    screen.fill((0, 0, 51))  # Dark navy blue background
    draw_towers()
    draw_disks()
    draw_ptr()
    blit_text(screen, f'Moves Left: {remaining_moves}', (512, 20), font_name='mono', size=40, color=(192, 192, 192))  # Silver text
    blit_text(screen, f'Lives: {lives}', (512, 70), font_name='mono', size=40, color=(192, 192, 192))  # Silver text
    
    elapsed_time = time.time() - start_time
    blit_text(screen, f'Time: {format_time(elapsed_time)}', (512, 120), font_name='mono', size=40, color=(192, 192, 192))
    
    pygame.display.flip()
    if not floating: 
        check_won()
    if remaining_moves <= 0:
        game_over(False)
    clock.tick(60)

pygame.quit()
sys.exit()