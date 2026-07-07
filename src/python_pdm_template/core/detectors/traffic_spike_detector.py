"""Detector de pico de trafego (iteracao 1: volume simples)."""
from __future__ import annotations

from collections.abc import Iterable, Iterator

from python_pdm_template.core.detectors.brute_force_detector import Detection
from python_pdm_template.core.models import LogEntry


class TrafficSpikeDetector:
    """Detecta pico de trafego total em janela."""

    SPIKE_THRESHOLD = 100

    def __init__(self, window_hours: int = 1, std_dev_multiplier: int = 2) -> None:
        """Define tamanho da janela e multiplicador de desvio padrao."""
        self.window_hours = window_hours
        self.std_dev_multiplier = std_dev_multiplier

    def process(self, entries: Iterable[LogEntry]) -> Iterator[Detection]:
        """Consuma entries e emita Detection ao ultrapassar SPIKE_THRESHOLD."""
        total_requests = 0
        for _ in entries:
            total_requests += 1
            if total_requests > self.SPIKE_THRESHOLD:
                yield Detection(
                    type="traffic_spike",
                    ip="global",
                    count=total_requests,
                    message="Pico de trafego detectado na janela atual",
                )
                total_requests = 0