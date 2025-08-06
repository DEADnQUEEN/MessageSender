import time

from utils import config, get_data, logger, formaters

from messageSender.wasender import WASender
from imageEditor.PILeditor import PILEditor
from imageEditor.image_editor import format_image


def main():
    bot = WASender(profile_path="user")
    editor = PILEditor()

    for row in get_data.get_from_csv(
        config.CSV_DATA_FILE,
        get_data.get_columns(config.COLUMN_PATH),
        have_title=False,
    ):
        number, city, code = row

        if bot.send_text(
            number,
            formaters.text_format(code)
        ):
            continue

        path = format_image(
            editor,
            city,
            code
        )
        bot.send_image(
            number,
            path
        )

    bot.quit()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.collect_log(str(e))
        print("Error logged")
        time.sleep(10)
