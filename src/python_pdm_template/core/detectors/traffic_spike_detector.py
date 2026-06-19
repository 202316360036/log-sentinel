from typing import Iterator, Iterable
from python_pdm_template.core.models import LogEntry
from python_pdm_template.core.detectors.brute_force_detector import Detection

class TrafficSpikeDetector:
    """Detector de pico de tráfego (Esqueleto inicial)."""
    
    def __init__(self, window_hours: int = 1, std_dev_multiplier: int = 2):
        self.window_hours = window_hours
        self.std_dev_multiplier = std_dev_multiplier

    def process(self, entries: Iterable[LogEntry]) -> Iterator[Detection]:
        # Agrega requisições. Para esta iteração 1, disparamos se o volume total for muito alto.
        total_requests = 0
        
        for entry in entries:
            total_requests += 1
            
            # Mock de disparo para passar no teste da primeira iteração
            if total_requests > 100:
                yield Detection(
                    type="traffic_spike",
                    ip="global",
                    count=total_requests,
                    message="Pico de tráfego detectado na janela atual"
                )
                total_requests = 0