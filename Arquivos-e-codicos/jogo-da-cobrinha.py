import pygame # type: ignore
from pygame.locals import * # type: ignore
from sys import exit
from random import randint

from pygame.mixer import Sound
# Inicialização do Pygame
pygame.init()

# Configuração da música de fundo
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.load('musica_de_fundo.mp3')
pygame.mixer.music.play(-1)

# Efeito sonoro de comida e de game over
efeito_de_comida = pygame.mixer.Sound('efeito_de_comida.mp3')
efeito_game_over = pygame.mixer.Sound('efeito_game_ouver.mp3')

# Função para inicializar o jogo
def iniciar_jogo(largura, altura, tela_cheia=False):
    # Configurações iniciais
    x_cobra = largura / 2 - largura / 30
    y_cobra = altura / 2
    velocidade_maxima = 10
    x_controle = velocidade_maxima
    y_controle = 0
    x_maca = randint(52, largura - 72)
    y_maca = randint(52, altura - 72)
    pontos = 0
    fonte = pygame.font.SysFont('arial', 40, True, True)
    tamanho_da_cobra = 5
    lista_cobra = []
    morreu = False

    # Configuração da tela
    if tela_cheia:
        tela = pygame.display.set_mode((largura, altura), FULLSCREEN)
    else:
        tela = pygame.display.set_mode((largura, altura))

    pygame.display.set_caption("Jogo Da Cobrinha")
    tempo = pygame.time.Clock()

    # Função para desenhar a cobra
    def aumenta_cobra(lista_cobra):
        for segmento in lista_cobra:
            pygame.draw.rect(tela, (0, 100, 0), (segmento[0], segmento[1], 25, 25))

    # Função para reiniciar o jogo
    def reiniciar_jogo():
        nonlocal pontos, tamanho_da_cobra, x_cobra, y_cobra, lista_cobra, x_maca, y_maca, morreu
        pontos = 0
        tamanho_da_cobra = 5
        x_cobra = largura / 2 - largura / 30
        y_cobra = altura / 2
        lista_cobra = []
        x_maca = randint(52, largura - 72)
        y_maca = randint(52, altura - 72)
        morreu = False

    # Loop principal do jogo
    while True:
        tempo.tick(30)
        tela.fill((123, 160, 91))

        # Renderiza o texto dos pontos na tela
        mensagem = f'Pontos: {pontos}'
        texto_formatado = fonte.render(mensagem, True, (255, 255, 255))

        # Captura de eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == K_a:
                    if x_controle == velocidade_maxima:
                        pass
                    else:
                        x_controle = -velocidade_maxima
                        y_controle = 0
                if event.key == K_d:
                    if x_controle == -velocidade_maxima:
                        pass
                    else:
                        x_controle = velocidade_maxima
                        y_controle = 0
                if event.key == K_w:
                    if y_controle == velocidade_maxima:
                        pass
                    else:
                        y_controle = -velocidade_maxima
                        x_controle = 0
                if event.key == K_s:
                    if y_controle == -velocidade_maxima:
                        pass
                    else:
                        y_controle = velocidade_maxima
                        x_controle = 0
                if event.key == K_f:
                    tela_cheia = not tela_cheia
                    if tela_cheia:
                        tela = pygame.display.set_mode((largura, altura), FULLSCREEN)
                    else:
                        tela = pygame.display.set_mode((largura, altura))

        # Movimento da cobra
        x_cobra += x_controle
        y_cobra += y_controle

        # Desenha a cobra e a maçã
        cobra = pygame.draw.rect(tela, (0, 100, 0), (x_cobra, y_cobra, 25, 25))
        maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 25, 25))

        # Verifica se a cobra comeu a maçã
        if maca.colliderect(cobra):
            x_maca = randint(52, largura - 72)
            y_maca = randint(52, altura - 72)
            pontos += 1
            efeito_de_comida.play()
            tamanho_da_cobra += 1

        # Atualiza a lista da cobra com sua cabeça atual
        lista_cabeca = [x_cobra, y_cobra]
        lista_cobra.append(lista_cabeca)

        # Verifica se a cobra se colidiu com ela mesma
        if lista_cobra.count(lista_cabeca) > 1:
            pygame.mixer.music.load('musica_de_fundo.mp3')
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(efeito_game_over)  # Reproduz o efeito de game over
            fonte_2 = pygame.font.SysFont('arial', 40, True, True)
            mensagem = 'Game Over! Pressione R para reiniciar.'
            texto_formatado = fonte_2.render(mensagem, True, (255, 255, 255))
            ret_texto = texto_formatado.get_rect()
            ret_texto.center = tela.get_rect().center

            morreu = True
            while morreu:
                tela.fill((0, 0, 0))
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == KEYDOWN and event.key == K_r:
                        reiniciar_jogo()
                        morreu = False
                        pygame.mixer.music.load('musica_de_fundo.mp3')
                        pygame.mixer.music.play()

                tela.blit(texto_formatado, ret_texto)
                pygame.display.update()

        # Garante que a cobra apareça do outro lado da tela ao ultrapassar os limites
        if x_cobra > largura:
            x_cobra = 0
        if x_cobra < 0:
            x_cobra = largura
        if y_cobra < 0:
            y_cobra = altura
        if y_cobra > altura:
            y_cobra = 0

        # Mantém o tamanho máximo da cobra
        if len(lista_cobra) > tamanho_da_cobra:
            del lista_cobra[0]

        # Desenha a cobra atualizada e atualiza a tela
        aumenta_cobra(lista_cobra)
        tela.blit(texto_formatado, (largura // 2 - 100, 40))  # Posição ajustada para os pontos
        pygame.display.update()

# Inicializa o jogo com uma janela inicial de tamanho 800x600
iniciar_jogo(800, 600)