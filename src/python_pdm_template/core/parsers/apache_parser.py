import re

# Importando o LogEntry que o documento diz que já existe. 
# O caminho exato do import pode variar, ajuste se a sua equipe colocou em outro lugar.
from python_pdm_template.core.models import LogEntry

class ParseError(Exception):
    pass

class ApacheParser:
    """Parser para formatos Common e Combined do Apache."""
    
    # Expressão Regular para o Combined Log Format (mais completo)
    COMBINED_REGEX = re.compile(
        r'^(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" '
        r'(?P<status>\d{3}) (?P<size>\S+) '
        r'"(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"$'
    )

    # Expressão Regular para o Common Log Format (básico)
    COMMON_REGEX = re.compile(
        r'^(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" '
        r'(?P<status>\d{3}) (?P<size>\S+)$'
    )

    def parse_line(self, line: str, line_number: int) -> LogEntry:
        # Tenta casar com o formato Combined primeiro (mais permissivo)
        match = self.COMBINED_REGEX.match(line)
        
        # Se não casar, tenta o Common
        if not match:
            match = self.COMMON_REGEX.match(line)
            
        # Se nenhum casar, levanta o erro com a linha
        if not match:
            raise ParseError(f"Linha malformada na linha {line_number}")
            
        data = match.groupdict()
        
        # O tamanho (size) no log do Apache pode vir como '-' quando é zero
        size_str = data.get('size')
        size = 0 if size_str == '-' else int(size_str)
        
        return LogEntry(
            ip=data['ip'],
            timestamp=data['timestamp'],
            method=data['method'],
            status=int(data['status']),
            # Caso não existam no Common, pegam None pelo .get()
            referer=data.get('referer'),
            user_agent=data.get('user_agent')
        )