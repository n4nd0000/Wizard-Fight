import pygame as pg

class Magia:
    def __init__(self, x, y, direcao, sprites, velocidade=12):
        self.sprites = sprites                  # Lista de imagens da animação da magia
        self.frame = 0                          # Frame atual da animação
        self.max_frame = len(sprites)           # Quantidade total de frames
        self.image = self.sprites[self.frame]   # Imagem atual da magia
        
        self.rect = self.image.get_rect(center=(x, y))  # Posição da imagem na tela

        # Hitbox da magia (área de colisão)
        self.hitbox = pg.Rect(0, 0, 120, 70)
        self.hitbox.center = self.rect.center
        
        self.direcao = direcao                  # Direção do projétil (1 = direita, -1 = esquerda)
        self.velocidade = velocidade * direcao  # Velocidade com sinal da direção
        self.ativo = True                       # Se a magia ainda está ativa na tela
        self.dano = 50                          # Dano que a magia causa
        self.contador_frames = 0                # Contador para controlar a troca de frame
        self.ja_reduziu_vel = False             # (opcional) Flag para reduzir velocidade uma vez

    def mover(self):
        # Move a magia
        self.rect.x += self.velocidade
        self.hitbox.center = self.rect.center

        # Atualiza animação da magia a cada 5 frames
        self.contador_frames += 1
        if self.contador_frames >= 5:
            self.contador_frames = 0
            if self.frame < self.max_frame - 1:
                self.frame += 1
                self.image = self.sprites[self.frame]
            else:
                self.ativo = False  # Desativa a magia ao fim da animação

        # Se sair da tela, desativa
        if self.rect.right < 0 or self.rect.left > 980:
            self.ativo = False

    def desenhar(self, tela):
        # Desenha a magia se estiver ativa
        if self.ativo:
            imagem = self.image
            if self.direcao == -1:
                imagem = pg.transform.flip(self.image, True, False)  # Espelha imagem para esquerda
            tela.blit(imagem, self.rect)
