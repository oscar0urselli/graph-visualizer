import math
import time
import json

import pygame
import pygame_gui

from graph.node import Node
from graph.edge import Edge
from graph.algos import DFS, BFS
import graph.utils



settings = graph.utils.init_settings()

pygame.init()
pygame.display.set_caption('Graph Visualizer')

SCREEN_SIZE = pygame.display.get_desktop_sizes()[0]
MODES = {
    pygame.K_ESCAPE: 'KILL',
    pygame.K_e: 'ADD EDGE',
    pygame.K_n: 'ADD NODE'
}
screen = pygame.display.set_mode()
application_bar = pygame.Surface((SCREEN_SIZE[0], 36))
application_bar.fill((105, 42, 26))
workspace = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1] - 36))
workspace.fill((135, 94, 81))


node_counter = 0
to_change_color = []
dont_change_color = None
delay = 1
start_time = 0
G = {}
nodes = []
edges = []

mode = 'ADD NODE'
start_node, end_node = None, None
end_pos, start_pos = None, None

ui_manager = pygame_gui.UIManager(SCREEN_SIZE)

file_btn = pygame_gui.elements.UIButton(
    relative_rect = pygame.Rect((0, 0), (72, 36)),
    text = 'File',
    manager = ui_manager
)
settings_btn = pygame_gui.elements.UIButton(
    relative_rect = pygame.Rect((72, 0), (100, 36)),
    text = 'Settings',
    manager = ui_manager
)
help_btn = pygame_gui.elements.UIButton(
    relative_rect = pygame.Rect((172, 0), (72, 36)),
    text = 'Help',
    manager = ui_manager
)
info_panel = pygame_gui.elements.UIPanel(
    relative_rect = pygame.Rect((1500, 100), (300, 800)),
    starting_layer_height = 1,
    manager = ui_manager,
    visible = 0,
)
info_panel_title = pygame_gui.elements.UITextBox(
    relative_rect = pygame.Rect((0, 0), (294, 36)),
    html_text = 'Object inspector',
    manager = ui_manager,
    container = info_panel
)
info_panel_type = pygame_gui.elements.UILabel(
    relative_rect = pygame.Rect((0, 50), (294, 36)),
    text = '',
    manager = ui_manager,
    container = info_panel
)
info_panel_id = pygame_gui.elements.UILabel(
    relative_rect = pygame.Rect((0, 90), (294, 36)),
    text = '',
    manager = ui_manager,
    container = info_panel
)


clock = pygame.time.Clock()

while mode != 'KILL':
    time_delta = clock.tick(settings['graphics']['fps']) / 1000
    for event in pygame.event.get():
        posx, posy = pygame.mouse.get_pos()
        pos = (posx, posy - 36)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            pass

        if event.type == pygame.QUIT:
            mode = 'KILL'
        if event.type == pygame.KEYDOWN:
            try:
                mode = MODES[event.key]
            except KeyError:
                pass
            
            if len(nodes) > 0:
                if event.key == pygame.K_d:
                    to_change_color = DFS(G).DFS()
                    start_time = time.time()
                elif event.key == pygame.K_b:
                    to_change_color = BFS(G).BFS()
                    start_time = time.time()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if mode == 'ADD NODE' and pos[1] > 0:
                    nodes.append(Node(pos, str(node_counter)))
                    G[str(node_counter)] = []
                    node_counter += 1
                    workspace.blit(nodes[-1].surf, pos)
                elif mode == 'ADD EDGE':
                    if start_pos == None:
                        for o in nodes:
                            if o.pos.collidepoint(pos):
                                start_pos = o.pos.center
                                start_node = o.id
                                edges.append(Edge(start_pos, start_pos, workspace))
                                break
                    elif end_pos == None:
                        for o in nodes:
                            if o.pos.collidepoint(pos) and o.id != start_node:
                                end_pos = o.pos.center
                                end_node = o.id
                                edges[-1].is_connecting = False
                                edges[-1].end_pos = end_pos
                                edges[-1].start_node = start_node
                                edges[-1].end_node = end_node

                                # Add check if bidirectional
                                G[start_node].append(end_node)
                                G[end_node].append(start_node)
                        
                                start_pos, end_pos = None, None
                                start_node, end_node = None, None
                                break
            elif pygame.mouse.get_pressed()[1]:
                show = False
                for o in nodes:
                    if o.pos.collidepoint(pos):
                        show = True

                        info_panel_type.set_text('Type: Node')
                        info_panel_id.set_text('Id: ' + o.id)

                        info_panel.show()
                
                if not show:
                    info_panel.hide()                    
            elif pygame.mouse.get_pressed()[2]:
                if mode == 'ADD EDGE' and start_pos != None and end_pos == None:
                    edges.pop()
                    start_pos = None
                else:
                    node_index = None
                    for i, o in enumerate(nodes):
                        if o.pos.collidepoint(pos):
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
                        for g in G:
                            try:
                                G[g].remove(nodes[node_index].id)
                            except ValueError:
                                pass
                        G.pop(nodes[node_index].id)
                        nodes.pop(node_index)

        ui_manager.process_events(event)
    
    ui_manager.update(time_delta)

    pressed_keys = pygame.key.get_pressed()

        
    screen.blit(application_bar, (0, 0))
    screen.blit(workspace, (0, 36))
    workspace.fill((135, 94, 81))
    for y in range(math.ceil(SCREEN_SIZE[1] / settings['bg']['square_size'])):
        for x in range(math.ceil(SCREEN_SIZE[0] / settings['bg']['square_size'])):
            square = pygame.Surface((settings['bg']['square_size'], settings['bg']['square_size']))
            square.fill((28, 27, 27))
            workspace.blit(square, ((settings['bg']['square_size'] + settings['bg']['line_thickness']) * x, (settings['bg']['square_size'] + settings['bg']['line_thickness']) * y))
    
    for e in edges:
        e.update(pressed_keys)

    for o in nodes:
        if time.time() - start_time >= delay and start_time != 0:
            try:
                if o.id == to_change_color[0]:
                    o.color = (255, 0, 0)
                    start_time = time.time()
                    dont_change_color = to_change_color.pop(0)
            except IndexError:
                start_time = 0

        if o.id != dont_change_color:
            o.color = (0, 0, 255)
        o.update(pressed_keys)
        workspace.blit(o.surf, o.pos)

    ui_manager.draw_ui(screen)

    # pygame.disply.update(list_of_rect_to_update)
    pygame.display.flip()

pygame.quit()