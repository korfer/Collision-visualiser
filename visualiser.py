import pygame
import math
import simulation



#PyGame Configuration
size = 500
rows = 10
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode(size=(size, size))
display.fill((255, 255, 255))
pygame.display.set_caption("Aim trainer")

class Thief():
    def __init__(self,x_cord, y_cord):
        super().__init__()
        self.x = x_cord
        self.y = y_cord
        self.width = 50
        self.height = 50
        self.speed = 1.719273*50*0.1
        self.diff_x = None
        self.diff_y = None
        self.image = pygame.image.load("trump.png")
        self.rect = self.image.get_rect()


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
        self.speed = 5

class Bullet:
    def __init__(self,x_cord, y_cord, angle):
        self.x = x_cord
        self.y = y_cord
        self.radius = 5
        self.color = (0,255,0)
        self.speed = 3*50*0.1
        self.angle = angle
        self.radians = math.radians(angle)
        self.cos = math.cos(self.radians)
        self.sin = math.sin(self.radians)
        self.tang = math.tan(self.angle)

    def shoot(self):
        self.x += self.cos * self.speed
        self.y -= self.sin * self.speed

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


def main():
    run = True

    # Object initialization
    turrel = Turrel(9*50, 3.012884*50)
    chest = Tresure(450,200)
    thief = Thief(0,2.913328*50-50)
    bullet = Bullet(9*50, 3.012884*50, 183.018356)

    while run == True:
        # Setting quit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


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
        clock.tick(5)

    pygame.quit()


main()