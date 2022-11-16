import pygame, string, warnings
import globals as G
from text_input import getnuminput

class Button:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, G.BUTTON_WIDTH, G.BUTTON_HEIGHT)
        if isinstance(color, tuple):
            self.color = pygame.Color(*color)
        elif isinstance(color, str):
            self.color = pygame.Color(color)
        elif isinstance(color, pygame.Color):
            self.color = color
        else:
            warnings.warn('`color` argument must be of type `tuple` `str` or `pygame.Color`', UserWarning)
        self.outlinerect = pygame.Rect(x - 2, y - 2, G.BUTTON_WIDTH + 4, G.BUTTON_HEIGHT + 4)
        self.name = color
        self.pending = False

    def update(self):
        if not self.pending:
            pos = pygame.mouse.get_pos()
            if pos[0] in range(self.rect.x, self.rect.x + self.rect.width) and pos[1] in range(self.rect.y, self.rect.y + self.rect.height):
                self.outline()
                self.hovertext()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        self.click()
        self.draw()

    def outline(self):
        pygame.draw.rect(G.SCREEN, pygame.Color('black') if self.color != pygame.Color('black') else pygame.Color('white'), self.outlinerect)

    def draw(self):
        pygame.draw.rect(G.SCREEN, self.color, self.rect)

    def click(self):
        G.SELECTED_COLOR = self.color

    def hovertext(self):
        surf = pygame.font.Font('resources\\8-Bit-Madness.ttf', 20).render(string.capwords(self.name), 1, pygame.Color('black'))
        pos = pygame.mouse.get_pos()
        if pos[0] + surf.get_width() > G.SCREEN_WIDTH:
            pos = (pos[0] - (surf.get_width() + 10), pos[1])
        else:
            pos = (pos[0] + 10, pos[1])
        G.GAME.pending(G.SCREEN.blit, (surf, pos))
        

class SelectorButton(Button):
    def __init__(self, x, y):
        self.r = 255
        self.g = 255
        self.b = 255
        super().__init__(x, y, (self.r, self.g, self.b))
        self.name = 'Custom'
        self.game = G.GAME

    def click(self):
        self.r, self.g, self.b = self.get_color()
        self.color = pygame.Color(self.r, self.g, self.b)
        super().click()

    def get_color(self):
        self.pending = True
        text = getnuminput((5, G.SCREEN_HEIGHT - 100), G.SCREEN, fontname='resources\\8-Bit-Madness', whilerunfunc=(G.GAME.draw_no, ()), other_text = 'RGB value separated by spaces (nothing to remain same) > ')
        text = text.split(' ')
        self.pending = False
        if text == []:
            return self.r, self.g, self.b
        try:
            return int(float(text[0])), int(float(text[1])), int(float(text[2]))
        except (ValueError, IndexError):
            return self.r, self.g, self.b


b1 = Button(5, 5, 'white')
b2 = Button(30, 5, 'light gray')
b3 = Button(55, 5, 'dark gray')
b4 = Button(80, 5, 'black')
b5 = Button(105, 5, 'dark red')
b6 = Button(130, 5, 'red')
b7 = Button(155, 5, 'orange')
b8 = Button(180, 5, 'gold')
b9 = Button(205, 5, 'light yellow')
b10 = Button(230, 5, 'yellow')
b11 = Button(255, 5, 'light green')
b12 = Button(280, 5, 'green')
b13 = Button(305, 5, 'light blue')
b14 = Button(330, 5, 'blue')
b15 = Button(355, 5, 'dark blue')
b16 = Button(380, 5, 'purple')
b17 = Button(405, 5, 'pink')
b18 = Button(430, 5, 'brown')
b19 = Button(455, 5, 'tan')
b20 = SelectorButton(480, 5)

buttons = [b1, b2, b3, b4, b5, b6,
           b7, b8, b9, b10, b11,
           b12, b13, b14, b15, b16,
           b17, b18, b19, b20]
