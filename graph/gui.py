import pygame
import pygame_gui
import os
import xml.etree.ElementTree as xmlET


class UIWindowMod(pygame_gui.elements.UIWindow):
    """
    This class is the same as pygame_gui.elements.UIWindow excpet for the followings:
    :param kill_on_close: On True the window will be killed when the close button is called, on False it will be hidden
    """
    def __init__(self, rect, manager, window_display_title, visible, object_id = None, resizable = False, kill_on_close = False) -> None:
        self.kill_on_close = kill_on_close
        super().__init__(rect = rect, manager = manager, window_display_title = window_display_title, resizable = resizable, visible = visible, object_id = object_id)
    
    def on_close_window_button_pressed(self):
        self.kill() if self.kill_on_close else self.hide()

class UIWidget:
    def __init__(self, xml_path: str, screen, manager) -> None:
        self.xml_path = xml_path
        self.screen = screen
        self.manager = manager

        self.ui_elements = {
            'image': pygame_gui.elements.UIImage,
            'button': pygame_gui.elements.UIButton,
            'textbox': pygame_gui.elements.UITextBox,
            'textentryline': pygame_gui.elements.UITextEntryLine,
            'horizontalslider': pygame_gui.elements.UIHorizontalSlider,
            'dropdownmenu': pygame_gui.elements.UIDropDownMenu,
            'panel': pygame_gui.elements.UIPanel,
            'windowmod': UIWindowMod
        }

        self.struct = {}

    def parse(self):
        tree = xmlET.parse(self.xml_path)
        root = tree.getroot()

        self.expand(root)

        return self.struct

    def expand(self, parent):
        for child in parent:
            if child.tag in self.ui_elements:
                self.struct[child.attrib['name']] = self.add_ui_element(child.tag, child.attrib, parent)
            self.expand(child)

    def add_ui_element(self, tag: str, attrib: dict, parent):
        pos = eval(attrib['pos'].replace('WIDTH', str(self.screen[0])).replace('HEIGHT', str(self.screen[1])))
        size = eval(attrib['size'].replace('WIDTH', str(self.screen[0])).replace('HEIGHT', str(self.screen[1])))
        rect = pygame.Rect(pos, size)
        container = None
        object_id = None
        visible = 1

        if parent.tag in self.ui_elements:
            container = self.struct[parent.attrib['name']]
        if 'class' in attrib and 'id' in attrib:
            object_id = pygame_gui.core.ObjectID(class_id = '@' + attrib['class'], object_id = '#' + attrib['id'])
        if 'visible' in attrib:
            visible = int(attrib['visible'])

        element = None
        if tag == 'image':
            element = self.ui_elements[tag](
                relative_rect = rect,
                image_surface = pygame.image.load(os.path.join(os.getcwd(), 'assets/icons/512x512/icon-512x512.png')),
                manager = self.manager,
                container = container,
                object_id = object_id
            )
        elif tag == 'button':
            element = self.ui_elements[tag](
                relative_rect = rect,
                text = attrib['text'],
                tool_tip_text = attrib['tool_tip_text'],
                manager = self.manager,
                container = container,
                object_id = object_id
            )
        elif tag == 'textbox':
            element = self.ui_elements[tag](
                relative_rect = rect,
                html_text = attrib['html_text'],
                manager = self.manager,
                container = container,
                object_id = object_id
            )
        elif tag == 'textentryline':
            element = self.ui_elements[tag](
                relative_rect = rect,
                manager = self.manager,
                object_id = object_id,
                container = container
            )
            if 'white_list' in attrib:
                element.set_allowed_characters(attrib['white_list'])
        elif tag == 'horizontalslider':
            element = self.ui_elements[tag](
                relative_rect = rect,
                start_value = float(attrib['start_value']),
                value_range = eval(attrib['value_range']),
                manager = self.manager,
                container = container,
                click_increment = float(attrib['click_increment']),
                object_id = object_id
            )
        elif tag == 'dropdownmenu':
            element = self.ui_elements[tag](
                relative_rect = rect,
                options_list = attrib['options_list'].split(';'),
                starting_option = attrib['starting_option'],
                manager = self.manager,
                object_id = object_id,
                container = container
            )
        elif tag == 'panel':
            element = self.ui_elements[tag](
                relative_rect = rect,
                starting_layer_height = int(attrib['starting_layer_height']),
                manager = self.manager,
                container = container,
                object_id = object_id,
                visible = visible
            )
        elif tag == 'windowmod':
            element = self.ui_elements[tag](
                rect = rect,
                window_display_title = attrib['window_display_title'],
                manager = self.manager,
                object_id = object_id,
                visible = visible
            )

        return element