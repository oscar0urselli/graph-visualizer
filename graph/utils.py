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