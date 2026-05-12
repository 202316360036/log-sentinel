"""Janela principal da GUI do Log Sentinel."""
from __future__ import annotations
from PySide6.QtWidgets import QMainWindow, QLabel


class MainWindow(QMainWindow):
    """Janela principal do Log Sentinel."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Log Sentinel")
        self.resize(1024, 768)
        self.setCentralWidget(QLabel("Em construcao"))
