from typing import Iterator, Iterable
from collections import defaultdict
from datetime import datetime
from dataclasses import dataclass
from python_pdm_template.core.models import LogEntry

@dataclass
class Detection:
    """Modelo básico para uma detecção."""
    type: str
    ip: str
    count: int
    message: str

class BruteForceDetector:
    """Detector de força bruta usando janela deslizante."""
    
    def __init__(self, threshold: int = 10, window_seconds: int = 60):
        self.threshold = threshold
        self.window_seconds = window_seconds

    def process(self, entries: Iterable[LogEntry]) -> Iterator[Detection]:
        history = defaultdict(list)

        for entry in entries:
            if entry.status in (401, 403):
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
                        type="brute_force",
                        ip=ip,
                        count=len(history[ip]),
                        message=f"Brute-force: {len(history[ip])} tentativas do IP {ip}"
                    )
                    history[ip] = []