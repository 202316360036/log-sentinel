```python
from python_pdm_template.gui.main_window import MainWindow


def test_janela_abre(qtbot):
    w = MainWindow()
    qtbot.addWidget(w)

    assert w.windowTitle() == "Log Sentinel"
```

