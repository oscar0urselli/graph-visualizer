import json
import os


def init_settings():
    """
    Load the settings from settings.json
    """
    settings = None
    dir = os.path.join(os.getcwd(), 'settings.json')
    try:
        with open(dir) as f:
            settings = json.loads(''.join(f.readlines()))
    except OSError:
        with open(dir, 'w') as f:
            f.write(
                '''
                {
                    "bg": {
                        "line_thickness": 10,
                        "square_size": 200,
                        "bg_primary_color": [20, 20, 20],
                        "bg_secondary_color": [80, 80, 80]
                    },
                    "graphics": {
                        "fps": 60
                    }
                }
                '''
            )
        settings = {
                "bg": {
                    "line_thickness": 10,
                    "square_size": 200,
                    "bg_primary_color": [20, 20, 20],
                    "bg_secondary_color": [80, 80, 80]
                },
                "graphics": {
                    "fps": 60
                }
            }

    return settings


def mouse_in_dmz(dmzs, mouse_pos) -> bool:
    """
    Check if the mouse is in one of the passed areas
    """
    for dmz in dmzs:
        if dmz.collidepoint(mouse_pos):
            return True

    return False

def update_node_inspector(node_inspector, edge_inspector, o, G):
    node_inspector['id'].html_text = 'Id: ' + o.id
    node_inspector['id'].rebuild()

    node_inspector['color'].html_text = 'Color: ' + str(o.color)
    node_inspector['color'].rebuild()

    node_inspector['neighbours'].html_text = 'Neighbours: { ' + ', '.join([i[0] + ': ' + str(i[1]) for i in G[o.id].items()]) + ' }'
    node_inspector['neighbours'].rebuild()

    node_inspector['node-inspector'].show()
    edge_inspector['edge-inspector'].hide()

def update_edge_inspector(edge_inspector, node_inspector, e, G):
    edge_inspector['color'].html_text = 'Color: ' + str(e.color)
    edge_inspector['color'].rebuild()

    edge_inspector['way'].html_text = e.start_node + (' <-> ' if e.is_bidirectional else ' --> ') + e.end_node
    edge_inspector['way'].rebuild()

    edge_inspector['weight'].set_text(str(e.weight))

    edge_inspector['edge-inspector'].show()
    node_inspector['node-inspector'].hide()

def can_click(run_algos, node_inspector, edge_inspector, top_bar, mouse) -> bool:
    can = True
    
    if run_algos['select_panel'].visible and run_algos['select_panel'].hover_point(mouse[0], mouse[1]):
        can = False
    if node_inspector['node-inspector'].visible and node_inspector['node-inspector'].hover_point(mouse[0], mouse[1]):
        can = False
    if edge_inspector['edge-inspector'].visible and edge_inspector['edge-inspector'].hover_point(mouse[0], mouse[1]):
        can = False
    if top_bar['top-bar'].visible and top_bar['top-bar'].hover_point(mouse[0], mouse[1]):
        can = False

    return can

def update_run_algos(run_algos, delay):
    if run_algos['algo_name'].html_text != run_algos['algos_selection'].selected_option:
        run_algos['algo_name'].html_text = run_algos['algos_selection'].selected_option
        run_algos['algo_name'].rebuild()

    if run_algos['select_panel'].visible:
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

    if run_algos['delay_slider'].get_current_value() != delay:
        delay = run_algos['delay_slider'].get_current_value()
        run_algos['delay_text_box'].html_text = 'Delay: ' + str(round(delay, 2)) + ' s'
        run_algos['delay_text_box'].rebuild()

    return delay