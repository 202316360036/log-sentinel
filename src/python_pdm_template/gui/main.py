import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView
from PySide6.QtCore import QAbstractTableModel, Qt, QThread
# Aqui a gente chama a janela que já existe na sua pasta!
from python_pdm_template.gui.main_window import MainWindow

def main():
    # 1. Cria o sistema do aplicativo
    app = QApplication(sys.argv)
    
    # 2. Cria a janelinha principal
    window = MainWindow()
    window.show()
    
    # 3. Liga o aplicativo e deixa ele rodando
    sys.exit(app.exec())

if __name__ == "__main__":
    main()