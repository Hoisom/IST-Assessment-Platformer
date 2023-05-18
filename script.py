import pygame
from sys import exit

screen_width = 960
screen_height = 540
FPS = 60
player_velocity = 4
fruits_left = 2

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer yipeee')

background_img = pygame.image.load("assets/heheh moint 2.png")


def Draw(window, background, player, fruit_display, objects):
    window.blit(background, (0, 0))

    for obj in objects:
        obj.draw()

    player.draw(window)
    window.blit(fruit_display, (0, 0))
    pygame.display.update()


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        self.image = pygame.image.load("assets/milkty t.png")
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.fall_time = 0
        self.jump_speed = -7.1
        self.jumped = False
        self.facing = "left"

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def speed_left(self, vel):
        self.x_vel -= vel

    def speed_right(self, vel):
        self.x_vel += vel

    def jump(self):
        if self.jumped == False:
            self.y_vel = self.jump_speed
            self.jumped = True

    def loop(self, fps):
        self.y_vel += min(2, self.fall_time / FPS * 1)
        self.fall_time += 1

        self.move(self.x_vel, self.y_vel)

    def landed(self):
        self.fall_time = 0
        self.y_vel = 0
        self.jumped = False

    def hit_head(self):
        self.y_vel = 2

    def draw(self, surface):
        if self.facing == "left":
            surface.blit(self.image, self.rect)
        elif self.facing == "right":
            surface.blit(pygame.transform.flip(self.image, False, True),
                         self.rect)

        if handle_keys(player, current_level)[pygame.K_LEFT]:
            surface.blit(self.image, self.rect)
            self.facing = "left"
        if handle_keys(player, current_level)[pygame.K_RIGHT]:
            surface.blit(pygame.transform.flip(self.image, False, True),
                         self.rect)
            self.facing = "right"


class Object(pygame.sprite.Sprite):

    def __init__(self, x, y, width=96, height=48):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/GRASS.png"), (width, height))
        self.rect = self.image.get_rect(left=x, top=y)

    def draw(self):
        screen.blit(self.image, self.rect)


class Collectible(pygame.sprite.Sprite):

    def __init__(self, x, y, sprite):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(f"assets/{sprite}.png"), (50, 50))
        self.rect = self.image.get_rect(left=x, top=y)

    def draw(self):
        screen.blit(self.image, self.rect)


class Lava(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(f"assets/lava.png"), (width, height))
        self.rect = self.image.get_rect(left=x, top=y)

    def draw(self):
        screen.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, left_bound, right_bound, facing="left"):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/shroomers t.png"), (45, 45))
        self.rect = self.image.get_rect(left=x, top=y)
        self.direction = facing
        self.left_bound = left_bound
        self.right_bound = right_bound

    def move(self):
        if self.direction == "left":
            if self.rect.x >= self.left_bound:
                self.rect.x -= 2
            else:
                self.direction = "right"

        else:
            if self.rect.right <= self.right_bound:
                self.rect.right += 2
            else:
                self.direction = "left"

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


#collision
def handle_verical_collision(player, objects, dy):
    obj = pygame.sprite.spritecollideany(player, objects)
    if obj:
        if isinstance(obj, Collectible):
            global fruits_left
            fruits_left -= 1
            obj.kill()

        elif isinstance(obj, Lava):
            lose()

        elif isinstance(obj, Enemy):
            lose()

        elif dy > 0:
            player.rect.bottom = obj.rect.top
            player.landed()

        elif dy < 0:
            if player.rect.bottom > obj.rect.bottom:
                player.rect.top = obj.rect.bottom
                player.hit_head()


def handle_Horizontal_collision(player, objects, dx):
    player.move(dx, 0)
    obj = pygame.sprite.pygame.sprite.spritecollideany(player, objects)
    player.move(-dx, 0)
    return obj


def handle_keys(player, objects):
    keys = pygame.key.get_pressed()

    collidingLeft = handle_Horizontal_collision(player, objects,
                                                -player_velocity)
    collidingRight = handle_Horizontal_collision(player, objects,
                                                 player_velocity)

    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        if isinstance(collidingLeft, Collectible) or isinstance(
                collidingLeft, Lava):
            player.speed_left(player_velocity)
        elif not collidingLeft:
            player.speed_left(player_velocity)
    if keys[pygame.K_RIGHT]:
        if isinstance(collidingRight, Collectible) or isinstance(
                collidingRight, Lava):
            player.speed_right(player_velocity)
        elif not collidingRight:
            player.speed_right(player_velocity)
    if keys[pygame.K_UP]:
        player.jump()

    handle_verical_collision(player, objects, player.y_vel)

    return keys


def check_win():
    global fruits_left
    global level

    if fruits_left == 0:

        if level == level_1:
            level = level_2.copy()
        elif level == level_2:
            level = level_3.copy()
        elif level == level_3:
            level = level_1.copy()

            font = pygame.font.Font(None, 36)
            text = font.render("Fruits Left: 0", True, (0, 0, 0))
            Draw(screen, background_img, player, text, current_level)

            font = pygame.font.SysFont("comicsansms", 115)
            text = font.render("You win!", True, (123, 5, 32))
            text_rect = text.get_rect(center=(screen_width / 2,
                                              screen_height / 2 - 50))
            screen.blit(text, text_rect)

            font = pygame.font.SysFont("opensans", 26)
            text = font.render("Click Anywhere To Restart, or just leave...",
                               True, (236, 127, 153))
            text_rect = text.get_rect(center=(screen_width / 2,
                                              screen_height / 2 + 50))
            screen.blit(text, text_rect)

            ended = True
            while ended:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONUP:
                        player.rect.x = 20
                        player.rect.y = 426
                        fruits_left = 2
                        current_level.empty()
                        current_level.add(level)
                        Draw(screen, background_img, player, text,
                             current_level)
                        ended = False

                pygame.display.update()

        font = pygame.font.Font(None, 36)
        text = font.render("Fruits Left: 0", True, (0, 0, 0))
        Draw(screen, background_img, player, text, current_level)

        font = pygame.font.SysFont("comicsansms", 115)
        text = font.render("Next Level?", True, (123, 5, 32))
        text_rect = text.get_rect(center=(screen_width / 2,
                                          screen_height / 2 - 50))
        screen.blit(text, text_rect)

        font = pygame.font.SysFont("opensans", 26)
        text = font.render("Click Anywhere To Continue", True, (236, 127, 153))
        text_rect = text.get_rect(center=(screen_width / 2,
                                          screen_height / 2 + 50))
        screen.blit(text, text_rect)

        ended = True
        while ended:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    player.rect.x = 20
                    player.rect.y = 426
                    fruits_left = 2
                    current_level.empty()
                    current_level.add(level)
                    Draw(screen, background_img, player, text, current_level)
                    ended = False

            pygame.display.update()


def lose():
    global fruits_left
    lost = True

    font = pygame.font.SysFont("comicsansms", 115)
    text = font.render("You Died", True, (123, 5, 32))
    text_rect = text.get_rect(center=(screen_width / 2,
                                      screen_height / 2 - 50))
    screen.blit(text, text_rect)

    font = pygame.font.SysFont("opensans", 26)
    text = font.render("Click Anywhere To Restart", True, (236, 127, 153))
    text_rect = text.get_rect(center=(screen_width / 2,
                                      screen_height / 2 + 50))
    screen.blit(text, text_rect)

    while lost:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lost = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                player.rect.x = 20
                player.rect.y = 426
                lost = False
                fruits_left = 2
                current_level.empty()
                current_level.add(level)
                Draw(screen, background_img, player, text, current_level)

        pygame.display.update()


level_1 = [
    Object(120, screen_height - 48 * 3, 288, 48),
    Object(120 + 96 * 5 - 20, 340),
    Object(0, screen_height - 48, 960, 48),
    Object(864, 310),
    Collectible(900, 229, "melon t"),
    Collectible(200, 250, "rasp t"),
    Lava(-200, 570, 1360, 1),
    Enemy(240, 351, 120, 412),
    Enemy(460, 447, 412, 960)
]

level_2 = [
    Lava(-200, 520, 1360, 20),
    Object(0, 492, 100, 48),
    Object(200, 430, 300),
    Enemy(250, 385, 200, 350),
    Enemy(400, 385, 350, 500, "right"),
    Object(550, 380, 300),
    Enemy(600, 335, 550, 700),
    Enemy(755, 335, 700, 850, "right"),
    Object(910, 305, 40, 40),
    Collectible(850, 280, "melon t"),
    Object(700, 230, 20, 20),
    Object(100, 150, 500),
    Enemy(175, 107, 100, 275),
    Enemy(350, 107, 275, 425),
    Enemy(425, 107, 425, 600, "right"),
    Collectible(0, 30, "rasp t")
]

level_3 = [
    Lava(-200, 570, 1360, 1),
    Object(0, 520, 100, 20),
    Object(100, 480, 200, 60),
    Enemy(160, 435, 100, 300),
    Object(300, 440, 200, 100),
    Enemy(360, 395, 300, 500),
    Object(500, 400, 100, 140),
    Lava(600, 440, 250, 100),
    Object(850, 400, 110, 140),
    Collectible(900, 270, "melon t"),
    Object(700, 300, 150),
    Object(400, 250, 150),
    Enemy(460, 205, 400, 550),
    Object(100, 200, 150),
    Object(375, 60, 100),
    Object(475, 84, 200, 24),
    Lava(475, 70, 200, 14),
    Object(675, 60, 100),
    Object(170, 100, 30, 30),
    Collectible(900, 50, "rasp t")
]

level = level_1.copy()

current_level = pygame.sprite.Group()
current_level.add(*level)

player = Player(20, 426, 41, 66)
clock = pygame.time.Clock()

running = True


def make_grid(screen_width, screen_height, cell_size):
    """Return a list of pairs of grid line points."""
    lines = []
    for x in range(0, screen_width, cell_size):
        lines.append(((x, 0), (x, screen_height)))
    for y in range(0, screen_height, cell_size):
        lines.append(((0, y), (screen_width, y)))

    for p1, p2 in lines:
        pygame.draw.line(screen, pygame.Color("gray80"), p1, p2)


while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()

    fruit_display = f"Fruits Left: {fruits_left}"

    font = pygame.font.Font(None, 36)
    text = font.render(fruit_display, True, (0, 0, 0))

    player.loop(FPS)
    handle_keys(player, current_level)
    current_level.update()

    for obj in current_level:
        if isinstance(obj, Enemy):
            obj.move()

    Draw(screen, background_img, player, text, current_level)
    check_win()
