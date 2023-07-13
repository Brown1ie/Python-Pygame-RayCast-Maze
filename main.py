import pygame
import sys
from settings import *
from player import *
from raycasting import *

#need to remake the map maker and reimplement it  done ish
#need to readd the animations  done just gotta write about it
#need to test out with mazemode  done
def render_text(screen, text, position):
    try:
        dmfont = "dmfont.ttf"
        CustomFont=pygame.font.Font(dmfont, 12)
    except:
        dmfont = None
        CustomFont=pygame.font.Font(dmfont,24)
    text_surface = CustomFont.render(text, True, (255, 255, 255))
    screen.blit(text_surface, position)
class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen=pygame.display.set_mode(RES)
        self.clock=pygame.time.Clock()
        self.delta_time = 1
        self.new_game()
        

        
    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer=ObjectRenderer(self)
        self.raycasting=RayCasting(self)
        self.hammer=Hammer(max_uses, self)
        
    def update(self):
        self.player.update()
        self.raycasting.update()
        pygame.display.flip()
        self.delt_time=self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill((128, 128, 128))  # Fills floor
        self.screen.fill((80, 80, 80), (0, 0, WIDTH, HEIGHT // 2))  # Fills sky
        
        self.object_renderer.draw()
        self.hammer.render(self.screen)
        self.uses_text = f"Hammer Uses: {self.hammer.current_uses}/{max_uses}"
        render_text(self.screen, self.uses_text, (10,10))
        #self.map.draw()
        #self.player.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                self.hammer.use()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game=Game()
    game.run()
            

            

