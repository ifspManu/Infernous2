import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da janela
LARGURA, ALTURA = 1280, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("INFERNOUS")

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonte
fonte = pygame.font.SysFont("Arial", 28, bold=True)

# Carrega imagens
fundo = pygame.image.load("fundo.jpg").convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

def vidass():
    if dano == 0 :
        tela.blit(vida8, (0,0))
    elif dano == 1:
        tela.blit(vida7, (0,0))
    elif dano == 2:
        tela.blit(vida6, (0,0))
    elif dano == 3:
        tela.blit(vida5, (0,0))
    elif dano == 4:
        tela.blit(vida4, (0,0))
    elif dano == 5:
        tela.blit(vida3, (0,0))
    elif dano == 6:
        tela.blit(vida2, (0,0))
    elif dano == 7:
        tela.blit(vida1, (0,0))
    elif dano == 8:
        tela.blit(vida0, (0,0))
        tela.blit(gameover,(0,0))


dano=0

vida8 = pygame.image.load("coracao/vida8.png").convert_alpha()
vida7 = pygame.image.load("coracao/vida7.png").convert_alpha()
vida6 = pygame.image.load("coracao/vida6.png").convert_alpha()
vida5 = pygame.image.load("coracao/vida5.png").convert_alpha()
vida4 = pygame.image.load("coracao/vida4.png").convert_alpha()
vida3 = pygame.image.load("coracao/vida3.png").convert_alpha()
vida2 = pygame.image.load("coracao/vida2.png").convert_alpha()
vida1 = pygame.image.load("coracao/vida1.png").convert_alpha()
vida0 = pygame.image.load("coracao/vida0.png").convert_alpha()
gameover = pygame.image.load("coracao/gameover.jpeg").convert_alpha()

flash_img = pygame.image.load("dano_sofrido.png").convert_alpha()
flash_img = pygame.transform.scale(flash_img, (LARGURA, ALTURA))

boneco_parado = pygame.image.load("jogador.png").convert_alpha()
boneco_andando1 = pygame.image.load("jogador1.png").convert_alpha()
boneco_andando2 = pygame.image.load("jogador.png").convert_alpha()

# Define posição inicial e velocidade
x, y = 100, 300
velocidade = 5
imagem_atual = boneco_parado

# Retângulo do jogador
boneco_rect = boneco_parado.get_rect(topleft=(x, y))

# Obstáculo (longe do boneco)
obstaculo_rect = pygame.Rect(600, 300, 100, 100)

# Controle da animação
contador_animacao = 0
fps_animacao = 10

# Controle de colisão e vidas
colidindo = False
vidas = 8
invencivel = False
tempo_invencivel = 0
duracao_invencivel = 1000  # 1 segundo de piscar

# Física do pulo
vel_y = 0  # velocidade vertical
gravidade = 0.8
pulo_forca = -15
no_chao = True  # indica se o boneco está no chão

# Define o chão como uma linha imaginária
chao_y = 500  # altura do chão

cor_tela_dano = (183, 3, 3)   # vermelho
tempo_flash = 0
duracao_flash = 100

# Relógio
clock = pygame.time.Clock()

# Loop principal
while True:
    tempo_atual = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Quando apertar espaço → pular
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and no_chao and vidas > 0:
                vel_y = pulo_forca
                no_chao = False

    teclas = pygame.key.get_pressed()
    andando = False

    # Movimento horizontal
    nova_posicao = boneco_rect.copy()

    if teclas[pygame.K_LEFT]:
        nova_posicao.x -= velocidade
        andando = True
    if teclas[pygame.K_RIGHT]:
        nova_posicao.x += velocidade
        andando = True

    # Física da gravidade
    vel_y += gravidade
    nova_posicao.y += vel_y

    # Verifica se tocou o chão
    if nova_posicao.bottom >= chao_y:
        nova_posicao.bottom = chao_y
        vel_y = 0
        no_chao = True

    # Testa colisão com obstáculo
    if nova_posicao.colliderect(obstaculo_rect) and not invencivel:
        colidindo = True
        tempo_flash = tempo_atual
        #vidas -= 1 
        dano += 1
        invencivel = True
        tempo_invencivel = tempo_atual
        #print(f"💥 Colisão! Vidas restantes: {vidas}")
    else:
        colidindo = False
        if not invencivel:
            boneco_rect = nova_posicao

    

    # Sai do modo invencível após 1s
    if invencivel and tempo_atual - tempo_invencivel > duracao_invencivel:
        invencivel = False

    # Animação do boneco
    if andando:
        contador_animacao += 1
        if (contador_animacao // fps_animacao) % 2 == 0:
            imagem_atual = boneco_andando1
        else:
            imagem_atual = boneco_andando2
    else:
        imagem_atual = boneco_parado
        contador_animacao = 0

    # Desenha fundo
    tela.blit(fundo, (0, 0))

    pygame.draw.rect(tela, VERMELHO, obstaculo_rect)  # obstáculo
    ###pygame.draw.line(tela, BRANCO, (0, chao_y), (LARGURA, chao_y), 2)  # chão
 
    vidass()


    # Se ainda tiver vidas
    if dano < 8:
        # desenhar jogador normalmente
        if not (invencivel and (tempo_atual // 100) % 2 == 0):
            tela.blit(imagem_atual, boneco_rect.topleft)

    '''if vidas > 0:
        # Piscar quando invencível (colidindo)
        if not (invencivel and (tempo_atual // 100) % 2 == 0):
            tela.blit(imagem_atual, boneco_rect.topleft)
    else:
        # Mostra mensagem de morte
        texto_game_over = fonte.render("💀 GAME OVER! Você morreu!", True, VERMELHO)
        tela.blit(texto_game_over, (LARGURA // 2 - texto_game_over.get_width() // 2, ALTURA // 2))
    '''
    # Mostra contador de vidas
    #texto_vidas = fonte.render(f"Vidas: {vidas}", True, WHITE)
    #tela.blit(texto_vidas, (20, 20))
    
    # Mensagem de colisão
    #if colidindo:
    #    texto = fonte.render("⚠️ COLISÃO DETECTADA!", True, VERMELHO)
    #    tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 20))
        
    
    # Tela vermelha piscando ao tomar dano
    if tempo_atual - tempo_flash < duracao_flash:
        if (tempo_atual // 50) % 2 == 0:   # piscar rápido
           tela.blit(flash_img, (0,0))         # flash vermelho
           

    pygame.display.flip()
    clock.tick(30)