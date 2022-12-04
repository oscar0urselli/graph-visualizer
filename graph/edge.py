import pygame
import math

class Edge(pygame.sprite.Sprite):
    def __init__(self, start, end, surf) -> None:
        self.weight = 0
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
            posx, posy = pygame.mouse.get_pos()
            pos = (posx, posy - 36)
            pygame.draw.line(self.surf, self.color, self.start_pos, pos, 10)
            
            if not self.is_bidirectional:
                pygame.draw.polygon(self.surf, self.color, self.arrow_points(self.start_pos, pos, 50))
        else:
            self.rect = pygame.draw.line(self.surf, self.color, self.start_pos, self.end_pos, 10)
            if not self.is_bidirectional:
                pygame.draw.polygon(self.surf, self.color, self.arrow_points(self.start_pos, self.end_pos, 50))

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

    def arrow_points(self, A, B, l) -> "tuple[tuple[float, float], tuple[float, float], tuple[float, float]]":
        AB = math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)
        theta = math.asin(math.sqrt((A[1] - B[1]) ** 2) / AB)
        R = l

        if A[0] < B[0]:
            if A[1] < B[1]:
                theta *= -1
        else:
            if A[1] > B[1]:
                theta *= -1

        alpha1 = math.radians(150) if A[0] < B[0] else math.radians(30)
        alpha2 = math.radians(210) if A[0] < B[0] else math.radians(330)
        gamma1 = (alpha1 - theta) % (2 * math.pi)
        gamma2 = (alpha2 - theta) % (2 * math.pi)

        x1 = B[0] + R * math.cos(gamma1)
        y1 = B[1] + R * math.sin(gamma1)

        x2 = B[0] + R * math.cos(gamma2)
        y2 = B[1] + R * math.sin(gamma2)

        return ((x1, y1), (x2, y2), B)