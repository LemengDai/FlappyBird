import pygame,random
from pygame.locals import (
    K_UP,
    K_RETURN,
    KEYDOWN,
    QUIT,
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("1.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (100,90))
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH/4, SCREEN_HEIGHT/2)
        )
    def update(self, pressed_keys):
        if pressed_keys[K_UP]: #bird jumps when the up key is pressed
            self.rect.move_ip(0,-20)
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()
        else: #otherwise bird moves downwards
            self.rect.move_ip(0,10)

class BPipe(pygame.sprite.Sprite):
    def __init__(self,h1):
        super(BPipe, self).__init__()
        self.surf = pygame.image.load("bp.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (100,h1))
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH + 20,SCREEN_HEIGHT-h1/2)
        )
        self.speed = 10
        self.score_counted = False
        
    def update(self): #pipes keep moving to the left
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class TPipe(pygame.sprite.Sprite):
    def __init__(self,h2):
        super(TPipe, self).__init__()
        self.surf = pygame.image.load("tp.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (100,h2))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH + 20,h2/2))
        self.speed = 10
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

def display_text(atext, size, y):
    font = pygame.font.Font('freesansbold.ttf',size)
    text = font.render(str(atext), True, (0,0,0))
    textRect = text.get_rect(center=(SCREEN_WIDTH/2,y))
    screen.blit(text, textRect)

def game_over(score):
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == QUIT: #close the game
                over = False
            if event.type == KEYDOWN:
                if event.key == K_RETURN: #restart the game
                    gameLoop()
        display_text('Score: '+str(score),50,SCREEN_HEIGHT/2)
        display_text('Press Enter to Play Again',50,SCREEN_HEIGHT/2+50)
        pygame.display.flip()

pygame.init()
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
background = pygame.image.load("bg.png").convert()
background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))

#define events for adding pipes
ADDBP = pygame.USEREVENT + 1
ADDTP = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBP,1200)
pygame.time.set_timer(ADDTP,1200)

def gameLoop():
    player = Player()
    Bpipe = pygame.sprite.Group()
    Tpipe = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    clock = pygame.time.Clock()

    running = True
    pause = False
    score = 0
    while running:
        if pause:
            game_over(score)
            running = False
        else:
            h1 = random.randint(50,350)
            h2 = SCREEN_HEIGHT-h1-200
            
            #event handler
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == ADDBP:
                    bpipe = BPipe(h1)
                    Bpipe.add(bpipe)
                    all_sprites.add(bpipe)
                if event.type == ADDTP:
                    tpipe = TPipe(h2)
                    Tpipe.add(tpipe)
                    all_sprites.add(tpipe)
            
            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys)
            Bpipe.update()
            Tpipe.update()
            screen.blit(background,(0,0))
            display_text(score, 32, 25)
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)
            
            #count the player's score
            for p in Bpipe:
                if player.rect.left > p.rect.right and not p.score_counted:
                    score += 1
                    p.score_counted = True
            
            #collision detection method
            if pygame.sprite.spritecollideany(player, Bpipe):
                player.kill()
                pause = True
            if pygame.sprite.spritecollideany(player, Tpipe):
                player.kill()
                pause = True
        
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    quit()

gameLoop()
