import pygame
def draw_text(surface,text,font,color,x,y):
    img = font.render(text,True,color)
    surface.blit(img,(x,y))

def load_image(path):
    return pygame.image.load(path).convert_alpha()

def draw_bg(surface,img):
    surface.blit(img,(0,0))
