from typing import Iterable, Dict, List
from dataclasses import dataclass, field
from python_pdm_template.core.detectors.brute_force_detector import Detection

@dataclass
class Report:
    """Relatório consolidado de detecções."""
    total_detections: int = 0
    detections_by_type: Dict[str, List[Detection]] = field(default_factory=dict)

class Aggregator:
    """Agrega um stream de detecções em um relatório consolidado."""

    def aggregate(self, detections: Iterable[Detection]) -> Report:
        report = Report()
        for detection in detections:
            report.total_detections += 1
            if detection.type not in report.detections_by_type:
                report.detections_by_type[detection.type] = []
            report.detections_by_type[detection.type].append(detection)
        return report