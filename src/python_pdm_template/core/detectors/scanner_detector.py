from typing import Iterator, Iterable
from collections import defaultdict
from datetime import datetime
from python_pdm_template.core.models import LogEntry
from python_pdm_template.core.detectors.brute_force_detector import Detection

class ScannerDetector:
    """Detector de varredura (scanners) buscando URLs sensíveis."""
    
    def __init__(self, threshold: int = 3, window_seconds: int = 60):
        self.threshold = threshold
        self.window_seconds = window_seconds
        self.sensitive_urls = ['/admin', '/.env', '/wp-login', '/.git']

    def process(self, entries: Iterable[LogEntry]) -> Iterator[Detection]:
        history = defaultdict(list)

        for entry in entries:
            # Verifica se a URL acessada contém alguma das strings sensíveis
            if any(sensitive in entry.url for sensitive in self.sensitive_urls):
                try:
                    time_str = entry.timestamp.split()[0]
                    dt = datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S")
                except Exception:
                    continue

                ip = entry.ip
                history[ip].append(dt)

                history[ip] = [t for t in history[ip] if (dt - t).total_seconds() <= self.window_seconds]

                if len(history[ip]) >= self.threshold:
                    yield Detection(
                        type="scanner",
                        ip=ip,
                        count=len(history[ip]),
                        message=f"Scanner detectado: {len(history[ip])} acessos sensíveis do IP {ip}"
                    )
                    history[ip] = []