import time

import pygame
import pygame_gui

from graph.node import Node
from graph.edge import Edge
from graph.algos import DFS, BFS, Dijkstra
from graph.gui import UIWidget
import graph.utils



settings = graph.utils.init_settings()

pygame.init()
pygame.display.set_caption('Graph Visualizer')
pygame.display.set_icon(pygame.image.load('assets/icons/32x32/icon-32x32.png'))

SCREEN_SIZE = pygame.display.get_desktop_sizes()[0]

screen = pygame.display.set_mode()
workspace = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]))
workspace.fill((135, 94, 81))

DMZS = [
    pygame.Rect((0, 75), (115, 375))
]


node_counter = 0
to_change_color = []
dont_change_color = (None, None)
start_time = 0
G = {}
nodes = []
edges = []

mode = 'ADD NODE'
bidirectional_edge = None
start_node = None
delay = 1.0
focused_obj = None

ui_manager = pygame_gui.UIManager(SCREEN_SIZE, 'theme.json')
top_bar = UIWidget('./assets/views/top-bar.xml', SCREEN_SIZE, ui_manager).parse()
tools_bar = UIWidget('./assets/views/tools-bar.xml', SCREEN_SIZE, ui_manager).parse()
node_inspector = UIWidget('./assets/views/node-inspector.xml', SCREEN_SIZE, ui_manager).parse()
edge_inspector = UIWidget('./assets/views/edge-inspector.xml', SCREEN_SIZE, ui_manager).parse()
run_algos = UIWidget('./assets/views/run-algos.xml', SCREEN_SIZE, ui_manager).parse()

clock = pygame.time.Clock()

while mode != 'KILL':
    time_delta = clock.tick(settings['graphics']['fps']) / 1000
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

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
                if run_algos['select_panel'].visible:
                    run_algos['select_panel'].hide()
                else:
                    run_algos['select_panel'].show()
            elif event.ui_element == run_algos['run_btn']:
                if run_algos['algos_selection'].selected_option == 'DFS':
                    to_change_color = DFS(G).DFS()
                elif run_algos['algos_selection'].selected_option == 'BFS':
                    to_change_color = BFS(G).BFS()
                elif run_algos['algos_selection'].selected_option == 'Dijkstra':
                    start = run_algos['start_node'].get_text()
                    end = run_algos['end_node'].get_text()
                    
                    if start not in G or end not in G:
                        continue
                    
                    to_change_color = Dijkstra(G).Dijkstra(start, end)
                start_time = time.time()
            elif event.ui_element == top_bar['minimize_btn']:
                pygame.display.iconify()
            elif event.ui_element == top_bar['close_btn']:
                mode = 'KILL'
            elif event.ui_element == run_algos['select_panel'].close_window_button:
                pass

        if event.type == pygame.QUIT:
            mode = 'KILL'

        if event.type == pygame.MOUSEBUTTONDOWN and graph.utils.can_click(run_algos, node_inspector, edge_inspector, top_bar, pos) and not graph.utils.mouse_in_dmz(DMZS, pos):
            if pygame.mouse.get_pressed()[0]: # Add object
                if mode == 'ADD NODE':
                    nodes.append(Node(pos, str(node_counter)))
                    G[str(node_counter)] = {}
                    node_counter += 1
                    workspace.blit(nodes[-1].surf, pos)
                elif mode == 'ADD EDGE':
                        for o in nodes:
                            if o.pos.collidepoint(pos):
                                if start_node == None:
                                    start_node = o.id
                                    edges.append(Edge(o.pos.center, o.pos.center, workspace))
                                    edges[-1].is_bidirectional = bidirectional_edge
                                else:
                                    edges[-1].is_connecting = False
                                    edges[-1].end_pos = o.pos.center
                                    edges[-1].start_node = start_node
                                    edges[-1].end_node = o.id

                                    G[start_node][o.id] = 0
                                    if bidirectional_edge:
                                        G[o.id][start_node] = 0
                        
                                    start_node = None
                                break
            elif pygame.mouse.get_pressed()[1]: # Object inspector
                node_inspector['node-inspector'].hide()
                edge_inspector['edge-inspector'].hide()

                _rect = None
                for i, o in enumerate(nodes + edges):
                    if o.type == 'Node':
                        _rect = o.pos.collidepoint(pos)
                    else:
                        _rect = o.rect.collidepoint(pos)
                    if _rect:
                        focused_obj = i if o.type == 'Node' else i - len(nodes)
                        if o.type == 'Node':
                            graph.utils.update_node_inspector(node_inspector, edge_inspector, o, G)
                        else:
                            graph.utils.update_edge_inspector(edge_inspector, node_inspector, o, G)
                        break                    
            elif pygame.mouse.get_pressed()[2]: # Delete object
                if mode == 'ADD EDGE' and start_node != None:
                    edges.pop()
                    start_pos = None
                else:
                    for i, o in enumerate(nodes):
                        if o.pos.collidepoint(pos):
                            e = 0
                            while e < len(edges):
                                if edges[e].start_pos == o.pos.center or edges[e].end_pos == o.pos.center:
                                    edges.pop(e)
                                else:
                                    e += 1
                            for g in G:
                                try:
                                    G[g].pop(o.id)
                                except KeyError:
                                    pass
                            G.pop(o.id)
                            nodes.pop(i)
                            if focused_obj == i:
                                node_inspector['node-inspector'].hide()
                            break
                    for i, e in enumerate(edges):
                        if e.rect.collidepoint(pos):
                            try:
                                G[e.start_node].pop(e.end_node)
                                if e.is_bidirectional:
                                    G[e.end_node].pop(e.start_node)
                                edges.pop(i)
                                if focused_obj == i:
                                    edge_inspector['edge-inspector'].hide()
                            except KeyError:
                                pass
                            break

        ui_manager.process_events(event)
    
    ui_manager.update(time_delta)

    pressed_keys = pygame.key.get_pressed()

        
    screen.blit(workspace, (0, 0))
    workspace.fill((28, 27, 27))

    # Update UI
    if edge_inspector['edge-inspector'].visible:
        try:
            if int(edge_inspector['weight'].get_text()) != edges[focused_obj].weight:
                edges[focused_obj].weight = int(edge_inspector['weight'].get_text())
                G[edges[focused_obj].start_node][edges[focused_obj].end_node] = edges[focused_obj].weight
                if edges[focused_obj].is_bidirectional:
                    G[edges[focused_obj].end_node][edges[focused_obj].start_node] = edges[focused_obj].weight
        except ValueError:
            pass
        except IndexError:
            edge_inspector['edge-inspector'].hide()
    if run_algos['select_panel'].visible:
        delay = graph.utils.update_run_algos(run_algos, delay)
    
    # Update edges
    for e in edges:
        e.update(pressed_keys)
    # Update nodes
    for o in nodes:
        if time.time() - start_time >= delay and start_time != 0:
            try:
                if o.id == to_change_color[0][0]:
                    o.color = to_change_color[0][1]
                    start_time = time.time()
                    dont_change_color = to_change_color.pop(0)
            except IndexError:
                start_time = 0

        if o.id != dont_change_color[0]:
            o.color = (0, 0, 255)
        o.update(pressed_keys)
        workspace.blit(o.surf, o.pos)

    ui_manager.draw_ui(screen)

    # pygame.disply.update(list_of_rect_to_update)
    pygame.display.flip()

pygame.quit()