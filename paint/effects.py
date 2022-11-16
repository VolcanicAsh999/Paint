import pygame, time
import globals as G
import buttons as b
import singlePygameGUI as PygameGUI
from text_input import gettextinput

handler = PygameGUI.ScreenHandler(G.SCREEN)

pygame.init()


class WidthSlider:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, G.BUTTON_WIDTH, 100)
        self.sliderect = pygame.Rect(x, y - 3, G.BUTTON_WIDTH, 5)
        self.cango = range(y - 3, y + 97)
        self.name = 'Adjust Width'
        self.hit = False
        self.y = y
        self.prevpos = pygame.mouse.get_pos()[1]

    def update(self):
        self.draw()
        if not self.hit:
            pos = pygame.mouse.get_pos()
            if pos[0] in range(self.sliderect.x, self.sliderect.x + self.sliderect.width) and pos[1] in range(self.sliderect.y, self.sliderect.y + self.sliderect.height):
                self.outline()
                self.hovertext()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        self.click(True)

        else:
            if pygame.mouse.get_pos()[1] in self.cango:
                self.sliderect = pygame.Rect(self.sliderect.x, pygame.mouse.get_pos()[1], G.BUTTON_WIDTH, 5)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and not pygame.mouse.get_pressed()[0]:
                    self.click(False)
                    self.update_width()

    def outline(self):
        pygame.draw.rect(G.SCREEN, pygame.Color('black'), pygame.Rect(self.sliderect.x - 2, self.sliderect.y - 2, self.sliderect.width + 4, self.sliderect.height + 4))
        pygame.draw.rect(G.SCREEN, pygame.Color('dark gray'), self.sliderect)

    def hovertext(self):
        surf = pygame.font.Font('resources\\8-Bit-Madness.ttf', 20).render(self.name, 1, pygame.Color('black'))
        pos = pygame.mouse.get_pos()
        if pos[0] + surf.get_width() > G.SCREEN_WIDTH:
            pos = (pos[0] - (surf.get_width() + 10), pos[1])
        else:
            pos = (pos[0] + 10, pos[1])
        G.GAME.pending(G.SCREEN.blit, (surf, pos))

    def click(self, hit):
        self.hit = hit
        self.prevpos = pygame.mouse.get_pos()[1]

    def update_width(self):
        width = ((self.sliderect.y - self.y) // 5) + 1
        G.SPOT_WIDTH = width

    def draw(self):
        pygame.draw.rect(G.SCREEN, pygame.Color('white'), self.rect)
        pygame.draw.rect(G.SCREEN, pygame.Color('dark gray'), self.sliderect)

class ClearButton(b.Button):
    def __init__(self, x, y):
        super().__init__(x, y, 'white')
        self.name = 'Clear Screen'
        self.game = G.GAME

    def click(self):
        self.game.spots = {}
        self.game.other = []
        self.game.other2 = []

class TextButton(b.Button):
    def __init__(self, x, y):
        super().__init__(x, y, 'white')
        self.name = 'Write Text'

    def draw(self):
        super().draw()
        G.SCREEN.blit(pygame.font.Font('resources\\8-Bit-Madness.ttf', 20).render('T', 1, pygame.Color('black')), (self.rect.x + 5, self.rect.y + 3))

    def click(self):
        self.pending = True
        text = gettextinput((5, G.SCREEN_HEIGHT - 150), G.SCREEN, fontname='resources\\8-Bit-Madness', whilerunfunc=(G.GAME.draw_no, ()), other_text='Text > ')
        text = text.replace('''"''', '''\\\"''').replace("""'""", """\\\'""")
        pos = handler.wait_for_click(func=(G.GAME.draw_no, ()))[1]
        #G.GAME.other.append({'func': f"pygame.font.Font('resources\\8-Bit-Madness.ttf', {G.SPOT_WIDTH * 7}).render", 'args': f"('{text}', 1, {G.SELECTED_COLOR})", 'pos': pos})
        G.GAME.other.append((pygame.font.Font('resources\\8-Bit-Madness.ttf', G.SPOT_WIDTH * 7).render(text, 1, G.SELECTED_COLOR), pos))
        self.pending = False
        G.GAME.ignorefornow = True
        return

class LineButton(b.Button):
    def __init__(self, x, y):
        super().__init__(x, y, 'white')
        self.name = 'Create Line'

    def draw(self):
        super().draw()
        pygame.draw.line(G.SCREEN, pygame.Color('black'), (self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y + self.rect.height))

    def click(self):
        self.pending = True
        pos1 = handler.wait_for_click(func=(G.GAME.draw_no, ()))[1]
        pos2 = handler.wait_for_click(func=(G.GAME.draw_no, ()))[1]
        G.GAME.other2.append({'type': 'line', 'pos1': pos1, 'pos2': pos2, 'color': G.SELECTED_COLOR, 'width': G.SPOT_WIDTH})
        self.pending = False
        G.GAME.ignorefornow = True
        return

class RectButton(b.Button):
    def __init__(self, x, y):
        super().__init__(x, y, 'white')
        self.name = 'Create Rect'

    def draw(self):
        super().draw()
        pygame.draw.rect(G.SCREEN, pygame.Color('black'), pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6))

    def click(self):
        self.pending = True
        pos1 = handler.wait_for_click(func=(G.GAME.draw_no, ()))[1]
        pos2 = handler.wait_for_click(func=(G.GAME.draw_no, ()))[1]
        G.GAME.other2.append({'type': 'rect', 'pos': (min(pos1[0], pos2[0]), min(pos1[1], pos2[1])), 'width': max(pos1[0], pos2[0]) - min(pos1[0], pos2[0]), 'height': max(pos1[1], pos2[1]) - min(pos1[1], pos2[1]), 'color': G.SELECTED_COLOR})
        self.pending = False
        G.GAME.ignorefornow = True
        return

class PicButton(b.Button):
    def __init__(self, x, y):
        super().__init__(x, y, 'white')
        self.name = 'Save Picture'

    def draw(self):
        super().draw()
        pygame.draw.rect(G.SCREEN, pygame.Color('grey'), pygame.Rect(self.rect.x + 2, self.rect.y + 4, self.rect.width - 4, self.rect.height - 8))

    def click(self):
        name = gettextinput((5, G.SCREEN_HEIGHT - 150), G.SCREEN, fontname='resources\\8-Bit-Madness', whilerunfunc=(G.GAME.draw_no, ()), other_text='Screenshot Name > ')
        G.GAME.take_pic(name)



b1 = WidthSlider(G.SCREEN_WIDTH - 25, 50)
b2 = ClearButton(G.SCREEN_WIDTH - 25, 180)
b3 = TextButton(G.SCREEN_WIDTH - 25, 205)
b4 = LineButton(G.SCREEN_WIDTH - 25, 230)
b5 = RectButton(G.SCREEN_WIDTH - 25, 255)
b6 = PicButton(G.SCREEN_WIDTH - 25, 280)

buttons = [b1, b2, b3, b4, b5, b6]
