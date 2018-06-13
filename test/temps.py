import pygame
from pygame.locals import *
from datetime import timedelta, datetime, date, time
 
 
class Chrono:
    def __init__(self, position, font, color=(255, 255, 255)):
        self.chrono = datetime.combine(date.today(), time(0, 0))
        self.font = font
        self.color = color
        self.label = self._make_chrono_label()
        self.rect = self.label.get_rect(topleft=position)
 
    def _make_chrono_label(self):
        "Crée une Surface représentant le temps du chrono"
        return font.render(self.chrono.strftime("%H : %M : %S"),
                           True, self.color)
 
    def update(self, dt):
        """Mise à jour du temps écoulé.
 
        dt est le nombre de millisecondes
        """
        old_chrono = self.chrono
        self.chrono += timedelta(milliseconds=dt)
        # Comme le chrono n'indique pas les fractions de secondes,
        # on ne met à jour le label que si quelque chose de visible a changé
        if old_chrono.second != self.chrono.second:
            self.label = self._make_chrono_label()
 
    def draw(self, surface):
        surface.blit(self.label, self.rect)
         
 
if __name__ == "__main__":
    pygame.init()
 
    fen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Chrono")
      
    font = pygame.font.Font(None, 64)
    fps_clock = pygame.time.Clock()
 
    chrono = Chrono(position=(100, 70), font=font)
 
    running = True
    while running:
        for evenement in pygame.event.get():
            if evenement.type == QUIT:
                running = False
                 
        dt = fps_clock.tick(60)
        chrono.update(dt)      
 
        fen.fill(0)
        chrono.draw(fen)
        pygame.display.update()
 
    pygame.quit()