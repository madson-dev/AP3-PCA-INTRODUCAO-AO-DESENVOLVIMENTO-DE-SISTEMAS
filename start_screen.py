
from pygame import KEYDOWN, K_RETURN, MOUSEBUTTONUP, mouse
from obj import Obj

class Start_screen:
    def __init__(self, image):
        from obj import Char

        self.bg = Obj(image, 0, 0)
        self.char = Char("assets/char1.png", 150, 550)
        
        self.enter = Obj("assets/enter1.png", 95, 500)

        self.change_scene = False
        
    def draw(self, window):
        """
        DESENHA NA TELA A IMAGEM DA VAR BG
        :param window: PASSA A IMAGEM PARA A TELA NA CLASS MAIN
        """
        self.bg.drawing(window)
        self.char.drawing(window)

        self.enter.drawing(window)

    def update(self):
        self.char.anim('char', 3, 5)  # AT. ANIMAÇÃO DO PERSONAGEM
        self.enter.anim('enter', 3, 3)

    def events(self, event):
        """
        INICIA O JOGO AO PRESSIONAR (ENTER)
        :param event: PASSA A CONDIÇÃO DO EVENTO PARA CLASS MAIN
        """

        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.change_scene = True
        
        if event.type == MOUSEBUTTONUP:
            if self.enter.sprite.rect.collidepoint((mouse.get_pos())):
                 self.change_scene = True
        

class Gameover(Start_screen):
    def __init__(self, image):
        super().__init__(image)

        self.over = Obj(image, 0, 0)
        self.enter = Obj("assets/enter1.png", 95, 500)

        self.change_scene = False

    def draw(self, window):
        """
         DESENHA NA TELA A IMAGEM DA VAR OVER
        :param window: PASSA A IMAGEM PARA A TELA NA CLASS MAIN
        """
        self.over.drawing(window)
        self.enter.drawing(window)

    def update(self):
        self.enter.anim('enter', 3, 3)

    def events(self, event):
        """
        RETORNA A CENA START AO PRESSIONAR (ENTER)
        :param event: PASSA A CONDIÇÃO DO EVENTO PARA CLASS MAIN
        """

        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.change_scene = True

        if event.type == MOUSEBUTTONUP:
            if self.enter.sprite.rect.collidepoint((mouse.get_pos())):
                self.change_scene = True


class Win(Start_screen):
    def __init__(self, image):
        super().__init__(image)
        
        self.over = Obj(image, 0, 0)
        self.enter = Obj("assets/enter1.png", 95, 500)

        self.change_scene = False

    def draw(self, window):
        """
         DESENHA NA TELA A IMAGEM DA VAR OVER
        :param window: PASSA A IMAGEM PARA A TELA NA CLASS MAIN
        """
        self.over.drawing(window)
        self.enter.drawing(window)

    def update(self):
        self.enter.anim('enter', 3, 3)

    def events(self, event):
        """
        RETORNA A CENA START AO PRESSIONAR (ENTER)
        :param event: PASSA A CONDIÇÃO DO EVENTO PARA CLASS MAIN
        """
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.change_scene = True

        if event.type == MOUSEBUTTONUP:
            if self.enter.sprite.rect.collidepoint((mouse.get_pos())):
                 self.change_scene = True