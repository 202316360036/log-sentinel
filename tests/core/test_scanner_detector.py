from python_pdm_template.core.models import LogEntry
from python_pdm_template.core.detectors.scanner_detector import ScannerDetector

def test_scanner_detector_positivo():
    detector = ScannerDetector(threshold=2, window_seconds=60)
    
    # Simulando acessos a URLs sensíveis
    entries = [
        LogEntry("10.0.0.1", "10/Oct/2000:13:55:01 -0700", "GET", 404, "/.env", None),
        LogEntry("10.0.0.1", "10/Oct/2000:13:55:05 -0700", "GET", 404, "/wp-login", None),
    ]
    
    detections = list(detector.process(entries))
    assert len(detections) == 1
    assert detections[0].type == "scanner"