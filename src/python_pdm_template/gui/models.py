from PySide6.QtWidgets import QApplication, QMainWindow, QTableView
from PySide6.QtCore import QAbstractTableModel, Qt, QThread

class LogEntryTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        # Se não passarem nenhuma lista, começamos com uma lista vazia
        self._data = data or []
        # O nome das nossas 4 colunas!
        self._headers = ["IP", "Timestamp", "Método", "Status"]

    def rowCount(self, parent=None):
        # Conta quantas linhas de dados nós temos
        return len(self._data)

    def columnCount(self, parent=None):
        # Como temos 4 colunas fixas, retorna 4
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        # Se não for para mostrar texto na tela, não fazemos nada
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        # Pega a linha atual da tabela
        log_entry = self._data[index.row()]
        column = index.column()

        # Dependendo da coluna, mostra um pedaço diferente do dado
        # Nota: Aqui estamos fingindo que o LogEntry tem esses atributos. 
        # Ajuste os nomes (.ip, .timestamp, etc.) se o ApacheParser do Aryan usar nomes diferentes!
        if column == 0:
            return getattr(log_entry, "ip", "")
        elif column == 1:
            return getattr(log_entry, "timestamp", "")
        elif column == 2:
            return getattr(log_entry, "method", "")
        elif column == 3:
            return getattr(log_entry, "status", "")
        
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        # Coloca os títulos bonitinhos ("IP", "Timestamp"...) no topo de cada coluna
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._headers[section]
        return None

    def set_data(self, data):
        # Função mágica para atualizar a tabela inteira quando o arquivo terminar de ser lido
        self.beginResetModel()
        self._data = data
        self.endResetModel()