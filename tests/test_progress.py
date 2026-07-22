
from app.cli.progress import ProgressReporter

def test_progress():
    p=ProgressReporter()
    p.tick()
    assert p.total==1
