import pygame as pg
from lutador import Lutador
import sys

#inicialização
pg.init() # inicia o pg
pg.mixer.init()
pg.mixer.music.load("tema.mp3")
pg.mixer.music.play(-1)
clock = pg.time.Clock()
FPS = 60
# Configurações da tela
largura, altura = 980,655 
tela = pg.display.set_mode((largura, altura))# carrega as informações da tela 
pg.display.set_caption(("Wizard fight"))
background = pg.image.load("cenario.png").convert()
#lícone
icone = pg.image.load("iconejogo.png")  # Substitua pelo caminho do seu ícone
pg.display.set_icon(icone)

# carregar sprites
def carregar_sprites(nome_arquivo, num_frames,largura_sprite,altura_sprite, escala_x=1, escala_y=1):
    imagem = pg.image.load(nome_arquivo).convert_alpha()
    sprites = []
    for i in range (num_frames):
        frame_original = imagem.subsurface(i * largura_sprite, 0, largura_sprite, altura_sprite)
        frame = pg.transform.scale(frame_original, (int(largura_sprite * escala_x), int(altura_sprite * escala_y)))
        sprites.append(frame)
    return sprites

#Tela restart 
# Em main.py

def tela_restart(tela, background, largura, altura, vitoria, vencedor, perdedor, clock, FPS):
    
    # Prepara o vencedor para começar a andar
    vencedor.iniciar_vitoria()

    #animação continua enquanto o vencedor estiver visível na tela
    animacao_rodando = True
    while animacao_rodando:
        clock.tick(FPS)

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Atualiza a animação de ambos (vencedor andando, perdedor morto no chão)
        vencedor.atualizar()
        perdedor.atualizar()

        # Move o vencedor para fora da tela
        vencedor.rect.x += vencedor.vel_x

        # Desenha a cena
        tela.blit(background, (0, 0))
        vencedor.desenhar(tela)
        perdedor.desenhar(tela)
        pg.display.update()

        # Condição para terminar a animação de vitória
        if vencedor.rect.right < 0 or vencedor.rect.left > largura:
            animacao_rodando = False # Para o loop da animação

    fonte = pg.font.SysFont(None, 48)
    if vitoria == 1:
        textovitoria = fonte.render("O Feiticeiro Triunfou Neste Combate!", True, (255, 255, 255))
    else:
        textovitoria = fonte.render("O Mago de Fogo Se Sagrou Vitorioso!", True, (255, 255, 255))
    textovitoria_rect = textovitoria.get_rect(midtop=(largura // 2, altura // 4))

    texto = fonte.render("Pressione R para reiniciar ou ESC para sair", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(largura // 2, altura // 2))

    while True:
        tela.blit(background, (0, 0))
        perdedor.desenhar(tela) 
        tela.blit(textovitoria, textovitoria_rect)
        tela.blit(texto, texto_rect)
        pg.display.update()

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                return False
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_r:
                    return True 
                if evento.key == pg.K_ESCAPE:
                    return False 
#carregamento dos sprites :

#jogador 1

parado1 = carregar_sprites("Wanderer Magican/Idle.png", 8, 128, 128,escala_x=2, escala_y=2)
correndo1 = carregar_sprites("Wanderer Magican/Run.png", 8, 128, 128,escala_x=2, escala_y=2)
pulando1 = carregar_sprites("Wanderer Magican/jump.png", 8, 128, 128,escala_x=2, escala_y=2)
ataque11 = carregar_sprites("Wanderer Magican/Attack_1.png", 7, 128, 128,escala_x=2, escala_y=2) 
ataque21 = carregar_sprites("Wanderer Magican/Magic_Sphere.png", 16, 128, 128,escala_x=2, escala_y=2)  # 1152 / 9 = 128
morte1 = carregar_sprites("Wanderer Magican/Dead.png", 4, 128, 128,escala_x=2, escala_y=2)         # 512 / 4 = 128
dano1 = carregar_sprites("Wanderer Magican/Hurt.png", 4, 128, 128,escala_x=2, escala_y=2)
magia1 = carregar_sprites("Wanderer Magican/Charge_1.png", 9, 64, 128, escala_x=6, escala_y=6)
vitoria1 = carregar_sprites("Wanderer Magican/Walk.png", 7, 128, 128,escala_x=2, escala_y=2)

#jogador 2
parado2 = carregar_sprites("Fire Wizard/Idle.png", 7, 128,128, escala_x=2, escala_y=2)
correndo2 = carregar_sprites("Fire wizard/Run.png", 8, 128,128, escala_x=2, escala_y=2)
pulando2 = carregar_sprites("Fire Wizard/Jump.png",9, 128, 128, escala_x=2, escala_y=2)
ataque12 = carregar_sprites("Fire Wizard/Attack_1.png", 4,128, 128, escala_x=2, escala_y=2)
ataque22 = carregar_sprites("Fire Wizard/Fireball.png",8, 128, 128, escala_x=2, escala_y=2)
morte2 = carregar_sprites("Fire Wizard/Dead.png", 6, 128, 128, escala_x=2, escala_y=2) 
dano2 = carregar_sprites("Fire Wizard/Hurt.png", 3, 128, 128, escala_x=2, escala_y=2)
magia2 = carregar_sprites("Fire Wizard/Charge.png", 12, 64, 64, escala_x=4, escala_y=4)
vitoria2 = carregar_sprites("Fire Wizard/Walk.png", 6, 128, 128, escala_x=2, escala_y=2)

# Criação dos objetos jogador 3
chao = 500
jogador1 = Lutador(200, chao, parado1, correndo1, pulando1, ataque11, ataque21,morte1, dano1, magia1, vitoria1, jogador=1)
jogador2 = Lutador(700, chao, parado2, correndo2, pulando2, ataque12,ataque22 ,morte2, dano2, magia2, vitoria2, jogador=2)

# Função que desenha a tela de pause
def desenha_tela_pause(superficie):
    tela.blit(superficie, (0, 0))  
    fonte = pg.font.Font(None, 60)
    texto = fonte.render("PAUSADO - pressione P para continuar", True, (255, 255, 255))
    rect = texto.get_rect(center=(largura // 2, altura // 2))
    tela.blit(texto, rect)

# Variáveis da tela de Pause
pausado = False
tela_pause = pg.Surface((largura, altura), pg.SRCALPHA)
tela_pause.fill((0, 0, 0, 150))
 
#tela de Start

def tela_start(tela, largura, altura):
    pg.font.init()
    
    fundo = pg.image.load("Tela_Start.png") 
    fundo = pg.transform.scale(fundo, (largura, altura))
    
    while True:
        tela.blit(fundo, (0, 0))
        pg.display.update()

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit()  
            elif evento.type == pg.KEYDOWN:
                if evento.key == pg.K_RETURN:
                    return  

tela_start(tela, largura, altura)

# Loop principal
rodando = True
while rodando:
    clock.tick(FPS)
    mouse = pg.mouse.get_pos()
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            rodando = False
        if evento.type == pg.KEYDOWN:
            if evento.key == pg.K_p:
                pausado = not pausado  
# Verificação se o jogo tá pausado
    if not pausado:
        teclas = pg.key.get_pressed()

        jogador1.mover(teclas)
        jogador2.mover(teclas)
        

        jogador1.aplicar_gravidade()
        jogador2.aplicar_gravidade()

        jogador1.atualizar()
        jogador2.atualizar()
            
        pg.mixer.music.unpause() 
        
    tela.fill((0, 0, 0))
    tela.blit(background, (0, 0))
    jogador1.desenhar(tela)
    jogador2.desenhar(tela)
       
    # Verifica os projéteis do jogador 1
    for proj in jogador1.projeteis:
    # Se um projétil ativo atinge o jogador 2
        if proj.ativo and proj.rect.colliderect(jogador2.hitbox_corpo):
    # o jogador 2 sofre dano
            jogador2.receber_dano(proj.dano)
            if not proj.ja_reduziu_vel:
                proj.ja_reduziu_vel = True
                proj.velocidade *= 0.4  # só reduz uma vez
                       
    # Faz o mesmo para os projéteis do jogador 2.
    for proj in jogador2.projeteis:
        if proj.ativo and proj.rect.colliderect(jogador1.hitbox_corpo):
            jogador1.receber_dano(proj.dano)
            if not proj.ja_reduziu_vel:
                proj.ja_reduziu_vel = True
                proj.velocidade *= 0.4  # só reduz uma vez
                
    # Repete a lógica pros 2
    for lutador in [jogador1, jogador2]:
        for proj in lutador.projeteis:
            proj.mover()
            proj.desenhar(tela) 
        lutador.projeteis = [proj for proj in lutador.projeteis if proj.ativo]

    if pausado:
        desenha_tela_pause(tela_pause)
        pg.mixer.music.pause()  
     
    # dano
    if jogador1.hitbox_ataque and jogador1.hitbox_ataque.colliderect(jogador2.hitbox_corpo):      
        if not jogador1.dano_aplicado:
            jogador2.receber_dano(10)
            jogador1.dano_aplicado = True
            
    if jogador2.hitbox_ataque and jogador2.hitbox_ataque.colliderect(jogador1.hitbox_corpo):
        if not jogador2.dano_aplicado:
            jogador1.receber_dano(10)
            jogador2.dano_aplicado = True

        
    #  Barra de vida do Jogador 1 
    pg.draw.rect(tela, (255, 0, 0), (50, 30, 200, 10))  
    pg.draw.rect(tela, (0, 255, 0), (50, 30, max(0, jogador1.vida), 10)) 

    #  Barra de vida do Jogador 2 
    vida2 = max(0, jogador2.vida)  
    pg.draw.rect(tela, (255, 0, 0), (732, 30, 200, 10))  
    pg.draw.rect(tela, (0, 255, 0), (732 + (200 - vida2), 30, vida2, 10)) 

    #Barra de vida
    font = pg.font.SysFont(None, 24)
    texto1 = font.render(f"Feiticeiro : {jogador1.vida}", True, (255, 255, 255))
    texto2 = font.render(f"Mago De Fogo: {jogador2.vida}", True, (255, 255, 255))
    tela.blit(texto1, (100, 15))
    tela.blit(texto2, (750, 15))
    # Recarga do especial
    
    # Jogador 1
    # Define a posição e o tamanho máximo da barra
    barra_recargax = 50
    barra_recargay = 50 
    largura_barra = 200
    altura_barra = 10
    # Calcula a recarga
    progresso_recarga1 = (jogador1.tempo_cooldown_ataque2 - jogador1.cooldown_ataque2) / jogador1.tempo_cooldown_ataque2 
    largura_recarga1 = largura_barra * progresso_recarga1
    # Desenha o fundo cinza da barra
    pg.draw.rect(tela, (40, 40, 40), (barra_recargax, barra_recargay, largura_barra, altura_barra))
    # Desenha a parte preenchida da barra (azul)
    pg.draw.rect(tela, (0, 150, 255), (barra_recargax, barra_recargay, largura_recarga1, altura_barra))
    # Desenha a borda da barra
    pg.draw.rect(tela, (255, 255, 255), (barra_recargax, barra_recargay, largura_barra, altura_barra), 2)

    # Jogador 2 
    # Define a posição e o tamanho máximo da barra
    regarga_x2 = 732
    BARRA_RECARGA2_Y = 50
    # Calcula o progresso e a largura da barra
    progresso_recarga2 = (jogador2.tempo_cooldown_ataque2 - jogador2.cooldown_ataque2) / jogador2.tempo_cooldown_ataque2
    largura_recarga2 = largura_barra * progresso_recarga2
    # Desenha o fundo e o preenchimento da barra para o Jogador 2
    pg.draw.rect(tela, (40, 40, 40), (regarga_x2, BARRA_RECARGA2_Y, largura_barra, altura_barra))
    pg.draw.rect(tela, (0, 150, 255), (regarga_x2, BARRA_RECARGA2_Y, largura_recarga2, altura_barra))
    pg.draw.rect(tela, (255, 255, 255), (regarga_x2, BARRA_RECARGA2_Y, largura_barra, altura_barra), 2)

    if jogador1.vida <= 0 or jogador2.vida <= 0:
        largura, altura = 982, 655
        tela = pg.display.set_mode((largura,altura))
        background = pg.image.load("cenario.png").convert()
        if jogador1.vida <= 0:
            vencedor = jogador2
            perdedor = jogador1
            vitoria = 2
        else:
            vencedor = jogador1
            perdedor = jogador2
            vitoria = 1
        reiniciar = tela_restart(tela, background, largura, altura, vitoria, vencedor, perdedor, clock, FPS)
         
        if reiniciar == True:
            jogador1.vida = 200
            jogador2.vida = 200
            jogador1 = Lutador(200, chao, parado1, correndo1, pulando1, ataque11, ataque21, morte1, dano1, magia1, vitoria1, jogador=1)
            jogador2 = Lutador(700, chao, parado2, correndo2, pulando2, ataque12, ataque22, morte2, dano2, magia2, vitoria2, jogador=2)
        else:
            rodando = False
        
    pg.display.update()
    if teclas[pg.K_ESCAPE]:
        rodando = False

pg.quit()
sys.exit()