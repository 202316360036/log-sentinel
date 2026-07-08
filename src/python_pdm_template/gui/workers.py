from PySide6.QtCore import QThread, Signal
import os

# O import do Core do Aryan (pode dar erro até o dele cair na master, mas já deixe pronto)
# Ajuste o caminho exato do import se o pacote dele tiver outro nome
from python_pdm_template.core.parsers import ApacheParser 

class LogParserWorker(QThread):
    # Sinais que a GUI vai escutar
    progress = Signal(int)     # Envia o percentual atual (0 a 100)
    finished = Signal(list)    # Envia a lista final de LogEntry quando terminar

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def run(self):
        log_entries = []
        
        if not os.path.exists(self.file_path):
            self.finished.emit([])
            return

        # Descobre o tamanho total do arquivo para calcular o progresso por bytes
        # (É mais rápido do que contar as linhas antes)
        total_bytes = os.path.getsize(self.file_path)
        bytes_processed = 0

        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                # Soma o tamanho da linha (mais o caractere de quebra de linha)
                bytes_processed += len(line.encode("utf-8"))
                
                # Limpa espaços/quebras de linha e manda pro parser do Aryan
                clean_line = line.strip()
                if clean_line:
                    try:
                        # Chama o método do parser do Aryan
                        entry = ApacheParser.parse_line(clean_line)
                        if entry:
                            log_entries.append(entry)
                    except Exception as e:
                        # Trate ou ignore linhas malformadas para não quebrar o worker
                        print(f"Erro ao processar linha: {e}")

                # Calcula e emite o progresso
                if total_bytes > 0:
                    percent = int((bytes_processed / total_bytes) * 100)
                    self.progress.emit(percent)

        # No final, emite a lista cheia para a GUI atualizar a tabela
        self.finished.emit(log_entries)
