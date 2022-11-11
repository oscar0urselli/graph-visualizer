import pygame
import pygame_gui


# Top bar
class TopBar:
    def __init__(self, manager, height = 36) -> None:
        self.file_btn = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((0, 0), (72, height)),
            text = 'File',
            manager = manager
        )
        self.settings_btn = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((72, 0), (100, height)),
            text = 'Settings',
            manager = manager
        )
        self.help_btn = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((172, 0), (72, height)),
            text = 'Help',
            manager = manager
        )

# Tools 

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