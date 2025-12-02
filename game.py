import pygame
import random
import sys

pygame.init()


WIDTH = 800
HEIGHT = 600
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Life Runner of Dragons")

tempo = pygame.time.Clock()
FPS = 60


class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load("learning/Verde.png").convert_alpha()
        
        self.image = pygame.transform.scale(self.image, (50, 50))
        
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.velocidade = 5

    def update(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.velocidade


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
      
        self.image = pygame.image.load("learning/dragao.webp").convert_alpha()
        
        self.image = pygame.transform.scale(self.image, (50, 50))
        
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.velocidade = 7

    def update(self):
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.kill()


def main():
    jogador = Jogador()
    obstaculos = pygame.sprite.Group()
    todos_sprites = pygame.sprite.Group(jogador)

    vidas = 3
    pontuacao = 0

    # Evento para spawnar obstáculos
    spawn_obstaculo_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_obstaculo_event, 1500)

    rodando = True
    while rodando:
        tempo.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == spawn_obstaculo_event:
                obstaculo = Obstaculo()
                obstaculos.add(obstaculo)
                todos_sprites.add(obstaculo)

        keys = pygame.key.get_pressed()
        jogador.update(keys)
        obstaculos.update()

       
        if pygame.sprite.spritecollide(jogador, obstaculos, True):
            vidas -= 1
            if vidas <= 0:
                print("Game Over! Pontuação final:", pontuacao)
                rodando = False

        pontuacao += 1

       
        tela.fill((0, 0, 0))
        todos_sprites.draw(tela)

        fonte = pygame.font.SysFont(None, 36)
        texto_vidas = fonte.render(f'Vidas: {vidas}', True, (255, 255, 255))
        texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
        tela.blit(texto_vidas, (10, 10))
        tela.blit(texto_pontuacao, (10, 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
