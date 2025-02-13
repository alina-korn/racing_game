import pygame
import random

# Настройки экрана
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Racing Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Класс машины
class Car:
    def __init__(self):
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.speed = 5
        self.alive = True
    
    def move(self, keys):
        if self.alive:
            if keys[pygame.K_LEFT] and self.rect.left > 200:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < 600:
                self.rect.x += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Класс дороги
class Road:
    def __init__(self):
        self.road_rect = pygame.Rect(200, 0, 400, HEIGHT)
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.road_rect)

# Класс препятствий
class Obstacle:
    def __init__(self):
        self.image = pygame.Surface((50, 80))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(random.randint(225, 575), -100))
        self.speed = 5
    
    def move(self):
        self.rect.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def off_screen(self):
        return self.rect.top > HEIGHT

# Основной игровой цикл
def game_loop():
    car = Car()
    road = Road()
    obstacles = []
    obstacle_timer = 0
    avoided = 0
    crashed = 0
    
    running = True
    while running:
        screen.fill(WHITE)
        road.draw(screen)
        car.draw(screen)
        
        keys = pygame.key.get_pressed()
        car.move(keys)
        
        if obstacle_timer > 50:
            obstacles.append(Obstacle())
            obstacle_timer = 0
        obstacle_timer += 1
        
        for obstacle in obstacles[:]:
            obstacle.move()
            obstacle.draw(screen)
            
            if obstacle.off_screen():
                obstacles.remove(obstacle)
                avoided += 1
            
            if car.rect.colliderect(obstacle.rect) and car.alive:
                car.alive = False
                crashed += 1
        
        score_text = font.render(f"Avoided: {avoided}  Crashed: {crashed}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    game_loop()
