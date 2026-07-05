"""Janela principal da GUI do Log Sentinel."""
from __future__ import annotations
# Trocamos o QLabel pelas pecinhas que vamos usar (Tabela, Botão, Barrinha...)
from PySide6.QtWidgets import (QMainWindow, QTableView, QPushButton, 
                               QVBoxLayout, QWidget, QFileDialog, QProgressBar)
from python_pdm_template.gui.models import LogEntryTableModel
from python_pdm_template.gui.workers import ParserWorker


class MainWindow(QMainWindow):
    """Janela principal do Log Sentinel."""

    def __init__(self) -> None:
        """Inicializa a janela principal com titulo, tamanho e os componentes da tabela."""
        super().__init__()
        self.setWindowTitle("Log Sentinel")
        self.resize(1024, 768)

        # 1. O "Cérebro" da Tabela (Model)
        self.model = LogEntryTableModel()
        
        # 2. O desenho da Tabela (View)
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # 3. O Botão e a Barrinha de Progresso
        self.btn_open = QPushButton("Abrir arquivo de log...")
        self.btn_open.clicked.connect(self.start_parsing)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # 4. Organizando tudo um embaixo do outro (como blocos de Lego)
        layout = QVBoxLayout()
        layout.addWidget(self.btn_open)
        layout.addWidget(self.table_view)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        
        # Trocamos o antigo QLabel pelo nosso container cheio de coisas!
        self.setCentralWidget(container)

    def start_parsing(self) -> None:
        """Abre o buscador de arquivos e inicia o operário para ler o log."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Escolha o Log", "", "Logs (*.log);;Todos (*.*)")
        
        if file_path:
            # Criando o nosso operário invisível do Commit 2
            self.worker = ParserWorker(file_path)
            
            # Conectando os rádio-comunicadores (Signals)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.finished.connect(self.on_finished)
            
            # Mandando ele trabalhar!
            self.worker.start()
            self.btn_open.setEnabled(False) # Desliga o botão para não clicar duas vezes

    def on_finished(self, log_entries: list) -> None:
        """Recebe os dados do operário quando ele termina e joga na tabela."""
        self.model.set_data(log_entries)
        self.btn_open.setEnabled(True) # Ativa o botão de novo
        self.progress_bar.setValue(100) # Deixa a barra cheia
