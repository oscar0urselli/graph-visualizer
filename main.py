import pygame

from graph.node import Node
from graph.edge import Edge


pygame.init()
pygame.display.set_caption('Graph Visualizer')

screen = pygame.display.set_mode((800, 800))

nodes = []
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
                    nodes.append(Node(pos))
                    screen.blit(nodes[-1].surf, pos)
                elif mode == 'ADD EDGE':
                    if start_pos == None:
                        for o in nodes:
                            if o.pos.collidepoint(pygame.mouse.get_pos()):
                                start_pos = o.pos.center
                                edges.append(Edge(start_pos, start_pos, screen))
                                break
                    elif end_pos == None:
                        for o in nodes:
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
                    node_index = None
                    for i, o in enumerate(nodes):
                        if o.pos.collidepoint(pygame.mouse.get_pos()):
                            node_index = i
                    edges_index = []
                    for i, e in enumerate(edges):
                        try:
                            if e.start_pos == nodes[node_index].pos.center or e.end_pos == nodes[node_index].pos.center:
                                edges_index.append(i)
                        except TypeError:
                            break
                    edges_index = sorted(edges_index, reverse = True)
                    for i in edges_index:
                        edges.pop(i)
                    if node_index != None:
                        nodes.pop(node_index)
    
    pressed_keys = pygame.key.get_pressed()

    screen.fill((80, 80, 80))

    for e in edges:
        e.update(pressed_keys)

    for o in nodes:
        o.update(pressed_keys)
        screen.blit(o.surf, o.pos)


    pygame.display.flip()

pygame.quit()