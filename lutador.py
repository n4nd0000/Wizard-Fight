import pygame as pg
from Magia import Magia

class Lutador:
    #propriedades iniciais do personagem.
    def __init__(self, x, y, sprites_parado, sprites_correndo, sprites_pulando,
                 sprites_ataque1, sprites_ataque2, sprites_morte, sprites_dano, sprites_magia, sprites_vitoria, jogador=1): #todas as propriedades do lutador 
        
        self.jogador = jogador      
        
        # Pega o primeiro sprite da animação 'parado' como referência para o tamanho.
        self.sprite_base = sprites_parado[0]
        # Armazena a largura e altura do sprite
        self.largura_sprite = self.sprite_base.get_width()
        self.altura_sprite = self.sprite_base.get_height()      

        self.rect = pg.Rect(0, 0, self.largura_sprite, self.altura_sprite)
        self.rect.center = (x, y) 
        self.vel_x = 0
        self.vel_y = 0
        self.no_chao = False
        self.pulando = False
        
        # Variáveis de ataque: armazenam a hitbox de ataque (quando ativa) e controlam a lógica de dano.
        self.hitbox_ataque = None
        self.dano_aplicado = False 
        self.recebendo_dano = False
        
        #projéteis (magia).
        self.projeteis = [] # Lista para armazenar as magias ativas na tela.
        self.cooldown_ataque2 = 0   # Contador de cooldown atual.
        self.tempo_cooldown_ataque2 = 60*25  # Cooldown para disparar magias (1 segundo a 60 FPS).
        self.magia_criada = False # Flag para garantir que a magia seja criada apenas uma vez por ataque.

        if self.jogador == 1:
            # Dicionário com ataque especial do Jogador 1.
            self.config_ataque2 = {
                "frame_disparo": 12,      # Frame da animação em que a magia é disparada.
                "deslocamento_x": 50,     # Deslocamento horizontal da origem da magia.
                "deslocamento_y": 45      # Deslocamento vertical da origem da magia.
            }
            # Define o tamanho da hitbox do corpo para o Jogador 1.
            largura_hitbox = self.largura_sprite * 0.25 
            altura_hitbox = self.altura_sprite * 0.55
        else: 
           
            self.config_ataque2 = {
                "frame_disparo": 5,    
                "deslocamento_x": 0,
                "deslocamento_y": 30
            }
            #hitbox do corpo para o Jogador 2.
            largura_hitbox = self.largura_sprite * 0.20  
            altura_hitbox = self.altura_sprite * 0.55 
        
        # Cria a hitbox do corpo do personagem com as dimensões definidas acima.
        self.hitbox_corpo = pg.Rect(0, 0, largura_hitbox, altura_hitbox)
        self._atualizar_hitbox_corpo()

        # Armazena todas as listas de sprites (frames de animação) para o personagem.
        self.sprites_parado = sprites_parado
        self.sprites_correndo = sprites_correndo
        self.sprites_pulando = sprites_pulando
        self.sprites_ataque1 = sprites_ataque1
        self.sprites_ataque2 = sprites_ataque2
        self.sprites_morte = sprites_morte
        self.sprites_dano = sprites_dano
        self.sprites_magia = sprites_magia
        self.frames_magia = []
        self.sprites_vitoria = sprites_vitoria # Armazena os sprites da vitória

        # Variáveis de estado e animação.
        self.estado = "parado"
        self.frame = 0 
        self.cont_anim = 0 
        
        # Atributos de combate.
        self.vida = 200
        self.morto = False 
        self.virado_esquerda = (jogador == 2) 
        
        self.atacando1 = False
        self.atacando2 = False
        
        # Bloco que define as teclas de controle para cada jogador.
        if jogador == 1:
            self.tecla_esq = pg.K_a
            self.tecla_dir = pg.K_d
            self.tecla_pulo = pg.K_w
            self.tecla_atk1 = pg.K_q
            self.tecla_atk2 = pg.K_e
        else: # jogador 2
            self.tecla_esq = pg.K_LEFT
            self.tecla_dir = pg.K_RIGHT
            self.tecla_pulo = pg.K_UP
            self.tecla_atk1 = pg.K_k
            self.tecla_atk2 = pg.K_l

    #posição da hitbox do corpo para que ela siga o sprite principal.
    def _atualizar_hitbox_corpo(self):
        self.hitbox_corpo.centerx = self.rect.centerx      
        self.hitbox_corpo.centery = self.rect.centery + (self.altura_sprite * 0.5 - self.hitbox_corpo.height * 0.5)

    # Cria uma hitbox de ataque temporária.
    def _criar_hitbox_ataque(self, tipo=1):
        #diferentes tamanhos de hitbox para diferentes tipos de ataque.
        if tipo == 1:
            largura = 60
            altura = 70
        elif tipo == 2:
            largura = 50  
            altura = 60
        else: # Padrão
            largura = 60
            altura = 70
        
        # Posiciona a hitbox na frente do personagem
        if self.virado_esquerda:
            x = self.hitbox_corpo.left - largura
        else:
            x = self.hitbox_corpo.right
        y = self.hitbox_corpo.centery - altura // 2.
        self.hitbox_ataque = pg.Rect(x, y, largura, altura)

    
    #iniciar animação do ataque 2.
    def realizar_ataque2(self):
        self.estado = "ataque2"
        self.frame_atual = 0   
    

    def mover(self, teclas):
        # Impede o movimento se o personagem estiver morto, atacando ou recebendo dano.
        if self.morto or self.atacando1 or self.atacando2 or self.recebendo_dano:
            return  
        
        if teclas[self.tecla_pulo] and self.no_chao:
            self.vel_y = -20
            self.no_chao = False
            self.pulando = True # estado pulando 
            self.estado = "pulando"
        # Zera a velocidade horizontal a cada frame para que o personagem pare se nenhuma tecla for pressionada.
        self.vel_x = 0
        # Movimento para a esquerda.
        if teclas[self.tecla_esq]:
            self.vel_x = -7
            self.estado = "correndo"
            self.virado_esquerda = True
        # Movimento para a direita.
        elif teclas[self.tecla_dir]:
            self.vel_x = 7
            self.estado = "correndo"
            self.virado_esquerda = False
        # Se não estiver se movendo, pulando ou atacando, o estado é 'parado'.
        else:
            if not self.pulando and not self.atacando1 and not self.atacando2:
                self.estado = "parado"

        # Pulo.
        

        # Ataque 1.
        if teclas[self.tecla_atk1] and not self.atacando1:
            self.atacando1 = True
            self.estado = "ataque1"
            self.frame = 0
            
        # Ataque 2 (especial), verifica também o cooldown.
        if teclas[self.tecla_atk2] and not self.atacando2 and self.cooldown_ataque2 == 0:
            self.atacando2 = True
            self.estado = "ataque2"
            self.frame = 0
            self.realizar_ataque2()
            # Ativa o cooldown após o uso.
            self.cooldown_ataque2 = self.tempo_cooldown_ataque2

        # Aplica o movimento horizontal ao retângulo do personagem.
        self.rect.x += self.vel_x
        # Atualiza a posição da hitbox do corpo para seguir o personagem.
        self._atualizar_hitbox_corpo()
        
        # Impede que o personagem saia dos limites da tela.
        if self.rect.x > 835:
            self.rect.x = 835
            self.estado = "parado"
        elif self.rect.x < -110:
            self.rect.x = -110
            self.estado = "parado"
    

    def iniciar_vitoria(self):
        self.estado = "vitoria" 
        self.frame = 0 
        if self.virado_esquerda:
            self.vel_x = -2
        else:
            self.vel_x = 2 
    
    #gravidade.(dinêmica do pulo)
    def aplicar_gravidade(self):
        if not self.no_chao:
            self.vel_y += 0.9 # Aumenta a velocidade de queda.
            self.rect.y += int(self.vel_y) # Aplica a velocidade vertical.
            # Verifica se o personagem tocou o chão.
            if self.rect.y >= 300:
                self.rect.y = 300
                self.vel_y = 0
                self.no_chao = True
                self.pulando = False
                self.estado = "parado"

    #atualização, chamado a cada frame do jogo.
    def atualizar(self):
       # Animação de vitória que acontece quando algum jogador pe derrotado
        if self.estado == "vitoria":
        # Define a velocidade da animação
            self.cont_anim += 1
            if self.cont_anim >= 5: 
                self.cont_anim = 0
                self.frame = (self.frame + 1) % self._num_frames_atual()
            return
        # Verifica se a vida chegou a zero e inicia o estado de 'morto'.
        if self.vida <= 0 and not self.morto:
            self.morto = True
            self.estado = "morto"
            self.frame = 0
            self.cont_anim = 0

        # Animação de morte (não entra em loop).
        if self.morto:
            self.cont_anim += 1
            if self.cont_anim >= 4: 
                self.cont_anim = 0
                if self.frame < len(self.sprites_morte) - 1:
                    self.frame += 1 
            return
        
        # Animação de receber dano.
        if self.recebendo_dano:
            self.cont_anim += 1
            if self.cont_anim >= 5:
                self.cont_anim = 0
                if self.frame < len(self.sprites_dano) - 1:
                    self.frame += 1
                else:
                    # Ao final da animação, retorna ao estado 'parado'.
                    self.recebendo_dano = False
                    self.estado = "parado"
                    self.frame = 0
            return # Sai do método.

        # Animação dos ataques.
        if self.atacando1 or self.atacando2:
            self.cont_anim += 1
            if self.cont_anim >= 5:
                self.cont_anim = 0
                if self.frame < self._num_frames_atual() - 1:
                    self.frame += 1
                else:
                    self.atacando1 = False
                    self.atacando2 = False
                    self.estado = "parado"
                    self.frame = 0
                    self.hitbox_ataque = None
                    self.dano_aplicado = False
                    self.magia_criada = False
            
            #cria a hitbox do ataque 1 em um frame específico.
            if self.atacando1:
                if self.frame == 3 and not self.dano_aplicado:
                    self._criar_hitbox_ataque(tipo=1)
                else:
                    self.hitbox_ataque = None

            #criar a magia do ataque 2 em um frame específico.
            elif self.atacando2 and self.frame == self.config_ataque2["frame_disparo"]:
                if not self.magia_criada:
                    y = self.rect.centery + self.config_ataque2["deslocamento_y"]
                    if self.virado_esquerda:
                        x = self.rect.centerx - self.config_ataque2["deslocamento_x"]
                        direcao = -1
                    else:
                        x = self.rect.centerx+ self.config_ataque2["deslocamento_x"]
                        direcao = 1
                    nova_magia = Magia(x, y, direcao, self.sprites_magia)
                    # Adiciona a magia à lista de projéteis.
                    self.projeteis.append(nova_magia)
                    self.magia_criada = True # Impede que mais de uma magia seja criada.
        
        # Reduz o contador de cooldown do ataque 2 a cada frame.
        if self.cooldown_ataque2 > 0:
            self.cooldown_ataque2 -= 1

        if not (self.atacando1 or self.atacando2 or self.recebendo_dano or self.morto):
            self.cont_anim += 1
            if self.cont_anim >= 5:
                self.cont_anim = 0
                self.frame = (self.frame + 1) % self._num_frames_atual()
        
       
        
            
    # Desenha o personagem na tela.
    def desenhar(self, tela):
        imagem = self._get_sprite_atual()
        if imagem is None:
            return
        # Vira a imagem horizontalmente se o personagem estiver virado para a esquerda.
        if self.virado_esquerda:
            imagem = pg.transform.flip(imagem, True, False)
        # Desenha a imagem do sprite na tela.
        tela.blit(imagem, self.rect.topleft)

    # Função chamadq quando o personagem é atingido.
    def receber_dano(self, dano):
        # O personagem só pode receber dano se não estiver morto ou na animação de dano.
        if not self.morto and not self.recebendo_dano:
            self.vida -= dano
            self.recebendo_dano = True
            self.estado = "dano"
            self.frame = 0
            self.cont_anim = 0

    def _get_sprite_atual(self) :
        def get_sprite_safe(sprites) :
            if 0 <= self.frame < len(sprites):
                return sprites[self.frame]
            else: 
                return sprites[0] if sprites else None 

        if self.estado == "parado":
            return get_sprite_safe(self.sprites_parado)
        elif self.estado == "correndo":
            return get_sprite_safe(self.sprites_correndo)
        elif self.estado == "pulando":
            return get_sprite_safe(self.sprites_pulando)
        elif self.estado == "ataque1":
            return get_sprite_safe(self.sprites_ataque1)
        elif self.estado == "ataque2":
            return get_sprite_safe(self.sprites_ataque2)
        elif self.estado == "morto":
            return get_sprite_safe(self.sprites_morte)
        elif self.estado == "dano":
            return get_sprite_safe(self.sprites_dano)
        elif self.estado == "vitoria":
            return get_sprite_safe(self.sprites_vitoria)
        else: 
            return self.sprites_parado[0] if self.sprites_parado else None

    #número de frames da animação atual.
    def _num_frames_atual(self):
        return len(self._get_lista_sprite_atual())

    #lista de sprites correspondente ao estado atual.
    def _get_lista_sprite_atual(self):
        if self.estado == "parado":
            return self.sprites_parado
        elif self.estado == "correndo":
            return self.sprites_correndo
        elif self.estado == "pulando":
            return self.sprites_pulando
        elif self.estado == "ataque1":
            return self.sprites_ataque1
        elif self.estado == "ataque2":
            return self.sprites_ataque2
        elif self.estado == "morto":
            return self.sprites_morte
        elif self.estado == "dano":
            return self.sprites_dano
        elif self.estado == "vitoria":
            return self.sprites_vitoria
        return self.sprites_parado