from typing import Iterator, List
from python_pdm_template.core.dao.log_file_dao import LogFileDAO
from python_pdm_template.core.parsers.apache_parser import ApacheParser
from python_pdm_template.core.detectors.brute_force_detector import Detection

class Pipeline:
    """Pipeline que integra DAO, Parser e Múltiplos Detectores (Pipe-and-Filter)."""

    def __init__(self, dao: LogFileDAO, parser: ApacheParser, detectors: List):
        self.dao = dao
        self.parser = parser
        self.detectors = detectors

    def run(self) -> Iterator[Detection]:
        # Lê as linhas e faz o parse
        entries = (self.parser.parse_line(line, i) for i, line in enumerate(self.dao.read_lines(), start=1))
        
        # Consome o gerador para uma lista na memória para passar por todos os detectores
        entries_list = list(entries)

        # Passa as entradas por cada detector (Strategy) e emite as detecções
        for detector in self.detectors:
            yield from detector.process(entries_list)