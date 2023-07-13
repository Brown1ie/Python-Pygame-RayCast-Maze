from settings import *
import pygame
import math
import gc





# AnimationLogic class
class AnimationLogic:
    def __init__(self, images, animation_speed,game):
        self.images = images
        self.animation_speed = animation_speed
        self.last_image_change_time = 0
        self.index = 0
        self.running = False
        self.game = game

    def start_animation(self):
        self.running = True

    def stop_animation(self):
        self.running = False

    def update_animation(self, player_pos):
        if not self.running:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_image_change_time >= self.animation_speed:
            self.index += 1
            if self.index == 14:
                hit_detection(player_pos, self.game.map.world_map)
            if self.index >= len(self.images):
                self.index = 0
                self.stop_animation()
            self.last_image_change_time = current_time

    def render(self, screen, position):
        if self.running:
            screen.blit(self.images[self.index], position)


class Hammer:
    def __init__(self, max_uses, game):
        self.max_uses = max_uses
        self.current_uses = max_uses
        self.swing_animation = None
        self.swing_images = []
        self.game = game

        for num in range(14):
            img = pygame.image.load(f"Swing\\{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT)).convert_alpha()
            self.swing_images.append(img)

        for num in range(14, -1, -1):
            img = pygame.image.load(f"Swing\\{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT)).convert_alpha()
            self.swing_images.append(img)

        self.hammer_image = pygame.image.load("IDLE.png").convert_alpha()
        self.hammer_image = pygame.transform.scale(self.hammer_image, (WIDTH, HEIGHT)).convert_alpha()
        self.hammer_width, self.hammer_height = self.hammer_image.get_size()

    def use(self):
        if self.current_uses > 0 and not self.swing_animation:
            self.swing_animation = AnimationLogic(self.swing_images, animation_speed, self.game)
            self.swing_animation.start_animation()
            self.current_uses -= 1

    def render(self, screen):
        if self.swing_animation:
            self.swing_animation.update_animation(self.game.player.pos)
            self.swing_animation.render(screen, (WIDTH // 2 - self.hammer_width // 2, HEIGHT // 2 - self.hammer_height // 2))

            if not self.swing_animation.running:
                self.swing_animation = None
        else:
            screen.blit(self.hammer_image, (WIDTH // 2 - self.hammer_width // 2, HEIGHT // 2 - self.hammer_height // 2))

def render_text(screen, text, position):
    try:
        self.dmfont = "dmfont.ttf"
        self.CustomFont=pygame.font.Font(self.dmfont, 12)
    except:
        self.dmfont = None
        self.CustomFont=pygame.font.Font(self.dmfont,24)
    text_surface = CustomFont.render(text, True, (255, 255, 255))
    screen.blit(text_surface, position)

def hit_detection(player_pos, world_map):
    # Get the player's map coordinates
    player_x = int(player_pos[0])
    player_y = int(player_pos[1])

    # Check the surrounding area for breakable walls
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            x = player_x + dx
            y = player_y + dy

            # Check if the coordinates are within the map boundaries
            if 0 <= x < len(world_map[0]) and 0 <= y < len(world_map):
                if world_map[y][x] == 2:
                    # Replace the breakable wall with an empty space
                    world_map[y][x] = 0

                    # Print the coordinates of the destroyed wall
                    print(f"Destroyed breakable wall at coordinates: ({x}, {y})")

    print(player_pos)


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle= PLAYER_ANGLE


    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx += speed * cos_a
            dy += speed * sin_a
        if keys[pygame.K_s]:
            dx += -speed * cos_a
            dy += -speed * sin_a

        if keys[pygame.K_d]:
            dx += -speed * sin_a
            dy += speed * cos_a

        if keys[pygame.K_a]:
            dx += speed * sin_a
            dy += -speed * cos_a

        self.check_wall_collision(dx, dy)

##        if keys [pygame.K_LEFT]:
##            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
##        if keys [pygame.K_RIGHT]:
##            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau          #tau = 2*pi

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        #pygame.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #                 (self.x * 100 + WIDTH * math.cos(self.angle),
        #                  self.y * 100 + WIDTH * math.sin(self.angle)),2)
        pygame.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100),15)

    def mouse_control(self):
        mx, my = pygame.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
            
        
    def update(self):
        self.movement()
        self.mouse_control()


    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
