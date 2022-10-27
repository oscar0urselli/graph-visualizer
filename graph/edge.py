import pygame

class Edge(pygame.sprite.Sprite):
    def __init__(self, start, end, surf) -> None:
        self.weight = None
        self.start_pos = start
        self.end_pos = end
        self.color = (53, 172, 176)
        self.pos = end
        self.surf = surf
        self.is_connecting = True
        self.rect = None

        super(Edge, self).__init__()

    def update(self, pressed_keys):
        if self.is_connecting:
            pygame.draw.line(self.surf, self.color, self.start_pos, pygame.mouse.get_pos(), 10)
        else:
            self.rect = pygame.draw.line(self.surf, self.color, self.start_pos, self.end_pos, 10)
        
        if pressed_keys[pygame.K_UP]:
            self.pos.move_ip(0, 2)
        if pressed_keys[pygame.K_DOWN]:
            self.pos.move_ip(0, -2)
        if pressed_keys[pygame.K_LEFT]:
            self.pos.move_ip(2, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.pos.move_ip(-2, 0)