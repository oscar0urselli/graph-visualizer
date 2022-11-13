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
            container = self.info_panel
        )
        self.info_panel_label2 = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 90), (294, 36)),
            html_text = '',
            manager = manager,
            container = self.info_panel
        )
        self.info_panel_label3 = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 130), (294, 36)),
            html_text = '',
            manager = manager,
            container = self.info_panel
        )
        self.info_panel_label4 = pygame_gui.elements.UITextBox(
            relative_rect = pygame.Rect((0, 170), (294, 36)),
            html_text = '',
            manager = manager,
            container = self.info_panel,
            wrap_to_height = True
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