import pygame
import globals as G
import singlePygameGUI as PygameGUI #USE OLD PYGAMEGUI
from text_input import gettextinput

pygame.init()

G.SCREEN = pygame.display.set_mode((G.SCREEN_WIDTH, G.SCREEN_HEIGHT))
pygame.display.set_caption(G.CAPTION)

handler = PygameGUI.ScreenHandler(G.SCREEN)

class Game:
    def __init__(self):
        G.GAME = self
        import buttons, effects
        globals().update({'buttons': buttons, 'effects': effects})
        self.buttons = buttons.buttons + effects.buttons
        self.spots = {}
        self.other = []
        self.other2 = []
        self.buttondown = False
        self.pendingevents = []
        self.screen = pygame.display.get_surface()
        self.ignorefornow = False

    def draw(self):
        self.screen.fill(G.BGCOLOR)
        self.pendingevent()
        handler.draw_text((5, G.SCREEN_HEIGHT - 25), f'Current Width: {G.SPOT_WIDTH}', font='resources\\8-Bit-Madness')
        handler.draw_text((5, G.SCREEN_HEIGHT - 50), f'Color:', font='resources\\8-Bit-Madness')
        pygame.draw.rect(G.SCREEN, G.SELECTED_COLOR, pygame.Rect(60, G.SCREEN_HEIGHT - 50, G.BUTTON_WIDTH, G.BUTTON_HEIGHT))
        for thing in self.other2:
            if thing['type'] == 'line':
                pygame.draw.line(G.SCREEN, thing['color'], thing['pos1'], thing['pos2'], width=thing['width'])
            if thing['type'] == 'rect':
                pygame.draw.rect(G.SCREEN, thing['color'], pygame.Rect(thing['pos'][0], thing['pos'][1], thing['width'], thing['height']))
        for button in self.buttons:
            button.update()
        for pos, data in self.spots.items():
            pygame.draw.circle(G.SCREEN, data[0], pos, data[1])
        for thing in self.other:
            self.screen.blit(thing[0], thing[1])
        pygame.display.update()

    def take_pic(self, imgname):
        """self.screen.fill(G.BGCOLOR)
        self.pendingevent()
        for pos, data in self.spots.items():
            pygame.draw.circle(G.SCREEN, data[0], pos, data[1])
        for thing in self.other2:
            if thing['type'] == 'line':
                pygame.draw.line(G.SCREEN, thing['color'], thing['pos1'], thing['pos2'], width=thing['width'])
            if thing['type'] == 'rect':
                pygame.draw.rect(G.SCREEN, thing['color'], pygame.Rect(thing['pos'][0], thing['pos'][1], thing['width'], thing['height']))
        for thing in self.other:
            self.screen.blit(thing[0], thing[1])
        pygame.display.update()"""
        self.draw()
        self.pending(pygame.image.save, (self.screen, imgname))

    def draw_no(self):
        """self.screen.fill(G.BGCOLOR)
        self.pendingevent()
        handler.draw_text((5, G.SCREEN_HEIGHT - 25), f'Current Width: {G.SPOT_WIDTH}', font='resources\\8-Bit-Madness')
        handler.draw_text((5, G.SCREEN_HEIGHT - 50), f'Color:', font='resources\\8-Bit-Madness')
        pygame.draw.rect(G.SCREEN, G.SELECTED_COLOR, pygame.Rect(60, G.SCREEN_HEIGHT - 50, G.BUTTON_WIDTH, G.BUTTON_HEIGHT))
        for thing in self.other2:
            if thing['type'] == 'line':
                pygame.draw.line(G.SCREEN, thing['color'], thing['pos1'], thing['pos2'], width=thing['width'])
            if thing['type'] == 'rect':
                pygame.draw.rect(G.SCREEN, thing['color'], pygame.Rect(thing['pos'][0], thing['pos'][1], thing['width'], thing['height']))
        for button in self.buttons:
            button.draw()
        for pos, data in self.spots.items():
            pygame.draw.circle(G.SCREEN, data[0], pos, data[1])
        for thing in self.other:
            self.screen.blit(thing[0], thing[1])
        pygame.display.update()"""
        self.draw()

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    dosave = gettextinput((5, G.SCREEN_HEIGHT - 150), self.screen, fontname='resources\\8-Bit-Madness', whilerunfunc=(self.draw_no, ()), other_text='Save Picture? (y/n) > ')
                    if dosave.lower() in ('y', 'yes', 'yup', 'yeah', 'please', 'plz', 'please do it', 'plz do it', 'much obliged', 'i\'d like that', 'id like that', 'thank you', 'thanks', 'thanks for doing it', 'thanks for doing that', 'please do that', 'plz do that', 'do that', 'do it', 'do', 'save', 'save picture', 'uh-huh', 'uhhuh', 'yah', 'sure', 'why not', 'why not?', 'go ahead', 'might as well', 'fine', 'now', 'hurry up', 'hurry'):
                        savename = gettextinput((5, G.SCREEN_HEIGHT - 150), self.screen, fontname='resources\\8-Bit-Madness', whilerunfunc=(self.draw_no, ()), other_text='Screenshot name > ')
                        self.take_pic(savename)
                    pygame.quit()
                    
            self.buttondown = bool(pygame.mouse.get_pressed()[0])

            if self.buttondown and not self.ignorefornow:
                if self.isvalidclick():
                        self.spots[pygame.mouse.get_pos()] = (G.SELECTED_COLOR, G.SPOT_WIDTH)
                        
            elif not self.buttondown and self.ignorefornow:
                self.ignorefornow = False

            self.draw()

    def isvalidclick(self):
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if pos[0] in range(button.rect.x, button.rect.x + button.rect.width) and pos[1] in range(button.rect.y, button.rect.y + button.rect.height):
                return False
        return True

    def pending(self, func, args):
        self.pendingevents.append((func, args))

    def pendingevent(self):
        for func, args in self.pendingevents:
            func(*args)
        self.pendingevents.clear()

def main():
    game = Game()
    game.loop()

if __name__ == '__main__':
    main()
