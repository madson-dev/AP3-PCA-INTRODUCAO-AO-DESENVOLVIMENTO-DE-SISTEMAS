from re import T
from time import sleep
import pygame as pg
from random import randrange

from obj import Char, Text, Obj


class Game:
    """
    CLASSE JOGO, ORGANIZA TODAS AS FUNCIONALIDADES E OBJETOS DO JOGO
    """

    def __init__(self):

        # VARIÁVEIS > OBJETOS > IMAGENS ATRIBUÍDAS > LOCALIZAÇÃO(X,Y)
        self.bg = Obj("assets/bg.png", 0, 0)
        self.bg2 = Obj("assets/bg.png", 0, -640)
        self.virus = Obj("assets/virus1.png", randrange(0, 300), -50)
        self.obj_pts = Obj("assets/objeto1.png", randrange(0, 300), -50)

        self.virus_variante = Obj("assets/virus5.png", randrange(0, 300), -200)

        self.char = Char("assets/char1.png", 150, 550)
        self.game_over = Obj("assets/game-over.png", 0, 0)

        self.s_new_fase = pg.mixer.Sound('assets/sounds/themebeach.mp3')
        self.s_over = pg.mixer.Sound('assets/sounds/over.mp3')

        self.s_new_fase.play(-1)

        # PONTOS E VIDAS
        self.score = Text(30, "0")
        self.bar = Text(30, "/")
        self.rank = Text(30, "0")

        self.life1 = Obj('assets/life.png', 30, 30)
        self.life2 = Obj('assets/life.png', 60, 30)
        self.life3 = Obj('assets/life.png', 90, 30)

        # VAR DE CONTROLE DE MOVIMENTOS
        self.move_up, self.move_down, self.move_left, self.move_right = False, False, False, False

        # VAR CONTROLE DA CENA
        self.new_fase = False
        self.change_scene = False
        self.victory = False

    def draw(self, window):
        """
        OBJETOS A SEREM DESENHADOS
        :param window: ADICIONA ESSES OBJETOS NA VAR DA TELA NA CLASS MAIN
        """

        self.bg.drawing(window)
        self.bg2.drawing(window)
        self.virus.drawing(window)
        self.virus_variante.drawing(window)
        self.obj_pts.drawing(window)
        self.char.drawing(window)

        self.score.draw(window, 260, 30)
        self.bar.draw(window, 285, 30)
        self.rank.draw(window, 300, 30)

        if self.char.life >= 3:
            self.life1.drawing(window), self.life2.drawing(window), self.life3.drawing(window)
        elif self.char.life == 2:
            self.life1.drawing(window), self.life2.drawing(window)
        elif self.char.life == 1:
            self.life1.drawing(window)
        else:
            self.game_OVER()

    def update(self):
        """
        ATUALIZA OS OBJETOS E FUNÇÕES
        """

        if self.char.pts >= self.char.rank:
            self.new_fase = True
            self.char.rank = self.char.rank * 2

        self.move_BG()  # AT. MOVIMENTO DO BACKGROUND
        # self.virus.anim('virus', 8, 5)  # AT. ANIMAÇÃO DO VIRUS
        self.move_OBJ_PTS()  # AT. MOVIMENTO DOS OBJETOS DE PONTOS
        # self.obj_pts.anim('objeto', 8, 3)  # AT. ANIMAÇÃO DOS OBJETOS DE PONTOS
        self.char.anim('char', 3, 5)  # AT. ANIMAÇÃO DO PERSONAGEM
        self.move_VIRUS()  # AT. MOVIMENTO DO VIRUS
        self.you_win()

        self.char.colision(self.virus.group, 'virus')  # AT. COLISÃO DO CHAR CONTRA O VIRUS
        self.char.colision(self.virus_variante.group, 'virus')  # AT. COLISÃO DO CHAR CONTRA O VIRUS
        self.char.colision(self.obj_pts.group, 'objeto')  # AT. COLISÃO DO CHAR CONTRA OS OBJ_PTS

        self.game_OVER()  # ATUALIZA A CONDIÇÃO DE FIM DE JOGO

        self.score.update_text(str(self.char.pts))  # AT. O TXT(SCORE) NA TELA
        self.rank.update_text(str(self.char.rank))  # AT. O TXT(RANK) NA TELA

    def move_CHAR(self, event):
        """
        MOVIMENTO DO PERSONAGEM
        CONTROLE DO MOVIMENTO POR KEYBOARD:
        A > DIREITA // S > ESQUERDA
        (MOVIMENTO PARA CIMA E BAIXO (W, S) OPCIONAL
        :param event: PASSA O EVENTO PARA A CLASS MAIN
        """

        # DESATIVADO------------------------------------
        # if self.move_up:        # CIMA POSIÇÃO Y VERTICAL
        #    self.char.sprite.rect[1] -= 0
        # else:
        #    self.char.sprite.rect[1] += 0
        # if self.move_down:      # BAIXO POSIÇÃO Y VERTICAL
        #    self.char.sprite.rect[1] += 0
        # else:
        #    self.char.sprite.rect[1] += 0

        if self.move_left:  # ESQUERDA POSIÇÃO X HORIZONTAL
            self.char.sprite.rect[0] -= 3
        else:
            self.char.sprite.rect[0] += 0

        if self.move_right:  # DIREITA POSIÇÃO X HORIZONTAL
            self.char.sprite.rect[0] += 3
        else:
            self.char.sprite.rect[0] += 0

        if event.type == pg.KEYDOWN:  # TECLA PRESSIONADA
            if event.key == pg.K_a:
                self.move_left = True
            if event.key == pg.K_d:
                self.move_right = True

            # if event.key == pg.K_w:
            #    self.move_up = True
            # if event.key == pg.K_s:
            #    self.move_down = True

        if event.type == pg.KEYUP:  # TECLA ACIMA
            if event.key == pg.K_a:
                self.move_left = False
            if event.key == pg.K_d:
                self.move_right = False

            # if event.key == pg.K_w:
            #    self.move_up = False
            # if event.key == pg.K_s:
            #    self.move_down = False

        # LIMITE DO MOVIMENTO DO PERSONAGEM NA TELA
        if self.char.sprite.rect[0] >= 313: self.char.sprite.rect[0] = 313
        if self.char.sprite.rect[0] <= 0: self.char.sprite.rect[0] = 0

    def move_BG(self):
        """
        MOVIMENTO DO BACK-GROUND
        DOIS OBJETOS DE BACK-GROUND, ADICIONA SEMPRE VALOR NA POSIÇÃO Y
        AO CHEGAR NO LIMITE RETORNA PARA POSIÇÃO INICIAL

        """
        # Troca as imagens de fundo
        if self.new_fase:
            self.bg.sprite.image = pg.image.load("assets/bg2.png")
            self.bg2.sprite.image = pg.image.load("assets/bg2.png")

        else:
            self.bg.sprite.image = pg.image.load("assets/bg.png")
            self.bg2.sprite.image = pg.image.load("assets/bg.png")

        #   add Movimento em Y nos objetos de BACK-GROUND
        self.bg.sprite.rect[1] += 1
        self.bg2.sprite.rect[1] += 1

        #   add loop e limite para o movimento do BACK-GROUND
        if self.bg.sprite.rect[1] >= 640:
            self.bg.sprite.rect[1] = 0

        if self.bg2.sprite.rect[1] >= 0:
            self.bg2.sprite.rect[1] = -640

    def move_VIRUS(self):
        """
        MOVIMENTO DO VIRUS
        OBJ SE MOVE SEMPRE ADICIONANDO VALOR EM Y E ALEATORIZANDO X
        AO CHEGAR NO LIMITE DA TELA, O MÉTODO KILL() ELIMINA O SPRITE.
        """
        from random import randrange
        from obj import Obj

        if self.new_fase:
            self.virus.sprite.rect[1] += 9
            self.virus_variante.sprite.rect[1] += 9
        else:
            self.virus.sprite.rect[1] += 8
            self.virus_variante.sprite.rect[1] += 8

        if self.virus.sprite.rect[1] >= 700:
            self.virus.sprite.kill()
            self.virus = Obj("assets/virus1.png", randrange(0, 300), -50)

        if self.new_fase:
            if self.virus_variante.sprite.rect[1] >= 700:
                self.virus_variante.sprite.kill()
                self.virus_variante = Obj("assets/virus6.png", randrange(0, 300), -200)
        else:
            if self.virus_variante.sprite.rect[1] >= 700:
                self.virus_variante.sprite.kill()
                self.virus_variante = Obj("assets/virus5.png", randrange(0, 300), -200)

    def move_OBJ_PTS(self):
        """
        MOVIMENTO DOS OBJETOS DE PONTOS
        OBJ SE MOVE SEMPRE ADICIONANDO VALOR EM Y E ALEATORIZANDO X
        AO CHEGAR NO LIMITE DA TELA, O MÉTODO KILL() ELIMINA O SPRITE.
        """
        from random import randrange, choice
        from obj import Obj

        lista = ['assets/objeto1.png', 'assets/objeto3.png', 'assets/objeto5.png']

        #   Define vlc em Y/e verifica se for >= 700Y/ sprite morre e o obj renasce aleatoriamente.
        self.obj_pts.sprite.rect[1] += 6

        if self.obj_pts.sprite.rect[1] >= 700:
            self.obj_pts.sprite.kill()
            f = choice(lista)

            self.obj_pts = Obj(str(f), randrange(0, 300), -50)

    def game_OVER(self):
        """
        VERIFICA A CONDIÇÃO DA VIDA DO PERSONAGEM
        SE FOR ZERO, ACIONA A TROCA DE CENA E ENCERRA O JOGO.
        """
        if self.char.life <= 0:

            self.s_new_fase.stop()
            self.change_scene = True
            self.new_fase = False
            self.s_over.play()


    def you_win(self):
        if self.char.pts >= 20:

            self.s_new_fase.stop()
            self.change_scene = True
            self.new_fase = False
            self.victory = True

