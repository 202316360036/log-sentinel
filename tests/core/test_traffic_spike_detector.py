from python_pdm_template.core.models import LogEntry
from python_pdm_template.core.detectors.traffic_spike_detector import TrafficSpikeDetector

def test_traffic_spike_detector_iteracao_1():
    detector = TrafficSpikeDetector()
    
    # Simulando um volume alto de requisições rápidas
    entries = [LogEntry("127.0.0.1", "10/Oct/2000:13:00:00 -0700", "GET", 200, "/", None) for _ in range(101)]
    
    detections = list(detector.process(entries))
    assert len(detections) >= 1
    assert detections[0].type == "traffic_spike"