import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Life Runner of Dragon")

clock = pygame.time.Clock()
FPS = 60

try:
    vida_img = pygame.image.load("learning/Verde.avif").convert_alpha()
    vida_img = pygame.transform.scale(vida_img, (30, 30))
except:
    vida_img = pygame.Surface((30, 30))
    vida_img.fill((0, 255, 0))

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("learning/cavaleiro.webp").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
        except:
            self.image = pygame.Surface((60, 60))
            self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.velocidade = 6

    def update(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.velocidade
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.velocidade
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, velocidade):
        super().__init__()
        try:
            self.image = pygame.image.load("learning/dragao.webp").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
        except:
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.velocidade = velocidade

    def update(self):
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.kill()

def main():
    jogador = Jogador()
    obstaculos = pygame.sprite.Group()
    todos_sprites = pygame.sprite.Group(jogador)

    vidas = 5
    fase = 1
    pontuacao = 0
    velocidade_obstaculo = 5
    MAX_FASES = 5

    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, 1500)

    rodando = True
    while rodando:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == spawn_event:
                obstaculo = Obstaculo(velocidade_obstaculo)
                obstaculos.add(obstaculo)
                todos_sprites.add(obstaculo)

        keys = pygame.key.get_pressed()
        jogador.update(keys)
        obstaculos.update()

        if pygame.sprite.spritecollide(jogador, obstaculos, True):
            vidas -= 1
            if vidas <= 0:
                rodando = False

        if jogador.rect.right >= WIDTH - 50:
            fase += 1
            velocidade_obstaculo += 3
            if fase > MAX_FASES:
                rodando = False
            else:
                jogador.rect.center = (100, HEIGHT // 2)

        pontuacao += 1

        tela.fill((0, 0, 0))
        todos_sprites.draw(tela)
        pygame.draw.rect(tela, (255, 255, 0), (WIDTH - 50, 0, 10, HEIGHT))

        for i in range(vidas):
            tela.blit(vida_img, (10 + i * 35, 10))

        fonte = pygame.font.SysFont(None, 36)
        texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
        texto_fase = fonte.render(f'Fase: {fase}', True, (255, 255, 255))
        tela.blit(texto_pontuacao, (10, 50))
        tela.blit(texto_fase, (10, 90))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    