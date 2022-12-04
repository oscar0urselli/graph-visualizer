import pygame
import pygame_gui
import os


# Top bar
class TopBar:
    def __init__(self, manager, height, bar_height) -> None:
        self.app_icon = pygame_gui.elements.UIImage(
            relative_rect = pygame.Rect(((bar_height - height) / 2, (bar_height - height) / 2), (height, height)),
            image_surface = pygame.image.load(os.path.join(os.getcwd(), 'assets/icons/512x512/icon-512x512.png')),
            manager = manager
        )
        self.file_btn = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((bar_height, (bar_height - height) / 2), (60, height)),
            text = 'File',
            manager = manager,
            object_id = pygame_gui.core.ObjectID(
                class_id='@topbar_btn',
                object_id='#file_btn'
            )
        )
        self.settings_btn = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((bar_height + 60, (bar_height - height) / 2), (90, height)),
            text = 'Settings',
            manager = manager,
            object_id = pygame_gui.core.ObjectID(
                class_id='@topbar_btn',
                object_id='#settings_btn'
            )
        )
        self.help_btn = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((bar_height + 60 + 90, (bar_height - height) / 2), (60, height)),
            text = 'Help',
            manager = manager,
            object_id = pygame_gui.core.ObjectID(
                class_id='@topbar_btn',
                object_id='#help_btn'
            )
        )

# Tools bar
class ToolsBar:
    def __init__(self, manager) -> None:
        self.add_node_btn = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((25, 150), (64, 64)),
            text = "",
            manager = manager,
            tool_tip_text = 'Add node',
            object_id = pygame_gui.core.ObjectID(
                class_id='@toolsbar_btn',
                object_id='#add_node_btn'
            )
        )
        self.add_bidirectional_edge_btn = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((25, 230), (64, 64)),
            text = '',
            manager = manager,
            tool_tip_text = 'Add undirected edge',
            object_id = pygame_gui.core.ObjectID(
                class_id='@toolsbar_btn',
                object_id='#add_bidirectional_edge_btn'
            )
        )
        self.add_directional_edge_btn = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((25, 310), (64, 64)),
            text = '',
            manager = manager,
            tool_tip_text = 'Add directed edge',
            object_id = pygame_gui.core.ObjectID(
                class_id='@toolsbar_btn',
                object_id='#add_directional_edge_btn'
            )
        )
        self.algorithms_btn = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((25, 390), (64, 64)),
            text = '',
            manager = manager,
            tool_tip_text = 'Select an algorithm to run',
            object_id = pygame_gui.core.ObjectID(
                class_id='@toolsbar_btn',
                object_id='#run_algos_btn'
            )
        )

class ObjectInspector:
    def __init__(self, manager, pos, size) -> None:
        self.info_panel = pygame_gui.elements.UIPanel(
            relative_rect = pygame.Rect(pos, size),
            starting_layer_height = 1,
            manager = manager,
            visible = 0
        )
        self.info_panel_title = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 0), (294, 36)),
            html_text = 'Object inspector',
            manager = manager,
            container = self.info_panel
        )
        self.info_panel_label1 = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 50), (294, 36)),
            html_text = '',
            manager = manager,
            container = self.info_panel,
            object_id = pygame_gui.core.ObjectID(
                class_id='@object_inspector_text_box',
                object_id='#label1_text_box'
            )
        )
        self.info_panel_label2 = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 90), (294, 36)),
            html_text = '',
            manager = manager,
            container = self.info_panel,
            object_id = pygame_gui.core.ObjectID(
                class_id='@object_inspector_text_box',
                object_id='#label2_text_box'
            )
        )
        self.info_panel_label3 = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 130), (294, 36)),
            html_text = '',
            manager = manager,
            container = self.info_panel,
            object_id = pygame_gui.core.ObjectID(
                class_id='@object_inspector_text_box',
                object_id='#label3_text_box'
            )
        )
        self.info_panel_label4 = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 170), (294, 36)),
            html_text = '',
            manager = manager,
            container = self.info_panel,
            wrap_to_height = True,
            object_id = pygame_gui.core.ObjectID(
                class_id='@object_inspector_text_box',
                object_id='#label4_text_box'
            )
        )

    def update_label1(self, html_text: str) -> None:
        self.info_panel_label1.html_text = html_text
        self.info_panel_label1.rebuild()

    def update_label2(self, html_text: str) -> None:
        self.info_panel_label2.html_text = html_text
        self.info_panel_label2.rebuild()

    def update_label3(self, html_text: str) -> None:
        self.info_panel_label3.html_text = html_text
        self.info_panel_label3.rebuild()

    def update_label4(self, html_text: str) -> None:
        self.info_panel_label4.html_text = html_text
        self.info_panel_label4.rebuild()

class RunAlgos:
    def __init__(self, manager, screen) -> None:
        size = (800, 500)
        self.rect = pygame.Rect((screen[0] / 2 - size[0] / 2, screen[1] / 2 - size[1] / 2), (size[0], size[1]))
        self.select_panel = pygame_gui.elements.UIPanel(
            relative_rect = self.rect,
            starting_layer_height = 1,
            manager = manager,
            visible = 0
        )
        self.select_panel_title = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 0), (size[0] - 6, 36)),
            html_text = 'Select an algorithm to run',
            manager = manager,
            container = self.select_panel
        )
        self.algos_selection = pygame_gui.elements.UIDropDownMenu(
            options_list = ['DFS', 'BFS', 'Dijkstra'],
            starting_option = 'None',
            relative_rect = pygame.Rect((0, 40), (size[0] - 6, 36)),
            manager = manager,
            container = self.select_panel
        )
        self.delay_text_box = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 280), (size[0] - 6, 30)),
            html_text = 'Delay',
            manager = manager,
            container = self.select_panel
        )
        self.delay_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect = pygame.Rect((0, 305), (size[0] - 200, 30)),
            start_value = 1,
            value_range = (0.01, 2),
            manager = manager,
            container = self.select_panel,
            click_increment = 0.01
        )

        # DFS
        self.dfs_panel = pygame_gui.elements.UIPanel(
            relative_rect = pygame.Rect((0, 80), (size[0] - 6, size[1] - 300)),
            starting_layer_height = 2,
            manager = manager,
            container = self.select_panel,
            visible = 0
        )
        self.dfs_title = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 0), (size[0] - 12, 36)),
            html_text = "DFS",
            manager = manager,
            container = self.dfs_panel
        )

        # BFS
        self.bfs_panel = pygame_gui.elements.UIPanel(
            relative_rect = pygame.Rect((0, 80), (size[0] - 6, size[1] - 300)),
            starting_layer_height = 2,
            manager = manager,
            container = self.select_panel,
            visible = 0
        )
        self.bfs_title = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 0), (size[0] - 12, 36)),
            html_text = "BFS",
            manager = manager,
            container = self.bfs_panel
        )

    def update(self, mode: str) -> None:
        if mode == 'RUN ALGOS':
            if self.algos_selection.selected_option == 'DFS':
                self.dfs_panel.show()
            elif self.algos_selection.selected_option == 'BFS':
                self.bfs_panel.show()
            else:
                self.dfs_panel.hide()
                self.bfs_panel.hide()

    def hide(self) -> None:
        self.select_panel.hide()
        self.dfs_panel.hide()
        self.bfs_panel.hide()

    def show(self) -> None:
        self.select_panel.show()