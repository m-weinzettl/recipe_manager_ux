import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.view.gui import *


if __name__ == "__main__":
    flet.run(main=gui)




