import pygame
import math
from random import randint, choice, random

# todo: out of bounds (player)
# todo: new enemies
# todo: fix inconsistent/not precise values (eventually), such as height of floor calculations for jumping
# todo: (eventually), the shotgun's sprite's weird shape causes collision issues, namely with the boundaries of the window
# todo: powerups: ideas in ignore.txt
pygame.init()
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
mouse_pos = (0, 0)
game_active = True
# Load images
background = pygame.image.load('assets/img/city_night_1.png').convert_alpha()
#background = pygame.image.load('assets/img/weird_dungon.png').convert_alpha()
background_surf = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background_surf.get_rect()
ground = pygame.image.load('assets/img/ground-shane-1-wide.png')
ground_surf = pygame.transform.scale_by(ground, 4)
ground_rect = ground_surf.get_rect(midbottom=(WIDTH // 2, HEIGHT))
player_bullet_img = pygame.image.load('assets/img/bullet2.png').convert_alpha()
enemy_bullet_img = pygame.image.load('assets/img/enemy_bullet_circle1.png').convert_alpha()
shotgun_img = pygame.image.load('assets/img/shotgun_right.png').convert_alpha()
shotgun_img_yellow = pygame.image.load('assets/img/shotgun_yellow.png').convert_alpha()
shotgun_img_red = pygame.image.load('assets/img/shotgun_red.png').convert_alpha()
mob_1_img = pygame.image.load('assets/img/drone_ball.png').convert_alpha()
tank_guy_img1 = pygame.image.load('assets/img/tank_guy_red1.png').convert_alpha()
tank_guy_img1 = pygame.transform.scale_by(tank_guy_img1, 4)
tank_guy_img2 = pygame.image.load('assets/img/tank_guy_red2.png').convert_alpha()
tank_guy_img2 = pygame.transform.scale_by(tank_guy_img2, 4)
tank_guy_img3 = pygame.image.load('assets/img/tank_guy_red3.png').convert_alpha()
tank_guy_img3 = pygame.transform.scale_by(tank_guy_img3, 4)
tank_guy_img4 = pygame.image.load('assets/img/tank_guy_red4.png').convert_alpha()
tank_guy_img4 = pygame.transform.scale_by(tank_guy_img4, 4)
tank_guy_angle_img1 = pygame.image.load('assets/img/tank_guy_angle1.png').convert_alpha()
tank_guy_angle_img1 = pygame.transform.scale_by(tank_guy_angle_img1, 4)
tank_guy_angle_img2 = pygame.image.load('assets/img/tank_guy_angle2.png').convert_alpha()
tank_guy_angle_img2 = pygame.transform.scale_by(tank_guy_angle_img2, 4)
tank_guy_angle_img3 = pygame.image.load('assets/img/tank_guy_angle3.png').convert_alpha()
tank_guy_angle_img3 = pygame.transform.scale_by(tank_guy_angle_img3, 4)
tank_guy_angle_img4 = pygame.image.load('assets/img/tank_guy_angle4.png').convert_alpha()
tank_guy_angle_img4 = pygame.transform.scale_by(tank_guy_angle_img4, 4)
heart_red = pygame.image.load('assets/img/heart1.png').convert_alpha()
heart_red_empty = pygame.image.load('assets/img/heart1_fade.png').convert_alpha()
rapid_powerup_img = pygame.image.load('assets/img/rapidfire_notext.png')
rapid_powerup_img = pygame.transform.scale_by(rapid_powerup_img, 2.5)
#bullet_img = pygame.image.load('assets/img/bullet1_enemy.png').convert_alpha()

# timersa
pygame.time.set_timer(mouse_timer, 10)

# Remember: These variables are also in reset()
spawn_timer_flying = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_timer_flying, randint(250, 500))

spawn_timer_shooting = pygame.USEREVENT + 3
pygame.time.set_timer(spawn_timer_shooting, randint(2000, 10000))
#pygame.time.set_timer(spawn_timer_shooting, 500)

blink_timer = pygame.USEREVENT + 4
pygame.time.set_timer(blink_timer, 100)

# GUI
main_font = pygame.font.Font('assets/GUI/HopeGold.ttf', 64)
# hearts are created elsewhere
# gameplay params
score = 0
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Render
        self.shotgun_library = [shotgun_img, shotgun_img_yellow, shotgun_img_red]
        self.current_frame = 0  # defaults to shotgun_img (index 0 of shotgun_library)
        self.last_frame = 0
        self.current_shotgun_img = pygame.transform.scale_by(self.shotgun_library[self.current_frame], 3)
        self.image = self.current_shotgun_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.last_blink = 0
        # variables for math crap
        self.player_speed = 0
        self.player_max_speed = 20
        self.player_acceleration = 1
        self.gravity = 0
        # reload time
        self.can_shoot = True
        self.shot_delay = 300
        self.last_shot = 0
        # jump time
        self.can_jump = True
        self.jump_delay = 200
        self.jump_counter = 2
        self.last_jump = 0
        # for i-frames
        self.is_invul = False
        self.i_frames = 3000
        self.now_invul = 0
        # for powerups
        self.has_powerup = False
        self.powerup_pickup_time = 0
        self.powerup_duration = 5000
        self.powerup_type = 'rapidfire'
        # params, bullet spread is in bullet class
        self.health = 3
        self.bullet_count = 5  # 5 default, make sure this is an odd number, huge number = cool explosion lol
        self.jump_height = 25
        self.multi_shot_counter = 0



    def point(self):
        # shotgun points at mouse
        global mouse_pos
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        angle = math.atan2(mouse_pos[1] - self.rect.centery, mouse_pos[0] - self.rect.centerx)
        # mouse_pos[y] and mouse_pos[x]
        #global angle_degrees
        self.angle_degrees = math.degrees(angle)
        if mouse_pos[0] < self.rect.x:  # flips if on left side
            # todo: I'm not a fan of the way this is rendered
            flipped_image = pygame.transform.flip(pygame.transform.scale_by(self.shotgun_library[self.current_frame], 3), flip_x=False, flip_y=True)
            self.image = pygame.transform.rotate(flipped_image, -self.angle_degrees)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:  # no flip
            self.image = pygame.transform.rotate(pygame.transform.scale_by(self.shotgun_library[self.current_frame], 3), -self.angle_degrees)
            self.rect = self.image.get_rect(center=self.rect.center)  # Update the rect
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_speed = max(-self.player_max_speed, self.player_speed - self.player_acceleration)
        if keys[pygame.K_d]:
            self.player_speed = min(self.player_max_speed, self.player_speed + self.player_acceleration)
        self.rect.x += self.player_speed
        # ^ moves player
        if keys[pygame.K_s]:
            # goes down faster if holding S
            self.gravity += 1.5
        if keys[pygame.K_w] and self.jump_counter == 0:
            # todo: maybe implement W key slowing down your fall
            #self.gravity -= 0.9
            pass
            # goes down slightly slower if holding W
        if keys[pygame.K_SPACE]:
            self.jump()
        if self.player_speed != 0:
            # "Friction"
            self.player_speed -= 0.5 * self.player_speed / abs(self.player_speed)
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= (HEIGHT - 50):
            self.rect.bottom = HEIGHT - 50
    def shoot(self, type):
        if self.can_shoot:
            self.multi_shot_counter = 0
            # create bullets, 5 for shotgun
            # todo: huge numbers make explosion lol
            if type == 1:
                for i in range(1, (self.bullet_count + 1)):
                    bullet.add(Bullet(i))
                    self.last_shot = pygame.time.get_ticks()
            if type == 2:
                # doubles amount of bullets
                for i in range(1, ((self.bullet_count * 2) + 1)):
                    bullet.add(Bullet(i))
                    self.last_shot = pygame.time.get_ticks() + 750  # longer delay
            self.can_shoot = False
    def jump(self):
        if self.can_jump and self.rect.y > 25:
                if pygame.Rect.colliderect(self.rect, ground_rect) or self.jump_counter > 0:
                    self.gravity = -self.jump_height
                    self.last_jump = pygame.time.get_ticks()
                    self.can_jump = False
                    if self.rect.y != (HEIGHT - ground_surf.get_height()):
                        self.jump_counter -= 1
    def checks(self):
        # works out timing for jumps/shots/i-frames, and refreshes jumps upon landing
        if not self.can_shoot and current_time - self.last_shot >= self.shot_delay:
            self.can_shoot = True
        if not self.can_jump and current_time - self.last_jump >= self.jump_delay:
            self.can_jump = True
        if self.is_invul and current_time - self.now_invul >= self.i_frames:
            self.is_invul = False
        if pygame.Rect.colliderect(self.rect, ground_rect):
            # landing refreshes jumps
            self.jump_counter = 2
        if self.has_powerup and current_time - self.powerup_pickup_time > self.powerup_duration:
            self.has_powerup = False
            self.reset()
            # removes powerup after set duration (powerup_duration)

    def frames(self):
        # for blinking (i-frames)
        if self.is_invul:
            blink_duration = 150
            if current_time - self.last_blink >= blink_duration:
                self.current_frame = 2 if self.current_frame == self.last_frame else self.last_frame
                self.last_blink = current_time
        else:
            self.current_frame = self.last_frame

    def refresh_jump(self):
        # killing enemies refreshes jump
        if self.jump_counter == 0:
            self.jump_counter = 1

    def powerup(self, powerup_type):
        global score
        # runs ONCE when powerup is picked up
        self.powerup_pickup_time = pygame.time.get_ticks()
        self.powerup_type = powerup_type
        self.has_powerup = True
        pygame.time.set_timer(spawn_timer_flying, 100)
        #pygame.time.set_timer(spawn_timer_shooting, 1000)
        score += 20


    def powerup_active(self):
        # runs when powerup active, ends AUTOMATICALLY after powerup_duration
        if self.powerup_type == 'rapidfire':
            self.current_frame = 1
            self.last_frame = 1
            self.shot_delay = 50

    def reset(self):
        self.player_max_speed = 20
        self.current_frame = 0
        self.last_frame = 0
        self.shot_delay = 300
        pygame.time.set_timer(spawn_timer_flying, randint(400, 500))
        pygame.time.set_timer(spawn_timer_shooting, randint(2000, 10000))

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.frames()
        out_of_bounds(self, 3)
        if self.has_powerup is True:
            self.powerup_active()
        self.checks()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_type):
        super().__init__()
        self.bullet_type = bullet_type
        self.image = pygame.transform.scale_by(player_bullet_img, 0.5)
        self.image = pygame.transform.rotate(self.image, -player.sprite.angle_degrees)
        projectile_pos = pygame.math.Vector2(player.sprite.rect.centerx, player.sprite.rect.centery)
        self.rect = self.image.get_rect(center=projectile_pos)
        self.projectile_speed = 30  # 30 is default
        self.direction = pygame.math.Vector2(mouse_pos) - self.rect.center
        self.bullet_spread = 4  # 4 is default

        if bullet_type == 1:  # flies straight
            self.direction = mouse_pos - self.rect.center
        if bullet_type > 1:
            # bullet type 1 has no skew, others do
            if bullet_type % 2 == 0:
                rotate_amount = ((bullet_type / 2) * self.bullet_spread)
            else:
                rotate_amount = (-((bullet_type - 1) / 2) * self.bullet_spread)
            self.direction.rotate_ip(rotate_amount)

        self.direction.normalize_ip()
        print(self.direction.x)
    def fly(self):
        # movement of bullet
        self.rect.x += self.direction.x * self.projectile_speed
        self.rect.y += self.direction.y * self.projectile_speed


    def update(self):
        # this method runs every tick
        self.out_of_bounds()
        self.fly()
    def out_of_bounds(self):
        # destroy bullet if out of bounds
        if out_of_bounds(self, 1):
            self.kill()
    def destroy(self):
        self.kill()


class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        # todo: consolidate loading sprites
        super().__init__()
        self.library = [mob_1_img]  # can add frames later
        self.current_frame = 0
        self.current_img = pygame.transform.scale_by(self.library[self.current_frame], 4)
        self.flipped_img = pygame.transform.flip(self.current_img, flip_x=True, flip_y=False)
        self.speed_options = [5, 5, 5, 5, 5, 5, 5, 5, 5, 10]
        self.speed = choice(self.speed_options)
        self.image = self.flipped_img
        if enemy_type == 1:
            # enemy comes from left
            self.rect = self.image.get_rect(midbottom= (-100, randint(0, HEIGHT)))
        if enemy_type == 2:
            # enemy comes from the right
            self.rect = self.image.get_rect(midbottom=(WIDTH + 100, randint(0, HEIGHT)))
        if enemy_type == 3:
            # enemy comes from the top
            self.rect = self.image.get_rect(midbottom=(randint(0, WIDTH), -100))


    def destroy(self):
        global score
        if pygame.sprite.spritecollide(self, bullet, True):
            self.kill()
            score += 1
            player.sprite.refresh_jump()
            multi_shot()
        if pygame.sprite.spritecollide(self, player, False):
            self.kill()
            player_take_damage()
    def fly(self):
        # flies toward player and point at them
        player_pos = pygame.math.Vector2(player.sprite.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)
        direction = player_pos - enemy_pos
        self.angle = math.atan2(player_pos[1] - self.rect.centery, player_pos[0] - self.rect.centerx)
        # global angle_degrees
        self.angle_degrees = math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.flipped_img, -self.angle_degrees)
        if direction.length() != 0:
            direction.normalize_ip()
            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed

    def update(self):
        self.fly()
        self.destroy()

class ShootingEnemy(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.library = [tank_guy_img1, tank_guy_img2, tank_guy_img3, tank_guy_img4]  # frames
        self.library_flipped = [pygame.transform.flip(tank_guy_img1, flip_x=True, flip_y=False),
                                pygame.transform.flip(tank_guy_img2, flip_x=True, flip_y=False),
                                pygame.transform.flip(tank_guy_img3, flip_x=True, flip_y=False),
                                pygame.transform.flip(tank_guy_img4, flip_x=True, flip_y=False)]
        self.current_frame = 0  # index of self.library
        self.image = self.library[self.current_frame]
        self.speed = 5
        # main sprite group, stores bullets ^
        self.can_shoot = True
        self.last_shot = 0
        self.shot_delay = 175
        self.alive = True
        # this divisor, used later, is for calculating self.rect.y movement
        self.side = side
        if self.side == 1:
            # right side of screen
            self.rect = self.image.get_rect(midbottom=(WIDTH + 100, HEIGHT - (HEIGHT / 18)))
        if self.side == 2:
            # left side of screen
            self.image = self.library_flipped[self.current_frame]
            self.rect = self.image.get_rect(midbottom=(-100, HEIGHT - (HEIGHT / 18)))


    def destroy(self):
        global score
        if pygame.sprite.spritecollide(self, bullet, True):
            # this is when PLAYER bullet collides with enemy
            self.kill()
            score += 2
            multi_shot()
            player.sprite.refresh_jump()
        if out_of_bounds(self, 2):
            # destroys if off-screen (500 pixels off-screen)
            self.kill()
        if pygame.sprite.collide_rect(self, player.sprite):
            player_take_damage()
            pass

    def shoot(self):  # call this with a type
        if self.can_shoot:
            if self.side == 1:
                # right side
                enemy_bullet.add(EnemyBullet(self.rect.midleft, 0, self.side))
            if self.side == 2:
                # left side
                enemy_bullet.add(EnemyBullet(self.rect.midright, 0, self.side))
            # this self.rect.whatever is passed into EnemyBullet as the "position" argument
            self.last_shot = pygame.time.get_ticks()
            self.can_shoot = False

    def move(self):
        if self.side == 1:
            self.rect.x -= self.speed
        if self.side == 2:
            self.rect.x += self.speed
    def animation(self):
        # cycles through each "frame" in self.library
        self.current_frame += 0.2 # speed
        if self.current_frame >= len(self.library):
            self.current_frame = 0
        if self.side == 1:
            self.image = self.library[int(self.current_frame)]
        if self.side == 2:
            self.image = self.library_flipped[int(self.current_frame)]

    def update(self):
        self.move()
        self.destroy()
        self.shoot()
        self.animation()
        if not self.can_shoot and current_time - self.last_shot >= self.shot_delay:
            # this is for delay between shots
            self.can_shoot = True


class ShootingEnemyAngled(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.library = [tank_guy_angle_img1, tank_guy_angle_img2, tank_guy_angle_img3, tank_guy_angle_img4]  # frames
        self.library_flipped = [pygame.transform.flip(tank_guy_angle_img1, flip_x=True, flip_y=False),
                                pygame.transform.flip(tank_guy_angle_img2, flip_x=True, flip_y=False),
                                pygame.transform.flip(tank_guy_angle_img3, flip_x=True, flip_y=False),
                                pygame.transform.flip(tank_guy_angle_img4, flip_x=True, flip_y=False)]
        self.current_frame = 0  # index of self.library
        self.image = self.library[self.current_frame]
        self.speed = 5
        # main sprite group, stores bullets ^
        self.can_shoot = True
        self.last_shot = 0
        self.shot_delay = 175
        self.alive = True
        # this divisor, used later, is for calculating self.rect.y movement
        self.side = side
        if self.side == 1:
            # right side of screen
            self.rect = self.image.get_rect(midbottom=(WIDTH + 100, HEIGHT - (HEIGHT / 18)))
        if self.side == 2:
            # left side of screen
            self.image = self.library_flipped[self.current_frame]
            self.rect = self.image.get_rect(midbottom=(-100, HEIGHT - (HEIGHT / 18)))



    def destroy(self):
        global score
        if pygame.sprite.spritecollide(self, bullet, True):
            # this is when PLAYER bullet collides with enemy
            self.kill()
            score += 2
            multi_shot()
            player.sprite.refresh_jump()
        if out_of_bounds(self, 2):
            # destroys if off-screen
            self.kill()
        if pygame.sprite.collide_rect(self, player.sprite):
            player_take_damage()
            pass

    def shoot(self):  # call this with a type
        if self.can_shoot:
            if self.side == 1:
                # right side
                enemy_bullet.add(EnemyBullet(self.rect.center,1, self.side))
            if self.side == 2:
                # left side
                enemy_bullet.add(EnemyBullet(self.rect.center,1, self.side))
            # this self.rect.whatever is passed into EnemyBullet as the "position" argument
            self.last_shot = pygame.time.get_ticks()
            self.can_shoot = False

    def move(self):
        if self.side == 1:
            self.rect.x -= self.speed
        if self.side == 2:
            self.rect.x += self.speed
    def animation(self):
        # cycles through each "frame" in self.library
        self.current_frame += 0.2 # speed
        if self.current_frame >= len(self.library):
            self.current_frame = 0
        if self.side == 1:
            self.image = self.library[int(self.current_frame)]
        if self.side == 2:
            self.image = self.library_flipped[int(self.current_frame)]

    def update(self):
        self.move()
        self.destroy()
        self.shoot()
        self.animation()
        if not self.can_shoot and current_time - self.last_shot >= self.shot_delay:
            # this is for delay between shots
            self.can_shoot = True
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, position, shot_angle, side):
        super().__init__()
        self.image = enemy_bullet_img
        self.rect = self.image.get_rect(center=position)
        self.projectile_speed = 10
        self.side = side
        self.angled = shot_angle
        # 1 will be straight shooter, 2 will be angled

    def update(self):
        # flight
        self.fly()
        self.collision()
    def collision(self):
        # destroy bullet if out of bounds
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()
        # destroy bullet if hits player + player takes damage
        if pygame.sprite.collide_rect(self, player.sprite):
            player_take_damage()
    def fly(self):
        if self.angled == 0:
            # straight shooting
            if self.side == 1:
                # right side
                self.rect.x -= self.projectile_speed
                self.rect.y -= 0
            if self.side == 2:
                # left side
                self.rect.x += self.projectile_speed
                self.rect.y -= 0
        if self.angled == 1:
            if self.side == 1:
                # right side
                self.rect.x -= self.projectile_speed
                self.rect.y -= 3
            if self.side == 2:
                # left side
                self.rect.x += self.projectile_speed
                self.rect.y -= 3
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, ob_type):
        super().__init__()
        if ob_type == 1:
            pass

class Heart(pygame.sprite.Sprite):
    def __init__(self, heart_type):
        super().__init__()
        # Render
        heart_red_resize = pygame.transform.scale_by(heart_red, 3)
        heart_red_empty_resize = pygame.transform.scale_by(heart_red_empty, 3)
        self.heart_library = [heart_red_resize, heart_red_empty_resize]
        # todo: heart_types can be consolidated to allow for more hearts later on (like with power-ups)
        if heart_type == 1:  # left heart
            self.image = self.heart_library[0]
            self.rect = self.image.get_rect(center=((WIDTH // 2) - 50, 125))
        if heart_type == 2:  # middle heart
            if player.sprite.health >= 2:
                self.image = self.heart_library[0]
            else:
                self.image = self.heart_library[1]
            self.rect = self.image.get_rect(center=(WIDTH // 2, 125))
        if heart_type == 3:  # right heart
            if player.sprite.health >= 3:
                self.image = self.heart_library[0]
            else:
                self.image = self.heart_library[1]
            self.rect = self.image.get_rect(center=((WIDTH // 2) + 50, 125))

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, powerup_type):
        super().__init__()
        self.powerup_type = powerup_type
        if self.powerup_type == 'rapidfire':
            self.speed = 5
            self.visual = rapid_powerup_img
            self.side = randint(1, 2)
            if self.side == 1:
                # right
                self.starting_position = (WIDTH + 100, 250)
            if self.side == 2:
                self.starting_position = (-100, 250)
        self.image = self.visual
        self.rect = self.image.get_rect(center = self.starting_position)

    def fly(self):
        if self.side == 1:
            # right
            self.rect.x -= self.speed
        if self.side == 2:
            self.rect.x += self.speed
    def collision(self):
        if pygame.sprite.spritecollide(self, player, False):
            player.sprite.powerup(self.powerup_type)
            self.kill()
        if out_of_bounds(self, 2):
            self.kill()

    def update(self):
        self.collision()
        self.fly()



# INSTANTIATE STUFF
# player
player = pygame.sprite.GroupSingle(Player())
# bullet
bullet = pygame.sprite.Group()
# enemies
flying_enemies = pygame.sprite.Group()
# heart
heart = pygame.sprite.Group()
# shooting enemies
shooting_enemies = pygame.sprite.Group()
shooting_enemies_angled = pygame.sprite.Group()
# bullet fired by enemies
enemy_bullet = pygame.sprite.Group()
# power ups
power_ups = pygame.sprite.Group()


for i in range(1, 4):
    heart.add(Heart(i))

power_ups.add(PowerUp('rapidfire'))

def player_take_damage():
    global game_active
    if player.sprite.is_invul is False:
        if player.sprite.health == 1:
            game_active = False  # end game
        else:
            flying_enemies.empty()
            # todo: this destroys all enemies on collision, might be a cool feature? idk
            player.sprite.now_invul = pygame.time.get_ticks()
            player.sprite.is_invul = True
            player.sprite.health -= 1
            player.sprite.has_powerup = False
            update_hearts()
            game_active = True  # keep game going


def multi_shot():
    global score
    # this is to be called whenever a collision has occurred
    # todo: more interesting rewards for multi-shots
    if player.sprite.can_shoot is False:
        player.sprite.multi_shot_counter += 1
        if player.sprite.multi_shot_counter > 1:
            score += 2
        if player.sprite.multi_shot_counter == 3:
            score += 5
        if player.sprite.multi_shot_counter == 5:
            score += 20
def update_hearts():
    heart.empty()
    for i in range(1, 4):
        heart.add(Heart(i))


def out_of_bounds(object_to_check, out_of_bounds_type):
    # checks if given thing is out of bounds, simply call it with a (self)
    # fixme: weird bugginess with y coords
    # type 1 is more strict
    # type 2 has padding
    # type 3 doesn't return true/false, but rather forces object to stay in bounds (strictly)
    padding = 500
    if out_of_bounds_type == 1:
        if (object_to_check.rect.x < 0 or object_to_check.rect.x > WIDTH
                or object_to_check.rect.y < 0 or object_to_check.rect.y > HEIGHT):
            return True
        else:
            return False
    if out_of_bounds_type == 2:
        if (object_to_check.rect.x < (-padding) or object_to_check.rect.x > (WIDTH + padding)
                or object_to_check.rect.y < -padding or object_to_check.rect.y > (HEIGHT + padding)):
            return True
        else:
            return False
    if out_of_bounds_type == 3:
        if object_to_check.rect.x < 0:
            object_to_check.rect.x = 0
        if object_to_check.rect.x > WIDTH:
            object_to_check.rect.x = WIDTH
        if object_to_check.rect.y < 0:
            object_to_check.rect.y = 0
        if object_to_check.rect.y > HEIGHT:
            object_to_check.rect.y = HEIGHT

def get_powerup(powerup_type):
    player.sprite.has_powerup = True
    power_up_duration = 2000
    time_at_pickup = pygame.time.get_ticks()
    if powerup_type == 1:
        if current_time - time_at_pickup <= power_up_duration:
            player.sprite.current_frame = 1
            player.sprite.last_frame = 1

        else:
            player.sprite.current_frame = 0
            player.sprite.last_frame = 0


while running:
    # Main Game loop
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if game_active:
            if event.type == pygame.QUIT:
                running = False
            if event.type == mouse_timer:
                player.sprite.point()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.sprite.shoot(1)
                if event.button == 3:
                    player.sprite.shoot(2)

            if event.type == spawn_timer_flying:
                # spawns enemies
                flying_enemies.add(FlyingEnemy(randint(1, 3)))
                pass
            if event.type == spawn_timer_shooting:
                shooter_type = randint(1,2)
                shooting_enemy_types = (1, 1, 1, 2)
                # ^ this is for the random.choice method
                # 1 = straight shooter, 2 is angled
                if shooter_type == 1:
                    shooting_enemies.add(ShootingEnemy(randint(1, 2)))
                    pass
                    # 1 or 2 determines side of spawning
                if shooter_type == 2:
                    shooting_enemies_angled.add(ShootingEnemyAngled(choice(shooting_enemy_types)))
                    pass
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                # reset the game
                game_active = True
                score = 0
                player.sprite.health = 3

    if game_active:
        # Main game
        # Render
        screen.blit(background_surf, (0, 0))
        screen.blit(ground_surf, ground_rect)
        score_text = main_font.render("SCORE : " + str(score), True, (220, 255, 220))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 50))

        player.draw(screen)
        player.update()

        bullet.draw(screen)
        bullet.update()

        flying_enemies.draw(screen)
        flying_enemies.update()

        shooting_enemies.draw(screen)
        shooting_enemies.update()

        shooting_enemies_angled.draw(screen)
        shooting_enemies_angled.update()

        enemy_bullet.draw(screen)
        enemy_bullet.update()

        power_ups.draw(screen)
        power_ups.update()

        heart.draw(screen)
    else:
        # this happens if player_collision returns false
        # End Screen
        for event in pygame.event.get():
            if game_active:
                if event.type == pygame.QUIT:
                    running = False
        heart.empty()
        bullet.empty()
        flying_enemies.empty()
        shooting_enemies.empty()
        enemy_bullet.empty()
        # empty everything to really ensure there's no memory leaks
        screen.fill('darkorchid4')
        score_text = main_font.render("SCORE : " + str(score), True, (200, 200, 200))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))


    # Update display
    pygame.display.flip()
    clock.tick(60) # fps

pygame.quit()
