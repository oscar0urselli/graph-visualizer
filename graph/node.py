import pygame
import uuid

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, id) -> None:
        self.uuid = uuid.uuid4()
        self.type = 'Node'
        
        self.radius = 16
        self.id = id
        self.__color = (0, 0, 255)
        self.color = self.__color
        self.surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        #self.surf.set_colorkey((0, 0, 0))
        self.pos = pygame.Rect(tuple(map(lambda c: c - self.radius, pos)), (32, 32))


        super(Node, self).__init__()
        pygame.draw.circle(self.surf, (0, 0, 0), (20, 20), 20)
        self.rect = pygame.draw.circle(self.surf, self.color, (20, 20), self.radius)

        self.font = pygame.font.SysFont(None, 24)
        self.txt = self.font.render(self.id, True, (255, 255, 255))

        w0, h0 = self.txt.get_size()
        self.surf.blit(self.txt, ((40 - w0) / 2, (40 - h0) / 2))


    def update(self, pressed_keys):
        if self.__color != self.color:
            self.__color = self.color
            self.rect = pygame.draw.circle(self.surf, self.color, (20, 20), self.radius)
            w0, h0 = self.txt.get_size()
            self.surf.blit(self.txt, ((40 - w0) / 2, (40 - h0) / 2))

        if pressed_keys[pygame.K_UP]:
            self.pos.move_ip(0, 2)
        if pressed_keys[pygame.K_DOWN]:
            self.pos.move_ip(0, -2)
        if pressed_keys[pygame.K_LEFT]:
            self.pos.move_ip(2, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.pos.move_ip(-2, 0)