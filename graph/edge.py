import pygame

class Edge(pygame.sprite.Sprite):
    def __init__(self, start, end, surf) -> None:
        self.weight = None
        self.start_node = None
        self.end_node = None
        self.is_bidirectional = True

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
            self.start_pos = (self.start_pos[0], self.start_pos[1] + 2)
            self.end_pos = (self.end_pos[0], self.end_pos[1] + 2)
        if pressed_keys[pygame.K_DOWN]:
            self.start_pos = (self.start_pos[0], self.start_pos[1] - 2)
            self.end_pos = (self.end_pos[0], self.end_pos[1] - 2)
        if pressed_keys[pygame.K_LEFT]:
            self.start_pos = (self.start_pos[0] + 2, self.start_pos[1])
            self.end_pos = (self.end_pos[0] + 2, self.end_pos[1])
        if pressed_keys[pygame.K_RIGHT]:
            self.start_pos = (self.start_pos[0] - 2, self.start_pos[1])
            self.end_pos = (self.end_pos[0] - 2, self.end_pos[1])