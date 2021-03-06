import pygame as pg

color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
color_name_saved = pg.Color('lightgreen')


class InputBox:

    def __init__(self, x, y, w, h, font, text):
        self.rect = pg.Rect(x, y, w, h)
        self.color = color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event, char):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            # if click on inputbox, delete text
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.text = ""
                self.txt_surface = self.font.render(self.text, True, self.color)
            else:
                self.active = False
            # input box change color
            if self.active is True:
                self.color = color_active
            else:
                self.color = color_inactive
        # get inputs and add to text
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    char.name = self.text
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) <= 8:
                        self.text += event.unicode
                # if text == char.name display other color
                if self.text is char.name:
                    self.color = color_name_saved
                else:
                    self.color = color_active
                self.txt_surface = self.font.render(self.text, True, self.color)

    def resize(self):
        # resize input box if text too long
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # blit text
        screen.blit(self.txt_surface, (
            self.rect.x + self.rect.width / 2 - self.txt_surface.get_width() / 2, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)