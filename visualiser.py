import pygame
import math
from joblib import dump, load
import pandas as pd
from sklearn.linear_model import LinearRegression

model = load('model.joblib')
X_test = load('x_test.joblib')
X_test.reset_index(drop=True, inplace=True)
Y_test = load('y_test.joblib')
Y_test.reset_index(drop=True, inplace=True)
Y_pred = model.predict(X_test)

# projectile = simulation.Projectile(spawn_x=6,spawn_y=6,speed=)
# engine = simulation.Engine(projectile=simulation.Projectile(spawn_x=))
#PyGame Configuration
size = 500
rows = 10
status = True

def set_settings():
    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode(size=(size, size))
    pygame.display.set_caption("Aim trainer")
    display.fill((255, 255, 255))
    return display, clock

class Thief():
    def __init__(self,x_cord, y_cord, speed):
        super().__init__()
        self.x = x_cord + 12.5
        self.y = y_cord - 12.5
        self.width = 25
        self.height = 25
        self.speed = speed * 0.1
        self.diff_x = None
        self.diff_y = None

    def move(self, chest_x, chest_y):
        self.diff_x = chest_x - self.x
        self.diff_y = chest_y - self.y
        if self.diff_x == 0:
            self.tang=1
        else:
            self.tang = abs(self.diff_y / self.diff_x)
        if self.diff_y > 0:
            self.y += self.tang*self.speed
        elif self.diff_y < 0:
            self.y -= self.tang*self.speed
        if self.diff_x > 0:
            self.x += self.speed
        elif self.diff_x < 0:
            self.x -= self.speed

class Turrel:
    def __init__(self,x_cord, y_cord):
        self.x = x_cord
        self.y = y_cord
        self.width = 50
        self.height = 50

class Bullet:
    def __init__(self,x_cord, y_cord, angle, speed):
        self.x = x_cord
        self.y = y_cord
        self.radius = 5
        self.color = (0,255,0)
        self.speed = speed * 0.1
        self.angle = angle
        self.radians = math.radians(angle)
        self.cos = math.cos(self.radians)
        self.sin = math.sin(self.radians)
        self.tang = math.tan(self.angle)

    def shoot(self):
        self.x += self.cos * self.speed
        self.y -= self.sin * self.speed * -1

class Tresure():
    def __init__(self,x_cord, y_cord):
        self.x = x_cord
        self.y = y_cord
        self.width = 50
        self.height = 50

def draw_grid(grid, size, rows):
    distanceBtwRows = size // rows
    x = 0
    y = 0
    for i in range(rows):
        x += distanceBtwRows
        y += distanceBtwRows
        pygame.draw.line(surface=grid, color=(0, 0, 0), start_pos=(x,0), end_pos=(x,size))
        pygame.draw.line(surface=grid, color=(0, 0, 0), start_pos=(0, y), end_pos=(size, y))


def main(bullet_x,bullet_y,thief_spawn_x,thief_spawn_y,bullet_speed,thief_speed,bullet_angle):
    status = True
    # Settings
    display, clock = set_settings()
    run = True
    tick_count = 0
    unit = 50

    # Values transformation to pixel units:
    bullet_cord_x = bullet_x * unit
    bullet_cord_y = bullet_y * unit
    thief_cord_x = thief_spawn_x * unit
    thief_cord_y = thief_spawn_y * unit
    bullet_speed_pixels = bullet_speed * unit
    thief_speed_pixels = thief_speed * unit

    # Object initialization
    turrel = Turrel(bullet_cord_x, bullet_cord_y)
    chest = Tresure(450, 450)
    thief = Thief(thief_cord_x, thief_cord_y, thief_speed_pixels)
    bullet = Bullet(bullet_cord_x, bullet_cord_y, bullet_angle, bullet_speed_pixels)

    while run == True:
        #If 10 ticks pass, we launch another simulation
        tick_count += 1
        if tick_count == 6 * 10:
            run = False

        # Setting quit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False


        # Filling background to erase old objects
        display.fill((255,255,255))

        # Drawing grid
        draw_grid(display, size, rows)

        # Drawing objects
        pygame.draw.rect(display, (0,0,255),(thief.x,thief.y,thief.width,thief.height))
        pygame.draw.rect(display, (255, 0, 0), (turrel.x, turrel.y, turrel.width, turrel.height))
        pygame.draw.circle(display, bullet.color, (bullet.x, bullet.y), bullet.radius)
        pygame.draw.rect(display, (100, 100, 100), (chest.x, chest.y, chest.width, turrel.height))
        if thief.diff_x and thief.diff_y == 0:
            pass
        else:
            thief.move(chest.x,chest.y)
        bullet.shoot()
        pygame.display.flip()  # updating display
        clock.tick(10)

    pygame.quit()
    return status

for i in range(len(Y_pred)):
    if status == True:
        # display, clock, pygame =
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         break
        print(X_test['thief_spawn_y'][i])
        print(Y_test[i])
        print(Y_test[i] - Y_pred[i])
        status = main(
             bullet_x=X_test['projectile_spawn_x'][i],
             bullet_y=X_test['projectile_spawn_y'][i],
             thief_spawn_x=X_test['thief_spawn_x'][i],
             thief_spawn_y=X_test['thief_spawn_y'][i],
             bullet_speed=X_test['projectile_speed'][i],
             thief_speed=X_test['thief_speed'][i],
             bullet_angle=Y_pred[i]
             # display=display,
             # clock=clock
             )
    else:
        break
