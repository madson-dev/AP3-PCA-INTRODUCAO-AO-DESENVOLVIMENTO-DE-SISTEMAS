class Obj:

    def __init__(self, imagem, x, y):
        """
        CLASS OBJETO
        MOLDE PARA CRIAR OBJETOS COM OS MÉTODOS DE ATRIBUIÇÃO DE IMAGEM E POSIÇÃO.
        O OBJETO É TRATADO POR RETÂNGULO.
        :param: imagem: PASSA LOCAL E NOME DA IMAGEM.
        :param: x: POSIÇÃO HORIZONTAL
        :param: y: POSIÇÃO VERTICAL
        """
        from pygame import sprite, image, Rect

        # Cria um grupo e transforma a propria imagem/obj no próprio grupo.
        self.group = sprite.Group()
        self.sprite = sprite.Sprite(self.group)

        # ATRIBUI PARÂMETRO DE IMAGEM| E RETÂNGULO COM POS X E Y
        self.sprite.image = image.load(imagem)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect[0] = x
        self.sprite.rect[1] = y

        self.frame = 1  # VAR FRAME
        self.tick = 0   # VAR CONTADOR

    def drawing(self, window):
        # DESENHA O GRUPO DE SPRITES NA TELA(CLASS MAIN)
        self.group.draw(window)

    def anim(self, imagem, tick, frames):
        """
        CONTROLE DOS FRAMES DE ANIMAÇÃO DO PERSONAGEM.
        :param imagem: PASSA A IMAGEM A SER TROCADA.
        :param tick: PASSA O TEMPO QUE LEVA PARA TROCAR O FRAME.
        :param frames: PASSA A QUANTIDADE DE FRAMES.
        :return: NONE
        """
        from pygame import image

        #   Add valor para FPS/Frame e define seu loop. /-/ add sequencia dos frames.

        self.tick += 0.5            # REGULA A VALOR ATRIBUÍDO AO CONTADOR

        if self.tick == tick:       # PARA ESSE TEMPO TROQUE O FRAME
            self.tick = 0
            self.frame += 1

        if self.frame == frames:    # FRAMES QUE O OBJ POSSUI
            self.frame = 1

        #   add na VAR = outra imagem com local + "nome da imagem" + valor de "VAR frame"
        self.sprite.image = image.load("assets/" + imagem + str(self.frame) + ".png")
        
class Char(Obj):
    """
    CLASSE DE CONTROLE DO PERSONAGEM
    CARACTERÍSTICAS DA CLASS
    <CLASSE HERDADA DE OBJ>
    """
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

        self.life = 3
        self.pts = 0
        self.rank = 10

    def colision(self, group, name):
        """
        CONFERE COLISÕES COM OUTROS GRUPOS DE SPRITES
        :param group: PASSA O NOME DO GRUPO A COLIDIR
        :param name: NOME DA IMAGEM DO OBJ A COLIDIR
        :return: NONE
        """
        from pygame import sprite, mixer
        mixer.init()

        sound_pts = mixer.Sound("assets/sounds/score.ogg")
        sound_block = mixer.Sound("assets/sounds/bateu.ogg")

        name = name
        colision = sprite.spritecollide(self.sprite, group, True)

        if name in "objeto" and colision:
            self.pts += 1
            sound_pts.play()

        elif name in "virus" and colision:
            self.life -= 1
            sound_block.play()


class Text:
    """
    CLASSE PARA TRANSFORMAR VARIÁVEL EM FORMATO TEXTO E RENDERIZAR NO DISPLAY
    """
    def __init__(self, size, text):
        """
        TRANSFORMA O CONTEÚDO DE UMA VAR EM TXT, PASSANDO TM DA FONTE E A VAR.
        :param size: TAMANHO DA FONTE.
        :param text: VARIÁVEL PARA SE TORNAR TXT
        """
        from pygame import font
        font.init()

        self.font = font.SysFont("Arial bold", size)
        self.render = self.font.render(text, True, (255, 255, 255))

    def draw(self, window, x, y):
        """
        RENDERIZA NA TELA OS PARÂMETROS.
        :param window: PASSA PARA A TELA NA CLASS MAIN
        :param x: POSIÇÃO X HORIZONTAL
        :param y: POSIÇÃO Y VERTICAL
        :return: NONE
        """
        window.blit(self.render, (x, y))

    def update_text(self, update):
        """
        ATUALIZA O CONTEÚDO DA VAR
        :param update: A VARIÁVEL A SER ATUALIZADA NA TELA
        :return: NONE
        """
        self.render = self.font.render(update, True, (255, 255, 255))
