import pygame, random

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, assets_path, speed):
        super().__init__()
        self.image = pygame.image.load(f"{assets_path}/alien{random.randint(1,5)}.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = speed
        self.move_direction = 1   # 1 = direita, -1 = esquerda

    def update(self):
        screen_w = pygame.display.get_surface().get_width()

        # Movimento horizontal normal
        self.rect.x += self.move_direction * self.speed

        # BATEU NA BORDA? -> INVERTE
        if self.rect.right >= screen_w:
            self.rect.right = screen_w
            self.move_direction = -1

        elif self.rect.left <= 0:
            self.rect.left = 0
            self.move_direction = 1


def create_aliens(rows, cols, group, assets_path, speed):
    start_x = 50       # posição inicial
    spacing_x = 70     # espaçamento horizontal
    start_y = 80
    spacing_y = 60

    for r in range(rows):
        for c in range(cols):
            x = start_x + c * spacing_x
            y = start_y + r * spacing_y
            group.add(Aliens(x, y, assets_path, speed))
