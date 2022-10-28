import math

import pygame

from graph.node import Node
from graph.edge import Edge



pygame.init()
pygame.display.set_caption('Graph Visualizer')

SCREEN_SIZE = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode()

node_counter = 0
G = {}
nodes = []
edges = []

running = True
mode = 'ADD NODE'
start_pos = None
start_node = None
end_pos = None
end_node = None

grid_offset = (0, 0)
line_thickness = 10
square_size = 200
bg_primary_color = (20, 20, 20)
bg_secondary_color = (80, 80, 80)


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
                    nodes.append(Node(pos, str(node_counter)))
                    G[str(node_counter)] = []
                    node_counter += 1
                    screen.blit(nodes[-1].surf, pos)
                elif mode == 'ADD EDGE':
                    if start_pos == None:
                        for o in nodes:
                            if o.pos.collidepoint(pygame.mouse.get_pos()):
                                start_pos = o.pos.center
                                start_node = o.value
                                edges.append(Edge(start_pos, start_pos, screen))
                                break
                    elif end_pos == None:
                        for o in nodes:
                            if o.pos.collidepoint(pygame.mouse.get_pos()) and o.value != start_node:
                                end_pos = o.pos.center
                                end_node = o.value
                                edges[-1].is_connecting = False
                                edges[-1].end_pos = end_pos
                                edges[-1].start_node = start_node
                                edges[-1].end_node = end_node
                                # Add the weight of the edge

                                # Add checking if bidirectional
                                G[start_node].append(end_node)
                                G[end_node].append(start_node)
                        
                                start_pos, end_pos = None, None
                                start_node, end_node = None, None
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


    screen.fill(bg_secondary_color)
    for y in range(math.ceil(SCREEN_SIZE[1] / square_size)):
        for x in range(math.ceil(SCREEN_SIZE[0] / square_size)):
            square = pygame.Surface((square_size, square_size))
            square.fill(bg_primary_color)
            screen.blit(square, ((square_size + line_thickness) * x, (square_size + line_thickness) * y))

    for e in edges:
        e.update(pressed_keys)

    for o in nodes:
        o.update(pressed_keys)
        screen.blit(o.surf, o.pos)


    pygame.display.flip()

pygame.quit()