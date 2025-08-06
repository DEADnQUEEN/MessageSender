from utils import config
import imageEditor
import os


def format_image(
        editor: imageEditor.editor.Editor,
        template: str,
        text: str
) -> str:
    if template not in config.CONFIG['templates']:
        raise IndexError(f"{template} is not a valid template name")

    save_to = os.path.join(
        config.TMP_PATH,
        f"{text}.png"
    )

    editor.open_image(
        config.CONFIG['templates'][template]
    )
    editor.set_font(
        config.CONFIG['font']['path'],
        config.CONFIG['font']['size']
    )
    color = config.CONFIG['font']['color']
    editor.draw_text_on_image(
        text,
        config.CONFIG['x'],
        config.CONFIG['y'],
        (color[0], color[1], color[2]),
    )

    editor.save_image(save_to)

    return save_to
