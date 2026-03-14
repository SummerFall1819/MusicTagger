#!/usr/bin/python
# -*- coding:utf-8 -*-
# Origin author: Mai-icy. Modification credits to Claude code.

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class InfoLabel(QLabel):
    def __init__(self, parent=None):
        super(InfoLabel, self).__init__(parent=parent)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # 设置label可复制
        self.metrics = QFontMetrics(self.font())

    def put_text(self, text: str):
        text = text if text else "N/A"
        new_text = self.metrics.elidedText(text, Qt.TextElideMode.ElideRight, self.width())
        self.setText(new_text)




