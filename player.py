import pygame
from bullets import Bullets
from explosion import Explosion

class Spaceship(pygame.sprite.Sprite):
    def __init__(self,x,y,hp,assets_path,laser_fx=None):
        super().__init__()
        self.image=pygame.image.load(f"{assets_path}/nave.png").convert_alpha()
        self.rect=self.image.get_rect(center=(x,y))
        self.health_start=hp
        self.health_remaining=hp
        self.last_shot=pygame.time.get_ticks()
        self.assets_path=assets_path
        self.laser_fx=laser_fx
    def update(self,screen,w,bullet_group,explosion_group,explosion_fx):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left>0: self.rect.x -=8
        if keys[pygame.K_RIGHT] and self.rect.right<w: self.rect.x +=8
        now=pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now-self.last_shot>500:
            if self.laser_fx: self.laser_fx.play()
            bullet_group.add(Bullets(self.rect.centerx, self.rect.top, self.assets_path, speed=7))
            self.last_shot=now
        self.mask=pygame.mask.from_surface(self.image)
        pygame.draw.rect(screen,(255,0,0),(self.rect.x,self.rect.bottom+10,self.rect.width,15))
        if self.health_remaining>0:
            pygame.draw.rect(screen,(0,255,0),(self.rect.x,self.rect.bottom+10,int(self.rect.width*(self.health_remaining/self.health_start)),15))
        else:
            explosion_group.add(Explosion(self.rect.centerx,self.rect.centery,3,self.assets_path))
            self.kill()
            return -1
        return 0
