#!/usr/bin/python
# -*- coding:utf-8 -*-
# Origin author: Mai-icy. Modification credits to Claude code.
import sys

sys.path.append("..")

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from ui.metadata_widget import MetadataWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MetadataWidget()
    myWin.show()
    sys.exit(app.exec())
