import pygame
class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,size,assets_path):
        super().__init__()
        self.images=[]
        for n in range(1,5):
            img=pygame.image.load(f"{assets_path}/exp{n}.png").convert_alpha()
            if size==1: img=pygame.transform.scale(img,(20,20))
            elif size==2: img=pygame.transform.scale(img,(40,40))
            elif size==3: img=pygame.transform.scale(img,(160,160))
            self.images.append(img)
        self.index=0
        self.image=self.images[self.index]
        self.rect=self.image.get_rect(center=(x,y))
        self.counter=0
    def update(self):
        self.counter+=1
        if self.counter>=3 and self.index < len(self.images)-1:
            self.counter=0
            self.index+=1
            self.image=self.images[self.index]
        if self.index>=len(self.images)-1 and self.counter>=3:
            self.kill()
