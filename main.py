import random
from pgzero.actor import Actor
import pgzrun

WIDTH = 1200
HEIGHT = 900

class Ship:
    def __init__(self):
        self.actor = Actor("ship.png")  # Gemimizin resmi
        self.actor.midbottom = (WIDTH / 2, HEIGHT)
        self.speed = 5

    def move(self, keys):
        if keys.left and self.actor.left > 0:
            self.actor.x -= self.speed
        if keys.right and self.actor.right < WIDTH:
            self.actor.x += self.speed
        if keys.up and self.actor.top > 0:
            self.actor.y -= self.speed
        if keys.down and self.actor.bottom < HEIGHT:
            self.actor.y += self.speed

class Laser:
    def __init__(self, x, y):
        self.actor = Actor("laser.png")
        self.actor.midbottom = (x, y)
        self.speed = 10
        self.active = True

    def move(self):
        if self.active:
            self.actor.y -= self.speed
            if self.actor.y < 0:
                self.active = False

class Meteor:
    def __init__(self):
        self.image = "m" + str(random.randint(0, 7)) + ".png"
        self.actor = Actor(self.image, (random.randint(40, WIDTH - 40), 0))
        self.speed = random.choice([3, 4, 5, 6, 7, 8])

    def move(self):
        self.actor.y += self.speed
        if self.actor.y > HEIGHT:
            self.reset()

    def reset(self):
        self.actor.y = 0
        self.actor.x = random.randint(40, WIDTH - 40)
        self.actor.image = "m" + str(random.randint(0, 7)) + ".png"

ship = Ship()
lasers = []
meteors = [Meteor() for _ in range(5)]

score = 0
lives = 4
main_menu = True
game_over = False
music_playing = False
sound_on = True
background = Actor("uzay_arka_plan.png", (WIDTH // 2, HEIGHT // 2)) #oyunumuzun arkaplan resimi. buradan 1200x900 olan çogu resm eklenir

# Ateş etme kontrolü
can_fire = True  # en basit time olmadan cozum

def allow_fire():
    global can_fire
    can_fire = True  # ynsden ates etmeye izin ver

# Butonlar
restart_button = Actor("button_re.png", (WIDTH // 2, HEIGHT // 2 + 200))
start_button = Actor("button_start.png", (WIDTH // 2, HEIGHT // 2))
volume_button = Actor("button_volume.png", (WIDTH // 2, HEIGHT // 2 + 100))
exit_button = Actor("button_exit.png", (WIDTH // 2, HEIGHT - 100))

def draw():
    global score, lives, main_menu, game_over
    background.draw()

    if main_menu:
        start_button.draw()
        volume_button.draw()
        exit_button.draw()

        # Butonların textleri ekledim
        screen.draw.text("START", center=(start_button.x, start_button.y),
                         fontsize=50, color="white")
        screen.draw.text("VOLUME", center=(volume_button.x, volume_button.y),
                         fontsize=50, color="white")
        screen.draw.text("EXIT", center=(exit_button.x, exit_button.y),
                         fontsize=50, color="white")

    elif lives > 0:
        ship.actor.draw()
        for laser in lasers:
            laser.actor.draw()
        for meteor in meteors:
            meteor.actor.draw()

        # Skor ve hak bilgileri yazdıralım
        screen.draw.text(
            f"Score: {score}", topleft=(10, 10), fontsize=40,
            color="white"
        )
        screen.draw.text(
            f"Lives: {lives}", topleft=(10, 60), fontsize=40,
            color="white"
        )

    else:
        game_over = True
        restart_button.draw()
        screen.draw.text("RESTART", center=(restart_button.x, restart_button.y),
                         fontsize=50, color="white")

def update():
    global score, lives, main_menu, game_over, can_fire

    if main_menu:
        return

    if not game_over:
        ship.move(keyboard)

        # Space tuşuna basıldığında ve ateş etmeye izin varsa
        if keyboard.space and can_fire:
            lasers.append(Laser(ship.actor.x, ship.actor.top))
            can_fire = False  # Tekrar ateş etmeyi engelle
            clock.schedule(allow_fire, 0.4)  # 0.4 saniye sonra ateş etmeye izin ver

        for laser in lasers:
            laser.move()
            for meteor in meteors:
                if meteor.actor.colliderect(laser.actor) and laser.active:
                    score += 10
                    meteor.reset()
                    laser.active = False  # Lazer yok olur

        lasers[:] = [l for l in lasers if l.active]

        for meteor in meteors:
            meteor.move()
            if meteor.actor.colliderect(ship.actor):
                lives -= 1
                meteor.reset()

def on_mouse_down(pos):
    global main_menu, music_playing, sound_on
    if main_menu and exit_button.collidepoint(pos):
        sys.exit()
    elif game_over and restart_button.collidepoint(pos):
        reset_game()
    elif main_menu and start_button.collidepoint(pos):
        main_menu = False
        if not music_playing:
            music.play("background_music") #arkaplan muzigi eklendi
            music_playing = True
    elif volume_button.collidepoint(pos):
        sound_on = not sound_on
        music.set_volume(0.5 if sound_on else 0)

def reset_game():
    global score, lives, main_menu, game_over, lasers
    score = 0
    lives = 4
    main_menu = True
    game_over = False
    lasers = []
    ship.actor.midbottom = (WIDTH / 2, HEIGHT)
    for meteor in meteors:
        meteor.reset()

pgzrun.go()
