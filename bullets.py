import pygame
from explosion import Explosion

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, assets_path, speed):
        super().__init__()
        self.assets_path = assets_path
        self.image = pygame.image.load(f"{assets_path}/tiro.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed  # <<< velocidade do tiro do jogador

    def update(self, alien_group, explosion_group, explosion_fx, game_vars):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
            return

        hit = pygame.sprite.spritecollide(self, alien_group, True)
        if hit:
            game_vars["score"] += 10
            self.kill()
            if explosion_fx:
                explosion_fx.play()
            explosion_group.add(
                Explosion(self.rect.centerx, self.rect.centery, 2, self.assets_path)
            )


class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, assets_path, speed):
        super().__init__()
        self.assets_path = assets_path
        self.image = pygame.image.load(f"{assets_path}/alien_bullet.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed  # <<< agora o tiro do alien tem velocidade

    def update(self, ship_group, explosion_group, explosion_fx, ship_ref, screen_h):
        self.rect.y += self.speed  # <<< antes estava quebrado, agora funciona

        if self.rect.top > screen_h:
            self.kill()
            return

        if pygame.sprite.spritecollide(self, ship_group, False, pygame.sprite.collide_mask):
            self.kill()
            if explosion_fx:
                explosion_fx.play()

            ship_ref.health_remaining -= 1
            explosion_group.add(
                Explosion(self.rect.centerx, self.rect.centery, 1, self.assets_path)
            )

