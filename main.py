import pygame



class Node(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        self.radius = 16
        self.value = None
        self.name = ""
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


pygame.init()

screen = pygame.display.set_mode((800, 800))

objects = []
edges = []


running = True
mode = 'ADD NODE'
start_pos = None
end_pos = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_e:
                mode = 'ADD EDGE'
            elif event.key == pygame.K_n:
                mode = 'ADD NODE'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if mode == 'ADD NODE':
                    pos = pygame.mouse.get_pos()
                    objects.append(Node(pos))
                    screen.blit(objects[-1].surf, pos)
                elif mode == 'ADD EDGE':
                    if start_pos == None:
                        for o in objects:
                            if o.pos.collidepoint(pygame.mouse.get_pos()):
                                start_pos = o.pos.center
                                edges.append(Edge(start_pos, start_pos, screen))
                                break
                    elif end_pos == None:
                        for o in objects:
                            if o.pos.collidepoint(pygame.mouse.get_pos()):
                                end_pos = o.pos.center
                                edges[-1].is_connecting = False
                                edges[-1].end_pos = end_pos
                        
                                start_pos, end_pos = None, None
                                break
            elif pygame.mouse.get_pressed()[2]:
                if mode == 'ADD EDGE' and start_pos != None and end_pos == None:
                    edges.pop()
                    start_pos = None
                else:
                    index = None
                    for i, o in enumerate(objects):
                        if o.pos.collidepoint(pygame.mouse.get_pos()):
                            index = i
                    if index != None:
                        objects.pop(index)
    
    pressed_keys = pygame.key.get_pressed()

    screen.fill((80, 80, 80))

    for e in edges:
        e.update(pressed_keys)

    for o in objects:
        o.update(pressed_keys)
        screen.blit(o.surf, o.pos)


    pygame.display.flip()

pygame.quit()