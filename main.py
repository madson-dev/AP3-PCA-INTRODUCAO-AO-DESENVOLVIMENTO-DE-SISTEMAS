
from pygame import display, event, mixer, time, QUIT


class Main:
    """
    CLASSE PRINCIPAL
    """

    def __init__(self):
        """
        FUNÇÃO INICIAL DA CLASSE
        CONTEM AS PRINCIPAIS CARACTERÍSTICAS E FUNCIONALIDADES(PG) PARA GERENCIAR O JOGO
        """
        from start_screen import Start_screen, Gameover, Win
        from game import Game

        # INICIA O MIXER DO PYGAME
        mixer.init()

        # LARGURA E ALTURA DO DISPLAY, E, TITULO
        self.window = display.set_mode([360, 640])
        display.set_caption('CORONA RUN')

        # VAR CONTROLE DO JOGO(GAME) E (INICIO E FIM)
        self.game = Game()
        self.start_screen = Start_screen("assets/start.png")
        self.over = Gameover("assets/game-over.png")
        self.win = Win("assets/youwin.png")

        # VAR DE CONTROLE DA CLASSE E VAR DE CONTROLE DE FPS
        self.loop = True
        self.fps = time.Clock()

    def draw(self):
        """
        CONTROLE SEQUENCIAL DE CENAS E ATUALIZAÇÃO DAS IMAGENS(OBJ)
        """

        # INICIA A CENA START
        if not self.start_screen.change_scene:
            self.start_screen.draw(self.window)
            self.start_screen.update()

        # INICIA A CENA DO GAME
        elif not self.game.change_scene:
            self.game.draw(self.window)
            self.game.update()

        # CENA DE VITORIA
        elif not self.win.change_scene and self.game.victory:
            self.win.draw(self.window)
            self.win.update()

        # RETORNA A CENA GAME OVER
        elif (not self.over.change_scene) and (not self.game.victory):
            self.over.draw(self.window)
            self.over.update()

        # ZERA O JOGO
        else:
            self.start_screen.change_scene = False
            self.game.change_scene = False
            self.over.change_scene = False
            self.win.change_scene = False
            self.game.victory = False
            self.game.char.life = 3
            self.game.char.pts = 0
            self.game.char.rank = 10
            self.game.s_new_fase.play(-1)

    def events(self):
        """
        CONTROLE E PASSAGEM DE EVENTOS
        """
        # LAÇO, PEGA TODOS OS EVENTOS DENTRO DOS PG.EVENT
        for events in event.get():
            if events.type == QUIT:
                self.loop = False

            # VERIFICA OS EVENTOS DE START E GAME
            # START_SCREEN
            if not self.start_screen.change_scene:
                self.start_screen.events(events)

            # GAME
            elif not self.game.change_scene:
                self.game.move_CHAR(events)

            # WIN
            elif not self.win.change_scene and self.game.victory:
                self.win.events(events)

            # GAME OVER
            else:
                self.over.events(events)

            # ADICIONA OS EVENTOS DAS CLASSES
            self.start_screen.events(events)
            self.game.move_CHAR(events)

    def update(self):
        """
        MANTÉM O LOOP PRINCIPAL DO JOGO
        - ATUALIZAÇÃO: FPS, IMAGENS, EVENTOS(CONDIÇÕES) E TELA.
        """
        while self.loop:
            self.fps.tick(30)
            self.draw()
            self.events()
            display.update()


# INICIA O JOGO
game = Main()
game.update()
