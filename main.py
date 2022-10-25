import pygame



class Node(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        self.weight = None
        self.edges = {}
        self.name = ""
        self.color = (0, 0, 255)
        self.surf = pygame.Surface((32, 32))
        self.surf.fill((255, 255, 255))
        self.pos = pygame.Rect(pos, (32, 32))


        super(Node, self).__init__()
        self.rect = pygame.draw.circle(self.surf, (0, 0, 255), (16, 16), 16)

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.pos.move_ip(0, 2)
        if pressed_keys[pygame.K_DOWN]:
            self.pos.move_ip(0, -2)
        if pressed_keys[pygame.K_LEFT]:
            self.pos.move_ip(2, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.pos.move_ip(-2, 0)

pygame.init()

screen = pygame.display.set_mode()

objects = []


screen.fill((255, 255, 255))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                objects.append(Node(pos))
                screen.blit(objects[-1].surf, pos)

    
    pressed_keys = pygame.key.get_pressed()

    screen.fill((255, 255, 255))

    for o in objects:
        o.update(pressed_keys)
        screen.blit(o.surf, o.pos)

    pygame.display.flip()

pygame.quit()