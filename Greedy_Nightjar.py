'''
To do:
1) Main menu with animated background (Play, Controls, About)      - done
2) Lost game menu without background (score info, best score, play again, main menu, exit) - done
3) Owl fly trajectory - non-linear     - done
4) Owl screams before appearing      - done
5) Animation for arrow down (slav nightjar)    - done
6) The morning coming after ... "hours", with clocks visible
'''

import pygame
from pygame import mixer
from random import randint


version = 2.0

pygame.init()
win = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Алчный козодой")

mixer.music.load("Sound\\night_forest.mp3")
menu_move_sound = mixer.Sound("Sound\\menu_move.wav")
menu_chosen_sound = mixer.Sound("Sound\\menu_chosen.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.3)

bg = pygame.transform.scale(pygame.image.load("Pics\\background.png"), (1000, 700))
bg_intro = pygame.transform.scale(pygame.image.load("Pics\\background.png"), (2000, 1400))
tree = pygame.transform.scale(pygame.image.load("Pics\\tree.png"), (1000, 700))
tree_intro = pygame.transform.scale(pygame.image.load("Pics\\tree.png"), (2000, 1400))
player_stand = pygame.transform.scale(pygame.image.load("Pics\\test_cozodoy_standing.png"), (200, 200))
player_stand_intro = pygame.transform.scale(pygame.image.load("Pics\\test_cozodoy_standing.png"), (400, 400))
player_jump = pygame.transform.scale(pygame.image.load("Pics\\cozodoy_jump.png"), (200, 200))
player_stand_eat = pygame.transform.scale(pygame.image.load("Pics\\cozodoy_eat_stand.png"), (200, 200))
player_stand_eat_intro = pygame.transform.scale(pygame.image.load("Pics\\cozodoy_eat_stand.png"), (400, 400))
player_jump_eat = pygame.transform.scale(pygame.image.load("Pics\\cozodoy_eat_jump.png"), (200, 200))
player_sit = pygame.transform.scale(pygame.image.load("Pics\\cozodoy_sitting.png"), (200, 200))
player_sit_eat = pygame.transform.scale(pygame.image.load("Pics\\cozodoy_sitting_eat.png"), (200, 200))
player_back_intro = pygame.transform.scale(pygame.image.load("Pics\\cozodoy_back.png"), (400, 400))
cursor = pygame.transform.scale(pygame.image.load("Pics\\cursor_paw.png"), (70, 70))
controls_menu = pygame.transform.scale(pygame.image.load("Pics\\ControlsMenu.png"), (1000, 700))
about_menu = pygame.transform.scale(pygame.image.load("Pics\\AboutMenu.png"), (1000, 700))
eaten_menu = pygame.transform.scale(pygame.image.load("Pics\\EatenMenu.png"), (1000, 700))


walk_left = []
for i in range(8):
    walk_left.append(pygame.transform.scale(pygame.image.load(f"Pics\\cozodoy_step_{i + 1}.png"), (200, 200)))

walk_left_eat = []
for i in range(8):
    walk_left_eat.append(pygame.transform.scale(pygame.image.load(f"Pics\\cozodoy_eat_step_{i + 1}.png"), (200, 200)))

font = pygame.font.SysFont("candara", 36)
font_intro = pygame.font.SysFont("candara", 40)
font_intro_2 = pygame.font.SysFont("candara", 90, bold=True)
menufont = pygame.font.SysFont("candara", 36)

def show_score(x, y):
    score = font.render(f"Score: {total_score}", True, (200, 200, 100))
    win.blit(score, (x, y))


class MainMenu():
    def __init__(self):
        self.rect_size = (200, 50)
        self.main_menu_font = pygame.font.SysFont("candara", 90)
        self.title_font = pygame.font.SysFont("candara", 90, bold=True)
        self.controls_font = pygame.font.SysFont("candara", 45)
        self.small_font = pygame.font.SysFont("candara", 25)
        self.about_font = pygame.font.SysFont("candara", 35)
        self.buttons = ["Play", "Controls", "About", "Quit"]
        self.buttons_playing = ["Continue", "Controls", "About", "Quit"]
        self.button_left_edges = []
        self.cursor_pos = 0
        self.controls = False
        self.about = False
        self.control_keys = [
            "E - eat",
            "ArrowLeft, A - walk left",
            "ArrowRight, D - walk right",
            "ArrowDown, S - get down",
            "Space - jump",
            "Esc - open menu"
                             ]
        self.about_lines = [f"version {version}",
                            "Greedy Nightjar in the night forest is trying",
                            "to catch moths and to avoid the Owl's claws.",
                            "My first game written in Python3 with pygame.",
                            "Contacts: Oleg Shchepin, ledum_laconicum@mail.ru",
                            "Latest version available here:",
                            "https://github.com/Gurdhhu/Greedy_Nightjar"]
    def draw_button(self, button_text, button_y, font):
        button_text_renderer = font.render(button_text,
                                       True,
                                       (250, 250, 250))
        if not self.controls:
            win.blit(button_text_renderer, (int(500 - button_text_renderer.get_width() / 2),
                                   button_y))
            self.button_left_edges.append(int(500 - button_text_renderer.get_width() / 2))
        else:
            width_before_dash = font.render(button_text[:button_text.index("-")], True, (250, 250, 250)).get_width()
            win.blit(button_text_renderer, (500 - width_before_dash,
                                            button_y))
    def draw(self):
        self.button_left_edges = []
        win.blit(bg_intro, (-300, -300))
        if not self.controls and not self.about:
            title_renderer = self.title_font.render("Greedy Nightjar",
                                               True,
                                               (250, 250, 250))
            win.blit(title_renderer, (int(500 - title_renderer.get_width() / 2), 90))
            if not playing:
                for bnum, button in enumerate(self.buttons):
                    self.draw_button(button, 190 + 100 * bnum, self.main_menu_font)
            else:
                for bnum, button in enumerate(self.buttons_playing):
                    self.draw_button(button, 190 + 100 * bnum, self.main_menu_font)
            win.blit(cursor, (self.button_left_edges[self.cursor_pos] - 100, 190 + 100 * self.cursor_pos))
            pygame.display.update()
        elif self.controls:
            win.blit(controls_menu, (0, 0))
            for knum, key in enumerate(self.control_keys):
                self.draw_button(key, 150 + 50 * knum, self.controls_font)
            go_back_renderer = self.small_font.render("Press Esc to return to Main Menu",
                                               True,
                                               (250, 250, 250))
            win.blit(go_back_renderer, (int(500 - go_back_renderer.get_width() / 2),
                                            150 + 50 * len(self.control_keys)))
            pygame.display.update()
        else:
            win.blit(about_menu, (0, 0))
            title_renderer = self.title_font.render("Greedy Nightjar",
                                               True,
                                               (250, 250, 250))
            win.blit(title_renderer, (int(500 - title_renderer.get_width() / 2), 90))
            for lnum, line in enumerate(self.about_lines):
                self.draw_button(line, 190 + 50 * lnum, self.about_font)
            go_back_renderer = self.small_font.render("Press Esc to return to Main Menu",
                                               True,
                                               (250, 250, 250))
            win.blit(go_back_renderer, (int(500 - go_back_renderer.get_width() / 2),
                                            190 + 50 * len(self.about_lines)))
            pygame.display.update()


class Moon():
    def __init__(self, x, y, size):
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load("Pics\\Moon.png"), self.size)
        self.x = x
        self.y = y
        self.counter_x = 0
        self.counter_y = 0
    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

class Owl():
    def __init__(self):
        self.facing = (1, -1)[randint(0, 1)]
        if self.facing == 1:
            self.x = randint(-300, 400)
        else:
            self.x = randint(600, 1300)
        self.y = -300
        self.vel = 10 * self.facing
        self.fly_count = randint(50, 100)  # change fly_dir after fly_count == 0
        self.fly_dir = 1  # 1 for flying down, -1 for flying up
        self.image = pygame.transform.scale(pygame.image.load("Pics\\owl_fly_0.png"), (300, 300))
        self.attack = pygame.transform.scale(pygame.image.load("Pics\\owl_fly_claws.png"), (300, 300))
        self.appear_sound = mixer.Sound("Sound\\owl_appears.wav")
        if self.facing == 1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.attack = pygame.transform.flip(self.attack, True, False)
        self.claws_out = False
        self.wait = 40

    def draw(self, win):
        if self.y < y and abs(self.x - x) <= 300:
            self.claws_out = True
            win.blit(self.attack, (self.x, self.y))

        else:
            self.claws_out = False
            win.blit(self.image, (self.x, self.y))

    def draw_claw_rect(self, win):
        global eaten
        if self.claws_out:
            if self.facing == 1:
                self.claw_coo = (self.x + 180, self.y + 215)
            else:
                self.claw_coo = (self.x + 120, self.y + 215)

            self.claws_rect = pygame.draw.circle(win, (200, 0, 0), self.claw_coo, 40)
            if is_sitting:
                if self.claws_rect.colliderect(pygame.Rect((x + 50, y + 130, 100, 70))):
                    eaten = True
            else:
                if last == "left":
                    if self.claws_rect.colliderect(pygame.Rect((x + 50, y + 25, 50, 100))):
                        eaten = True
                else:
                    if self.claws_rect.colliderect(pygame.Rect((x + 100, y + 25, 50, 100))):
                        eaten = True

class Star():
    def __init__(self):
        self.x = randint(0, 1000)
        self.y = randint(0, 400)
        self.facing = (-1, 1)[randint(0, 1)]
        self.color = [(253, 253, 177), (144, 242, 246), (255, 123, 123)][randint(0, 2)]
        self.vel = 20
        self.inclination = randint(1, 10)
        self.lifetime = randint(5, 50)
        self.count = 0
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), 2)

class Moth():
    def __init__(self, y, size, facing, vel):
        self.images_left = []
        self.images_right = []
        self.x = 1
        self.y = y
        self.size = size
        self.color = ["white", "yellow", "blue"][randint(0, 2)]
        self.facing = facing
        self.vel = vel * facing
        self.fly_count = 0
        self.fly_amplitude = 50 + randint (-10, 10)
        self.fly_dir = ["up", "down"][randint(0, 1)]
        self.fly_stage = 0
        self.active_images = self.images_left

        for i in range(4):
            self.images_left.append(pygame.transform.scale(pygame.image.load(f"Pics\\moth_{self.color}_fly_{i + 1}.png"),
                                                      (size * 10, size * 10)))

        for i in range(4):
            newimage = pygame.transform.scale(pygame.image.load(f"Pics\\moth_{self.color}_fly_{i + 1}.png"),
                                                      (size * 10, size * 10))
            self.images_right.append(pygame.transform.flip(newimage, True, False))

        if self.facing == -1:
            self.x = 999
            self.active_images = self.images_left
        else:
            self.active_images = self.images_right

    def draw(self, win):
        if self.fly_count + 1 >= 12:
            self.fly_count = 0

        win.blit(self.active_images[self.fly_count // 3], (self.x, self.y))
        self.fly_count += 1

def draw_window():
    global anim_count, time_count
    global total_score, scores, bg

    for owl in owls:
        owl.draw_claw_rect(win)

    win.blit(bg, (0, 0))

    for star in stars:
        star.draw(win)

    moon.draw(win)

    win.blit(tree, (0, 0))

    if anim_count + 1 >= 32:
        anim_count = 0

    if is_jump == True:
        if beak_open:
            if last == "left":
                win.blit(player_jump_eat, (x, y))
            else:
                win.blit(pygame.transform.flip(player_jump_eat, True, False), (x, y))
        else:
            if last == "left":
                win.blit(player_jump, (x, y))
            else:
                win.blit(pygame.transform.flip(player_jump, True, False), (x, y))
    elif is_sitting == True:
        if last == "left":
            if beak_open:
                win.blit(player_sit_eat, (x, y))
            else:
                win.blit(player_sit, (x, y))
        else:
            if beak_open:
                win.blit(pygame.transform.flip(player_sit_eat, True, False), (x, y))
            else:
                win.blit(pygame.transform.flip(player_sit, True, False), (x, y))

    elif left:
        if beak_open:
            win.blit(walk_left_eat[anim_count // 4], (x, y))
            anim_count += 1
        else:
            win.blit(walk_left[anim_count // 4], (x, y))
            anim_count += 1

    elif right:
        if beak_open:
            win.blit(pygame.transform.flip(walk_left_eat[anim_count // 4], True, False), (x, y))
            anim_count += 1
        else:
            win.blit(pygame.transform.flip(walk_left[anim_count // 4], True, False), (x, y))
            anim_count += 1

    else:
        if last == "left":
            if beak_open:
                win.blit(player_stand_eat, (x, y))
            else:
                win.blit(player_stand, (x, y))
        else:
            if beak_open:
                win.blit(pygame.transform.flip(player_stand_eat, True, False), (x, y))
            else:
                win.blit(pygame.transform.flip(player_stand, True, False), (x, y))

    for moth in moths:
        moth.draw(win)

    for owl in owls:
        owl.draw(win)

    if beak_open:
        if not is_sitting:
            if last == "left":
                if is_jump:
                    throat_center = (x+67, y+57)
                    throat = pygame.draw.circle(win, (50, 15, 15), throat_center, 23)
                    inner_throat = pygame.draw.circle(win, (0, 0, 0), throat_center, 15)
                else:
                    throat_center = (x+67, y+63)
                    throat = pygame.draw.circle(win, (50, 15, 15), throat_center, 23)
                    inner_throat = pygame.draw.circle(win, (0, 0, 0), throat_center, 15)
            else:
                if is_jump:
                    throat_center = (x+131, y+57)
                    throat = pygame.draw.circle(win, (50, 15, 15), throat_center, 23)
                    inner_throat = pygame.draw.circle(win, (0, 0, 0), throat_center, 15)
                else:
                    throat_center = (x + 131, y + 63)
                    throat = pygame.draw.circle(win, (50, 15, 15), throat_center, 23)
                    inner_throat = pygame.draw.circle(win, (0, 0, 0), throat_center, 15)
        else:
            if last == "left":
                throat_center = (x + 60, y + 150)
                throat = pygame.draw.circle(win, (50, 15, 15), throat_center, 23)
                inner_throat = pygame.draw.circle(win, (0, 0, 0), throat_center, 15)
            else:
                throat_center = (x + 140, y + 150)
                throat = pygame.draw.circle(win, (50, 15, 15), throat_center, 23)
                inner_throat = pygame.draw.circle(win, (0, 0, 0), throat_center, 15)


        for moth in moths:
            if throat.colliderect(pygame.Rect((moth.x, moth.y, moth.size*10, moth.size*10))):
                eaten_sound = mixer.Sound("Sound\\moth_eaten.wav")
                eaten_sound.play()
                total_score += moth.size * 10
                moths.pop(moths.index(moth))

    if not eaten:
        show_score(800, 15)

    if eaten:
        scores.append(total_score)
        text_eaten1 = menufont.render("Nightjar is devoured by Owl.",
                                     True,
                                     (250, 250, 250))  # Козодой сожран совой!
        text_eaten2 = menufont.render(f"Total score: {total_score}",
                                     True,
                                     (250, 250, 250))
        text_eaten5 = menufont.render(f"Your best score: {max(scores)}",
                                     True,
                                     (250, 250, 250))
        text_eaten3 = menufont.render("Play again?",
                                     True,
                                     (250, 250, 250))
        text_eaten4 = menufont.render("Yes (Enter) / No (Esc)",
                                     True,
                                     (250, 250, 250))
        win.blit(eaten_menu, (0, 0))
        win.blit(text_eaten1, (int(1000 / 2 - text_eaten1.get_width() / 2),
                              int(650 / 2 - text_eaten1.get_height() / 2 - text_eaten1.get_height())))
        win.blit(text_eaten2, (int(1000 / 2 - text_eaten2.get_width() / 2),
                              int(700 / 2 - text_eaten2.get_height() / 2)))
        win.blit(text_eaten5, (int(1000 / 2 - text_eaten5.get_width() / 2),
                              int(700 / 2 - text_eaten3.get_height() / 2 + text_eaten3.get_height())))
        win.blit(text_eaten3, (int(1000 / 2 - text_eaten3.get_width() / 2),
                              int(750 / 2 - text_eaten3.get_height() / 2 + text_eaten3.get_height() * 2)))
        win.blit(text_eaten4, (int(1000 / 2 - text_eaten4.get_width() / 2),
                              int(750 / 2 - text_eaten4.get_height() / 2 + text_eaten4.get_height() * 3)))

    pygame.display.update()


clock = pygame.time.Clock()

total_score = 0
scores = []

x = 50
y = 255
speed = 7

is_jump = False
jump_count = 11
is_sitting = False

left = False
right = False
last = "right"
anim_count = 0

beak_open = False
beak_open_count = 3
beak_closed_count = 2
eaten = False

run = True
moths = []
stars = []
owls = []
facing_values = [1, -1]
colors = ["white", "red", "blue"]
moon = Moon(-100, 100, (180, 180))
moon_intro = Moon(320, 0, (300, 300))

intro_count = 240
intro = True
text_count = 1
sound_intro = False
intro_beak_open = True
intro_beak_open_count = 0
intro_beak_closed_count = 0

menu = True
play_again = True
playing = False

time_count = 0

while intro and intro_count > 0:
    clock.tick(30)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
        intro = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro = False
            play_again = False

    intro_count -= 1

    win.blit(bg_intro, (-800, -200))

    for star in stars:
        if star.x > 0 and star.x < 1000 and star.y > 0 and star.y < 700 and star.count < star.lifetime:
            star.x += star.vel * star.facing * 2
            star.y += int((star.inclination ** 2) / 2)
            star.count += 1
        else:
            stars.pop(stars.index(star))

    for star in stars:
        star.draw(win)

    moon_intro.draw(win)

    win.blit(tree_intro, (0, -450))

    if intro_count > 140:
        win.blit(player_back_intro, (400, 100))
        intro_text_full = font_intro.render("Greedy Nightjar is eager to eat some moths",
                                       True,
                                       (250, 250, 250),
                                       (0, 0, 0))
        intro_text = font_intro.render("Greedy Nightjar is eager to eat some moths"[:text_count],
                                       True,
                                       (250, 250, 250))
        win.blit(intro_text, (int(500 - intro_text_full.get_width() / 2), 30))
        text_count += 1

    elif intro_count > 90:
        intro_text = font_intro_2.render("HELP HIM", True, (250, 250, 250))
        win.blit(intro_text, (int(500 - intro_text.get_width() / 2), 60))
        win.blit(player_stand_intro, (400, 100))

    elif intro_count > 40:
        if sound_intro == False:
            eaten_sound = mixer.Sound("Sound\\intro_voice.wav")
            eaten_sound.play()
            sound_intro = True
        intro_text = font_intro_2.render("HELP HIM", True, (250, 250, 250))
        win.blit(intro_text, (int(500 - intro_text.get_width() / 2), 60))
        if intro_beak_open:
            if intro_beak_open_count < 4:
                win.blit(player_stand_eat_intro, (400, 100))
                intro_beak_open_count += 1
            else:
                win.blit(player_stand_eat_intro, (400, 100))
                intro_beak_open = False
                intro_beak_open_count = 0
        else:
            if intro_beak_closed_count < 4:
                win.blit(player_stand_intro, (400, 100))
                intro_beak_closed_count += 1
            else:
                win.blit(player_stand_intro, (400, 100))
                intro_beak_open = True
                intro_beak_closed_count = 0

        if intro_count < 65:
            intro_text = font_intro.render("And beware of the owl claws...",
                                           True, (250, 250, 250))
            win.blit(intro_text, (int(500 - intro_text.get_width() / 2), 500))

    else:
        win.blit(player_stand_intro, (400, 100))
        intro_text = font_intro.render("And beware of the owl claws...",
                                       True, (250, 250, 250))
        win.blit(intro_text, (int(500 - intro_text.get_width() / 2), 500))

    if randint(0, 30) == 1:
        stars.append(Star())

    pygame.display.update()

def play():
    global x, y, speed, is_jump, jump_count, is_sitting, left, right, last, anim_count
    global beak_open, beak_open_count, beak_closed_count, eaten, clock, run, moths, stars, owls
    global facing_values, colors, moon, total_score, scores, play_again, menu, playing, version

    total_score = 0

    x = 50
    y = 255
    speed = 7

    is_jump = False
    jump_count = 11

    left = False
    right = False
    last = "right"
    anim_count = 0

    beak_open = False
    beak_open_count = 3
    beak_closed_count = 2
    eaten = False
    eaten_sound = False

    clock = pygame.time.Clock()
    run = True
    moths = []
    stars = []
    owls = []
    facing_values = [1, -1]
    colors = ["white", "red", "blue"]
    moon = Moon(-100, 100, (180, 180))

    while(run):
        clock.tick(30)

        if not eaten and not menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    play_again = False
                    playing = False
                if event.type == pygame.KEYDOWN:
                    if not beak_open:
                        if event.key == pygame.K_e and beak_closed_count >= 3:
                            beak_open = True

                    if not is_jump:
                        if event.key == pygame.K_SPACE:
                            is_jump = True
                            is_sitting = False

                    if event.key == pygame.K_ESCAPE:
                        mixer.music.pause()
                        menu = True

            if is_jump:
                if jump_count >= -11:
                    if jump_count < 0:
                        y += int((jump_count ** 2) / 2)
                    else:
                        y -= int((jump_count ** 2) / 2)
                    jump_count -= 1
                else:
                    is_jump = False
                    jump_count = 11

            if beak_open:
                if beak_open_count > 0:
                    beak_open_count -= 1
                else:
                    beak_open = False
                    beak_open_count = 3
                    beak_closed_count = 0
            else:
                beak_closed_count += 1

            if moon.counter_x == 7:
                moon.x += 1
                moon.counter_x = 0
            else:
                moon.counter_x += 1

            if moon.counter_y == 12:
                moon.y -= 1
                moon.counter_y = 0
            else:
                moon.counter_y += 1

            for owl in owls:
                if owl.x > -300 and owl.x < 1300 and owl.y >= -300 and owl.y < 700:
                    if owl.wait < 0:
                        if owl.fly_count > 0 and owl.fly_dir == 1:
                            owl.x += owl.vel
                            owl.y += abs(owl.vel) * owl.fly_dir
                            owl.fly_count -= 1
                        elif owl.fly_count == 0:
                            owl.fly_dir = -1
                            owl.x += owl.vel
                            owl.fly_count += 1
                        elif owl.fly_count < 3:
                            owl.x += owl.vel
                            owl.fly_count += 1
                        else:
                            owl.x += owl.vel
                            owl.y += abs(owl.vel) * owl.fly_dir
                            owl.fly_count += 1
                    else:
                        owl.wait -= 1
                else:
                    owls.pop(owls.index(owl))

            for star in stars:
                if star.x > 0 and star.x < 1000 and star.y > 0 and star.y < 700 and star.count < star.lifetime:
                    star.x += star.vel * star.facing * 2
                    star.y += int((star.inclination ** 2) / 2)
                    star.count += 1
                else:
                    stars.pop(stars.index(star))

            for moth in moths:
                if moth.x > 0 and moth.x < 1000:
                    moth.x += moth.vel

                    if moth.fly_dir == "up":
                        if moth.fly_stage < moth.fly_amplitude:
                            moth.y += int(moth.vel * (1 - moth.fly_stage / moth.fly_amplitude)) + randint(-5, 5)
                            moth.fly_stage += 1
                        else:
                            moth.fly_dir = "down"
                            moth.y -= int(moth.vel * (1 - moth.fly_stage / moth.fly_amplitude)) + randint(-5, 5)
                            moth.fly_stage -= 1

                    else:
                        if moth.fly_stage > moth.fly_amplitude // 2:
                            moth.y -= int(moth.vel * (1 - moth.fly_stage / moth.fly_amplitude)) + randint(-5, 5)
                            moth.fly_stage -= 1
                        elif moth.fly_stage > 0:
                            moth.y -= int(moth.vel * (moth.fly_stage / moth.fly_amplitude)) + randint(-5, 5)
                            moth.fly_stage -= 1
                        else:
                            moth.fly_dir = "up"
                            moth.y += int(moth.vel * (1 - moth.fly_stage / moth.fly_amplitude)) + randint(-5, 5)
                            moth.fly_stage += 1

                else:
                    moths.pop(moths.index(moth))

            keys = pygame.key.get_pressed()

            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and x > 0:
                if not keys[pygame.K_DOWN] or not keys[pygame.K_s]:
                    is_sitting = False
                    x -= speed
                    left = True
                    right = False
                    last = "left"
                else:
                    is_sitting = True
                    left = False
                    right = False
                    last = "left"
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and x < 800:
                if not keys[pygame.K_DOWN] or not keys[pygame.K_s]:
                    is_sitting = False
                    x += speed
                    right = True
                    left = False
                    last = "right"
                else:
                    is_sitting = True
                    left = False
                    right = False
                    last = "right"
            elif not is_jump and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                is_sitting = True
            else:
                left = False
                right = False
                is_sitting = False
                anim_count = 0

            if len(moths) <= 5 and randint(0, 30) == 1:
                moths.append(Moth(y=randint(1, 300),
                                  size=randint(4, 7),
                                  facing=facing_values[randint(0, 1)],
                                  vel=randint(3, 5)))

            if randint(0, 30) == 1:
                stars.append(Star())

            if not owls:
                if randint(0, 120) == 1:
                    owls.append(Owl())
                    for owl in owls:
                        owl.appear_sound.play()

            draw_window()

        elif eaten:
            playing = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    play_again = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = False
                        play_again = True
                        playing = True
                    elif event.key == pygame.K_ESCAPE:
                        run = False
                        play_again = True
                        playing = False
                        menu = True
            if not eaten_sound:
                eaten_sound = mixer.Sound("Sound\\eaten_by_owl.wav")
                eaten_sound.play()
                eaten_sound.set_volume(0.3)
                eaten_sound = True
            anim_count = 0

            draw_window()

        else:
            main_menu = MainMenu()
            while menu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        play_again = False
                        menu = False
                    if not main_menu.controls and not main_menu.about:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                if playing:
                                    mixer.music.unpause()
                                    menu = False
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                menu_move_sound.play()
                                if main_menu.cursor_pos < len(main_menu.buttons) - 1:
                                    main_menu.cursor_pos += 1
                                else:
                                    main_menu.cursor_pos = 0
                            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                                menu_move_sound.play()
                                if main_menu.cursor_pos > 0:
                                    main_menu.cursor_pos -= 1
                                else:
                                    main_menu.cursor_pos = len(main_menu.buttons) - 1
                            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_e:
                                menu_chosen_sound.play()
                                if main_menu.cursor_pos == 0:
                                    playing = True
                                    menu = False
                                    mixer.music.unpause()
                                elif main_menu.cursor_pos == 1:
                                    main_menu.controls = True
                                elif main_menu.cursor_pos == 2:
                                    main_menu.about = True
                                elif main_menu.cursor_pos == 3:
                                    run = False
                                    play_again = False
                                    menu = False
                    elif main_menu.controls:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                main_menu.controls = False
                    elif main_menu.about:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                main_menu.about = False

                main_menu.draw()


while play_again:
    play()

pygame.quit()
