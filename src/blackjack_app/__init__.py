# note: when using "uv init", this __init__.py file replaces main.py when using "uv run <project-name>".
# in pyproject.toml, under [project.scripts], devs can initialte a cli command.
# in this program's case, it's '"blackjack-app = "blackjack_app:main"'. Run by simply inputting 'blackjack-app' into the cli.
# essentially does the following: "import sys; from blackjack_app import main; sys.exit(main())"
# when running directly from this __init__.py file, the 'if __name__ == "__main__": main()' part runs
# ...could an executable shell script be used to make executing this program easier?
import sys
from pathlib import Path  # allows for path traversal

# from windows.test import test
from PySide6.QtWidgets import QApplication

# when importing stuff from the src folder, use the folder below it as the "root" folder
from blackjack_app.windows.main_window import MainWindow


# 'def main() -> None:' - After a function '-> type' defines an expected return type.
def main() -> None:
    __app_dir = Path(__file__).resolve().parent  # get absolute file path of this file,
    # then go back one to get the app's directory.

    app = QApplication(sys.argv)
    window = MainWindow(__app_dir)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
