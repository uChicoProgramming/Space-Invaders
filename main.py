import pygame, os, random
from pygame import mixer
from settings import SCREEN_WIDTH,SCREEN_HEIGHT,FPS,WHITE
from utils import draw_text,draw_bg,load_image
from player import Spaceship
from aliens import create_aliens
from bullets import Bullets,Alien_Bullets
from explosion import Explosion
from score import load_scores, save_score

pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()
pygame.init()

screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders com Menu")

clock=pygame.time.Clock()

BASE=os.path.dirname(__file__)
ASSETS=os.path.join(BASE,"assets")

font40=pygame.font.SysFont("Arial",40)
font60=pygame.font.SysFont("Arial",60)
title_font = pygame.font.Font(os.path.join(ASSETS, "joystix.otf"), 60)
title_button = pygame.font.Font(os.path.join(ASSETS, "joystix.otf"), 35)
score_font = pygame.font.Font(os.path.join(ASSETS, "joystix.otf"), 20)
player_font = pygame.font.Font(os.path.join(ASSETS, "joystix.otf"), 10)
hud_font = pygame.font.SysFont("Arial", 28)

def safe_sound(p):
    try: s=pygame.mixer.Sound(p); s.set_volume(0.25); return s
    except: return None

explosion_fx = safe_sound(os.path.join(ASSETS,"explosion.wav"))
explosion2_fx= safe_sound(os.path.join(ASSETS,"explosion2.wav"))
laser_fx     = safe_sound(os.path.join(ASSETS,"laser.wav"))

bg = load_image(os.path.join(ASSETS,"bg.jpg")) if os.path.exists(os.path.join(ASSETS,"bg.jpg")) else None
menu_bg = load_image(os.path.join(ASSETS, "menu_bg.png"))

STATE_MENU=0
STATE_GAME=1
STATE_OVER=2
STATE_SCORES=3
state=STATE_MENU

phase = 1
score = 0
game_vars = {"score": 0, "player_name": ""}  # <- nome começa vazio
name_active = False
name_box = None


def draw_retro_button(surface, x, y, w, h, text, font):
    yellow = (255, 230, 0)
    dark_yellow = (200, 180, 0)
    brown = (120, 80, 20)

    pygame.draw.rect(surface, brown, (x+4, y+4, w, h), border_radius=6)
    pygame.draw.rect(surface, yellow, (x, y, w, h), border_radius=6)
    pygame.draw.rect(surface, dark_yellow, (x, y, w, h), 4, border_radius=6)

    txt = title_button.render(text, True, brown)
    txt_rect = txt.get_rect(center=(x + w//2, y + h//2))
    surface.blit(txt, txt_rect)

    return pygame.Rect(x, y, w, h)


def draw_menu():
    screen.blit(menu_bg, (0,0))

    title1 = title_font.render("GALACTIC", True, (255, 183, 0))
    title2 = title_font.render("DEFENDER", True, (255, 183, 0))

    y_start = 170
    screen.blit(title1, (SCREEN_WIDTH//2 - title1.get_width()//2, y_start))
    screen.blit(title2, (SCREEN_WIDTH//2 - title2.get_width()//2, y_start + title1.get_height() + 5))

    start_btn = draw_retro_button(screen, SCREEN_WIDTH//2 - 150, 400, 300, 80, "INICIAR", font40)
    scores_btn = draw_retro_button(screen, SCREEN_WIDTH//2 - 150, 520, 300, 80, "SCORES", font40)

    box_w, box_h = 300, 40
    box_x = SCREEN_WIDTH//2 - box_w//2
    box_y = 330
    name_rect = pygame.Rect(box_x, box_y, box_w, box_h)

    pygame.draw.rect(screen, (255,255,255), name_rect, 2, border_radius=6)

    text_to_show = game_vars["player_name"] if game_vars["player_name"] else "DIGITE O NOME"
    color = WHITE if game_vars["player_name"] else (180,180,180)

    name_text = hud_font.render(text_to_show, True, color)
    screen.blit(name_text, (box_x + 8, box_y + (box_h - name_text.get_height())//2))

    return start_btn, scores_btn, name_rect


def draw_over(win):
    screen.fill((0,0,0))
    msg="VOCÊ VENCEU!" if win else "GAME OVER"
    over=font60.render(msg,True,WHITE)
    screen.blit(over,(SCREEN_WIDTH//2-over.get_width()//2,250))
    btn1=font40.render("RECOMEÇAR",True,WHITE)
    r1=btn1.get_rect(center=(SCREEN_WIDTH//2,420))
    screen.blit(btn1,r1)
    btn2=font40.render("MENU",True,WHITE)
    r2=btn2.get_rect(center=(SCREEN_WIDTH//2,500))
    screen.blit(btn2,r2)
    return r1,r2


def start_game():
    spaceship_group=pygame.sprite.Group()
    bullet_group=pygame.sprite.Group()
    alien_group=pygame.sprite.Group()
    alien_bullet_group=pygame.sprite.Group()
    explosion_group=pygame.sprite.Group()
    explosion_group.assets_path=ASSETS

    create_aliens(5, 5, alien_group, ASSETS, speed=phase)
    ship=Spaceship(SCREEN_WIDTH//2,SCREEN_HEIGHT-100,3,ASSETS,laser_fx)
    spaceship_group.add(ship)
    return spaceship_group,bullet_group,alien_group,alien_bullet_group,explosion_group,ship


def draw_scores_screen():
    screen.fill((10,10,20))
    title = title_font.render("TOP SCORES", True, (255,200,0))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 60))

    entries = load_scores()
    y = 160
    for i, (name, s) in enumerate(entries):
        txt = hud_font.render(f"{i+1}. {name} — {s}", True, WHITE)
        screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, y))
        y += 38

    back_btn = draw_retro_button(screen, SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 130, 300, 70, "VOLTAR", font40)
    return back_btn


spaceship_group=bullet_group=alien_group=alien_bullet_group=explosion_group=ship=None
game_over=0
last_alien=pygame.time.get_ticks()

running=True
while running:
    clock.tick(FPS)

    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            running=False

        # ============================
        #      ***** MENU *****
        # ============================
        if state == STATE_MENU:

            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # botões prontos ANTES do clique
                start_btn, scores_btn, name_box = draw_menu()

                if start_btn.collidepoint(mx,my):
                    if game_vars["player_name"] == "":
                        game_vars["player_name"] = "PLAYER"

                    phase = 1
                    game_vars["score"] = 0
                    (spaceship_group, bullet_group, alien_group,
                    alien_bullet_group, explosion_group, ship) = start_game()
                    game_over = 0
                    state = STATE_GAME

                elif scores_btn.collidepoint(mx,my):
                    state = STATE_SCORES

                elif name_box.collidepoint(mx,my):
                    name_active = True
                else:
                    name_active = False

            # DIGITAR NOME
            if e.type == pygame.KEYDOWN and name_active:
                if e.key == pygame.K_BACKSPACE:
                    game_vars["player_name"] = game_vars["player_name"][:-1]
                elif e.key == pygame.K_RETURN:
                    name_active = False
                else:
                    if len(game_vars["player_name"]) < 12:
                        ch = e.unicode
                        if ch.isprintable():
                            game_vars["player_name"] += ch.upper()


        # ============================
        #    ***** SCORES *****
        # ============================
        elif state == STATE_SCORES:
            if e.type == pygame.MOUSEBUTTONDOWN:
                back_btn = draw_scores_screen()
                mx,my = pygame.mouse.get_pos()
                if back_btn.collidepoint(mx,my):
                    state = STATE_MENU


        # ============================
        #   ***** GAME OVER *****
        # ============================
        elif state==STATE_OVER:
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                if r1.collidepoint(mx,my):
                    phase = 1
                    score = 0
                    (spaceship_group,bullet_group,alien_group,
                     alien_bullet_group,explosion_group,ship)=start_game()
                    game_over=0
                    state=STATE_GAME
                if r2.collidepoint(mx,my):
                    state=STATE_MENU


    # =====================================
    #           DESENHAR TELAS
    # =====================================

    if state==STATE_MENU:
        draw_menu()

    elif state==STATE_SCORES:
        back_btn = draw_scores_screen()

    elif state==STATE_GAME:
        screen.blit(menu_bg, (0,0))

        if ship:
            game_over=ship.update(screen,SCREEN_WIDTH,bullet_group,explosion_group,explosion_fx)

        for b in list(bullet_group):
            b.update(alien_group, explosion_group, explosion_fx, game_vars)

        alien_group.update()
        now=pygame.time.get_ticks()

        fire_rate = max(300, 1000 - phase * 80)

        if now - last_alien > fire_rate and len(alien_group) > 0:
            a = random.choice(alien_group.sprites())
            shots = min(1 + (phase // 2), 5)

            for _ in range(shots):
                alien_bullet_group.add(
                    Alien_Bullets(
                        a.rect.centerx,
                        a.rect.bottom,
                        ASSETS,
                        speed=2 + phase * 0.8
                    )
                )
            last_alien = now

        for ab in list(alien_bullet_group):
            ab.update(spaceship_group,explosion_group,explosion2_fx,ship,SCREEN_HEIGHT)

        explosion_group.update()

        if len(alien_group) == 0:
            phase += 1
            create_aliens(5, 8, alien_group, ASSETS, speed= phase * 0.6)

        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)
        explosion_group.draw(screen)

        draw_text(screen, f"Fase: {phase}", score_font, (255, 183, 0), 10, 10)

        text = f"Pontos: {game_vars['score']}"
        img = score_font.render(text, True, (255, 183, 0))
        screen.blit(img, (SCREEN_WIDTH - img.get_width() - 10, 10))

        name_img = player_font.render(game_vars.get("player_name","PLAYER"), True, WHITE)
        screen.blit(name_img, (10, 40))

        if game_over!=0:
            try:
                save_score(game_vars.get("player_name","PLAYER"), game_vars.get("score",0))
            except:
                pass
            state=STATE_OVER
            win = (game_over==1)


    elif state==STATE_OVER:
        r1,r2 = draw_over(win)

    pygame.display.update()

pygame.quit()
