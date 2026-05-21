#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import os
from collections import namedtuple
from enum import Enum

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from components.mask_widget import MaskWidget
from ui.ui_source.SettingDialog import Ui_SettingDialog


Setting = namedtuple("Setting", ["api_mode", "is_lrc", "is_rename", "auto_if"])
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")


class ApiMode(Enum):
    CLOUD = 0
    KUGOU = 1


class SettingDialog(QDialog, Ui_SettingDialog):
    done_signal = pyqtSignal(Setting)

    def __init__(self, parent=None):
        super(SettingDialog, self).__init__(parent)
        self.setupUi(self)
        self.auto_if = False
        self._load_config()
        self._init_signal()

    def _init_signal(self):
        self.auto_button.clicked.connect(self.auto_event)
        self.api_comboBox.currentIndexChanged.connect(self.comboBox_event)

    def _load_config(self):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
            api_mode = self._normalize_api_mode(config.get("api_mode", ApiMode.CLOUD.value))
            self.api_comboBox.setCurrentIndex(api_mode)
            self.is_download_lrc_checkBox.setChecked(config.get("is_lrc", False))
            self.is_rename_file_checkBox.setChecked(config.get("is_rename", True))
        except (FileNotFoundError, json.JSONDecodeError):
            self.api_comboBox.setCurrentIndex(ApiMode.CLOUD.value)
            self.is_download_lrc_checkBox.setChecked(False)
            self.is_rename_file_checkBox.setChecked(True)

    def _save_config(self):
        config = {
            "api_mode": self._normalize_api_mode(self.api_comboBox.currentIndex()),
            "is_lrc": self.is_download_lrc_checkBox.isChecked(),
            "is_rename": self.is_rename_file_checkBox.isChecked(),
        }
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def _normalize_api_mode(self, api_mode: int) -> int:
        if api_mode in (ApiMode.CLOUD.value, ApiMode.KUGOU.value):
            return api_mode
        return ApiMode.CLOUD.value

    def comboBox_event(self):
        if not self.is_download_lrc_checkBox.isEnabled():
            self.is_download_lrc_checkBox.setEnabled(True)

    def auto_event(self):
        self.auto_if = True
        self.accept()

    def accept(self) -> None:
        self._save_config()
        mode = ApiMode(self._normalize_api_mode(self.api_comboBox.currentIndex()))
        setting = Setting(
            api_mode=mode,
            is_lrc=self.is_download_lrc_checkBox.isChecked(),
            is_rename=self.is_rename_file_checkBox.isChecked(),
            auto_if=self.auto_if,
        )
        self.done_signal.emit(setting)
        super(SettingDialog, self).accept()

    def show(self) -> None:
        self.auto_if = False
        self._set_mask_visible(True)
        super(SettingDialog, self).show()

    def done(self, a0: int) -> None:
        self._set_mask_visible(False)
        super(SettingDialog, self).done(a0)

    def _set_mask_visible(self, flag: bool):
        if self.parent():
            if not hasattr(self.parent(), "mask_widget"):
                self.parent().mask_widget = MaskWidget(self.parent())
            if flag:
                self.parent().mask_widget.show()
            else:
                self.parent().mask_widget.hide()
