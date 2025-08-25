import tkinter

from GUI.interface import template as interface

from GUI.loaders.csv_loader import CSVLoader
from GUI.loaders.template import TemplateLoader
from GUI.sender_view.sender_ui import SenderUI

from utils import logger

def main():
    csv_viewer = CSVLoader()
    template = TemplateLoader()

    root = tkinter.Tk()
    root.title("WhatsAppBot")
    root.geometry("500x300")

    main_frame = interface.UserView(
        root,
        csv_viewer,
        template,
        SenderUI,
    )
    main_frame.pack(fill=tkinter.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as error:
        logger.collect_log(error, "app")
