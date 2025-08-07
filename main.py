import time

from utils import config, get_data, logger, formaters
from messageSender.WhatsAppSender.wasender import WASender
from imageEditor.PILeditor import PILEditor
from imageEditor.image_editor import format_image


def main():
    editor = PILEditor()
    with WASender(profile_path="user") as bot:
        for row in get_data.get_from_csv(
            config.CSV_DATA_FILE,
            get_data.get_columns(config.COLUMN_DATA),
            config.CSV_HAS_TITLE,
        ):
            number, city, code = row

            if not bot.send_text(
                number,
                formaters.text_format(code)
            ):
                logger.collect_log(f"text sender timeout", f"timeout-{number}")
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


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.collect_log(str(e))
        print("Error logged")
        input("Press Enter to exit...")
    time.sleep(5)
