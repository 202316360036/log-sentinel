import hashlib
from pathlib import Path
from typing import Generator

class LogFileDAO:
    """DAO para leitura de arquivos de log com cálculo de hash SHA-256 integrado."""
    
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self._digest = ""

    @property
    def digest(self) -> str:
        """Retorna o hash SHA-256 calculado após a leitura do arquivo."""
        return self._digest

    def read_lines(self) -> Generator[str, None, None]:
        """Lê o arquivo linha a linha usando gerador (streaming) e calcula o hash."""
        sha256_hash = hashlib.sha256()
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # O hash precisa dos bytes exatos da linha
                sha256_hash.update(line.encode('utf-8'))
                # O yield devolve a linha sem quebrar o streaming
                yield line
                
        # Salva o hash final apenas quando a leitura termina
        self._digest = sha256_hash.hexdigest()