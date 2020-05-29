import pygame
from pygame import mixer
from random import randint


pygame.init()
win = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Алчный козодой")

mixer.music.load("Sound\\night_forest.mp3")
mixer.music.play(-1)

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
player_back_intro = pygame.transform.scale(pygame.image.load("Pics\\cozodoy_back.png"), (400, 400))

walk_left = []
for i in range(8):
    walk_left.append(pygame.transform.scale(pygame.image.load(f"Pics\\cozodoy_step_{i + 1}.png"), (200, 200)))

walk_left_eat = []
for i in range(8):
    walk_left_eat.append(pygame.transform.scale(pygame.image.load(f"Pics\\cozodoy_eat_step_{i + 1}.png"), (200, 200)))

font = pygame.font.SysFont("calibri", 36)
font_intro = pygame.font.SysFont("calibri", 40)
font_intro_2 = pygame.font.SysFont("calibri", 90)
menufont = pygame.font.SysFont("calibri", 36)

def show_score(x, y):
    score = font.render(f"Счет: {total_score}", True, (200, 200, 100))
    win.blit(score, (x, y))


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
        self.y = -200
        self.vel = 7 * self.facing
        self.image = pygame.transform.scale(pygame.image.load("Pics\\owl_fly_0.png"), (300, 300))
        self.attack = pygame.transform.scale(pygame.image.load("Pics\\owl_fly_claws.png"), (300, 300))
        if self.facing == 1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.attack = pygame.transform.flip(self.attack, True, False)
        self.claws_out = False

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
            if self.claws_rect.colliderect(pygame.Rect((x+50, y+25, 70, 100))):
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
    global anim_count
    global total_score

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

        for moth in moths:
            if throat.colliderect(pygame.Rect((moth.x, moth.y, moth.size*10, moth.size*10))):
                eaten_sound = mixer.Sound("Sound\\moth_eaten.wav")
                eaten_sound.play()
                total_score += moth.size * 10
                moths.pop(moths.index(moth))

    if not eaten:
        show_score(830, 15)

    if eaten:
        text_eaten1 = menufont.render(f"Козодой сожран совой!",
                                     True,
                                     (250, 250, 250))
        text_eaten2 = menufont.render(f"Вы набрали {total_score} очков.",
                                     True,
                                     (250, 250, 250))
        text_eaten3 = menufont.render(f"Играть снова?",
                                     True,
                                     (250, 250, 250))
        text_eaten4 = menufont.render(f"Да (Enter) / Нет (Esc)",
                                     True,
                                     (250, 250, 250))
        max_text_width = max(text_eaten1.get_width(), text_eaten2.get_width(), text_eaten4.get_width())
        textx = int(1000 / 2 - max_text_width / 2)
        texty = int(700 / 2 - text_eaten2.get_height() / 2)
        pygame.draw.rect(win, (0, 0, 0), ((textx - 5, texty - text_eaten2.get_height() - 5),
                                                (max_text_width + 10, text_eaten2.get_height() * 3 + 50)))
        win.blit(text_eaten1, (int(1000 / 2 - text_eaten1.get_width() / 2),
                              int(700 / 2 - text_eaten1.get_height() / 2 - text_eaten1.get_height())))
        win.blit(text_eaten2, (int(1000 / 2 - text_eaten2.get_width() / 2),
                              int(700 / 2 - text_eaten2.get_height() / 2)))
        win.blit(text_eaten3, (int(1000 / 2 - text_eaten3.get_width() / 2),
                              int(700 / 2 - text_eaten3.get_height() / 2 + text_eaten3.get_height())))
        win.blit(text_eaten4, (int(1000 / 2 - text_eaten4.get_width() / 2),
                              int(700 / 2 - text_eaten4.get_height() / 2 + text_eaten4.get_height() * 2)))

    pygame.display.update()


clock = pygame.time.Clock()

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

play_again = True

while intro and intro_count > 0:
    clock.tick(30)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
        intro = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro = False
            pygame.quit()

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
        intro_text = font_intro.render("Алчный козодой жаждет съесть жирных мотыльков"[:text_count],
                                       True,
                                       (250, 250, 250),
                                       (0, 0, 0))
        win.blit(intro_text, (70, 60))
        text_count += 1

    elif intro_count > 90:
        intro_text = font_intro_2.render("ПОМОГИ ЕМУ", True, (250, 250, 250), (0, 0, 0))
        win.blit(intro_text, (int(500 - intro_text.get_width() / 2), 60))
        win.blit(player_stand_intro, (400, 100))

    elif intro_count > 40:
        if sound_intro == False:
            eaten_sound = mixer.Sound("Sound\\intro_voice.wav")
            eaten_sound.play()
            sound_intro = True
        intro_text = font_intro_2.render("ПОМОГИ ЕМУ", True, (250, 250, 250), (0, 0, 0))
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
            intro_text = font_intro.render("И берегись когтей совы...", True, (250, 250, 250), (0, 0, 0))
            win.blit(intro_text, (int(500 - intro_text.get_width() / 2), 500))

    else:
        win.blit(player_stand_intro, (400, 100))
        intro_text = font_intro.render("И берегись когтей совы...", True, (250, 250, 250), (0, 0, 0))
        win.blit(intro_text, (int(500 - intro_text.get_width() / 2), 500))

    if randint(0, 30) == 1:
        stars.append(Star())

    pygame.display.update()

def play():
    global x, y, speed, is_jump, jump_count, left, right, last, anim_count, beak_open, beak_open_count
    global beak_closed_count, eaten, clock, run, moths, stars, owls, facing_values, colors, moon
    global total_score, play_again

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

        if not eaten:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    play_again = False
                if event.type == pygame.KEYDOWN:
                    if not beak_open:
                        if event.key == pygame.K_e and beak_closed_count >= 3:
                            beak_open = True

                    if not is_jump:
                        if event.key == pygame.K_SPACE:
                            is_jump = True

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
                if owl.x > -300 and owl.x < 1300 and owl.y > -300 and owl.y < 700:
                    owl.x += owl.vel
                    owl.y += abs(owl.vel)
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
                x -= speed
                left = True
                right = False
                last = "left"
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and x < 800:
                x += speed
                right = True
                left = False
                last = "right"
            else:
                left = False
                right = False
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

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    play_again = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = False
                        play_again = True
                    elif event.key == pygame.K_ESCAPE:
                        run = False
                        play_again = False
            if not eaten_sound:
                eaten_sound = mixer.Sound("Sound\\eaten_by_owl.wav")
                eaten_sound.play()
                eaten_sound = True
            anim_count = 0

        draw_window()

while play_again:
    play()

pygame.quit()
