import pygame

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, id) -> None:
        self.radius = 16
        self.id = id
        self.color = (0, 0, 255)
        self.surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        #self.surf.set_colorkey((0, 0, 0))
        self.pos = pygame.Rect(tuple(map(lambda c: c - self.radius, pos)), (32, 32))


        super(Node, self).__init__()
        pygame.draw.circle(self.surf, (0, 0, 0), (20, 20), 20)
        self.rect = pygame.draw.circle(self.surf, (0, 0, 255), (20, 20), self.radius)

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.pos.move_ip(0, 2)
        if pressed_keys[pygame.K_DOWN]:
            self.pos.move_ip(0, -2)
        if pressed_keys[pygame.K_LEFT]:
            self.pos.move_ip(2, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.pos.move_ip(-2, 0)