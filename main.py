import time
import os

import pygame
import pygame_gui

from graph.node import Node
from graph.edge import Edge
from graph.algos import DFS, BFS
from graph.gui import UIWidget
import graph.utils



settings = graph.utils.init_settings()

pygame.init()
pygame.display.set_caption('Graph Visualizer')
pygame.display.set_icon(pygame.image.load('assets/icons/32x32/icon-32x32.png'))

SCREEN_SIZE = pygame.display.get_desktop_sizes()[0]
TOP_BAR_HEIGHT = 36

screen = pygame.display.set_mode()
application_bar = pygame.Surface((SCREEN_SIZE[0], TOP_BAR_HEIGHT))
application_bar.fill((105, 42, 26))
workspace = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1] - TOP_BAR_HEIGHT))
workspace.fill((135, 94, 81))

DMZS = [
    pygame.Rect((0, -TOP_BAR_HEIGHT), (SCREEN_SIZE[0], TOP_BAR_HEIGHT)),
    pygame.Rect((0, 75), (115, 375))
]


node_counter = 0
to_change_color = []
dont_change_color = None
start_time = 0
G = {}
nodes = []
edges = []

mode = 'ADD NODE'
bidirectional_edge = None
start_node, end_node = None, None
end_pos, start_pos = None, None
delay = 1.0

ui_manager = pygame_gui.UIManager(SCREEN_SIZE, 'theme.json')
topbar = UIWidget('./assets/views/top-bar.xml', SCREEN_SIZE, ui_manager).parse()
tools_bar = UIWidget('./assets/views/tools-bar.xml', SCREEN_SIZE, ui_manager).parse()
node_inspector = UIWidget('./assets/views/node-inspector.xml', SCREEN_SIZE, ui_manager).parse()
edge_inspector = UIWidget('./assets/views/edge-inspector.xml', SCREEN_SIZE, ui_manager).parse()
run_algos = UIWidget('./assets/views/run-algos.xml', SCREEN_SIZE, ui_manager).parse()

clock = pygame.time.Clock()

while mode != 'KILL':
    time_delta = clock.tick(settings['graphics']['fps']) / 1000
    for event in pygame.event.get():
        posx, posy = pygame.mouse.get_pos()
        pos = (posx, posy - TOP_BAR_HEIGHT)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == tools_bar['add_node_btn']:
                mode = 'ADD NODE'
            elif event.ui_element == tools_bar['add_undirected_edge_btn']:
                mode = 'ADD EDGE'
                bidirectional_edge = True
            elif event.ui_element == tools_bar['add_directed_edge_btn']:
                mode = 'ADD EDGE'
                bidirectional_edge = False
            elif event.ui_element == tools_bar['run_algos_btn']:
                if mode == 'RUN ALGOS':
                    run_algos['select_panel'].hide()
                    mode = ''
                else:
                    mode = 'RUN ALGOS'
                    run_algos['select_panel'].show()
            elif event.ui_element == run_algos['run_btn']:
                if run_algos['algos_selection'].selected_option == 'DFS':
                    to_change_color = DFS(G).DFS()
                elif run_algos['algos_selection'].selected_option == 'BFS':
                    to_change_color = BFS(G).BFS()
                elif run_algos['algos_selection'].selected_option == 'Dijkstra':
                    pass
                start_time = time.time()
                mode = ''
            elif event.ui_element == topbar['minimize_btn']:
                pygame.display.iconify()
            elif event.ui_element == topbar['close_btn']:
                mode = 'KILL'
            elif event.ui_element == run_algos['select_panel'].close_window_button:
                mode = ''

        if event.type == pygame.QUIT:
            mode = 'KILL'
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and not graph.utils.mouse_in_dmz(DMZS, pos):
                if mode == 'ADD NODE':
                    nodes.append(Node(pos, str(node_counter)))
                    G[str(node_counter)] = {}
                    node_counter += 1
                    workspace.blit(nodes[-1].surf, pos)
                elif mode == 'ADD EDGE':
                    if start_pos == None:
                        for o in nodes:
                            if o.pos.collidepoint(pos):
                                start_pos = o.pos.center
                                start_node = o.id
                                edges.append(Edge(start_pos, start_pos, workspace))
                                edges[-1].is_bidirectional = bidirectional_edge
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

                                G[start_node][end_node] = 0
                                if bidirectional_edge:
                                    G[end_node][start_node] = 0
                        
                                start_pos, end_pos = None, None
                                start_node, end_node = None, None
                                break
            elif pygame.mouse.get_pressed()[1]:
                show = False
                for o in nodes:
                    if o.pos.collidepoint(pos):
                        show = True

                        node_inspector['id'].html_text = 'Id: ' + o.id
                        node_inspector['id'].rebuild()

                        node_inspector['color'].html_text = 'Color: ' + str(o.color)
                        node_inspector['color'].rebuild()

                        node_inspector['neighbours'].html_text = 'Neighbours: { ' + ', '.join([i[0] + ': ' + str(i[1]) for i in G[o.id].items()]) + ' }'
                        node_inspector['neighbours'].rebuild()

                        node_inspector['node-inspector'].show()
                        edge_inspector['edge-inspector'].hide()

                        break
                if not show:
                    for e in edges:
                        if e.rect.collidepoint(pos):
                            show = True

                            edge_inspector['color'].html_text = 'Color: ' + str(e.color)
                            edge_inspector['color'].rebuild()

                            edge_inspector['way'].html_text = e.start_node + (' <-> ' if e.is_bidirectional else ' --> ') + e.end_node
                            edge_inspector['way'].rebuild()

                            edge_inspector['weight'].set_text(str(e.weight))

                            edge_inspector['edge-inspector'].show()
                            node_inspector['node-inspector'].hide()

                            break
                
                if not show:
                    node_inspector['node-inspector'].hide()
                    edge_inspector['edge-inspector'].hide()
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
                                G[g].pop(nodes[node_index].id)
                            except KeyError:
                                pass
                        G.pop(nodes[node_index].id)
                        nodes.pop(node_index)
                        node_inspector['node-inspector'].hide()
                    
                    edge_node = None
                    edge_index = None
                    for i, e in enumerate(edges):
                        if e.rect.collidepoint(pos):
                            edge_node = (e.start_node, e.end_node)
                            edge_index = i
                    if edge_node != None:
                        try:
                            G[edge_node[0]].pop(edge_node[1])
                            if edges[edge_index].is_bidirectional:
                                G[edge_node[1]].pop(edge_node[0])
                            edges.pop(edge_index)
                            edge_inspector['edge-inspector'].hide()
                        except KeyError:
                            pass

        ui_manager.process_events(event)
    
    ui_manager.update(time_delta)

    pressed_keys = pygame.key.get_pressed()

        
    screen.blit(application_bar, (0, 0))
    screen.blit(workspace, (0, TOP_BAR_HEIGHT))
    workspace.fill((28, 27, 27))

    # Update UI
    if run_algos['delay_slider'].get_current_value() != delay:
        delay = run_algos['delay_slider'].get_current_value()
        run_algos['delay_text_box'].html_text = 'Delay: ' + str(round(delay, 2)) + ' s'
        run_algos['delay_text_box'].rebuild()

    if run_algos['algo_name'].html_text != run_algos['algos_selection'].selected_option:
        run_algos['algo_name'].html_text = run_algos['algos_selection'].selected_option
        run_algos['algo_name'].rebuild()

    if mode == 'RUN ALGOS':
        if run_algos['algos_selection'].selected_option == 'DFS':
            run_algos['dfs_panel'].show()
            run_algos['bfs_panel'].hide()
            run_algos['dijkstra_panel'].hide()
        elif run_algos['algos_selection'].selected_option == 'BFS':
            run_algos['bfs_panel'].show()
            run_algos['dfs_panel'].hide()
            run_algos['dijkstra_panel'].hide()
        elif run_algos['algos_selection'].selected_option == 'Dijkstra':
            run_algos['dijkstra_panel'].show()
            run_algos['dfs_panel'].hide()
            run_algos['bfs_panel'].hide()
    
    # Update edges
    for e in edges:
        e.update(pressed_keys)
    # Update nodes
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