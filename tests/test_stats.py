
from app.index_writer.stats import IndexStats
def test_stats():
    s=IndexStats()
    assert s.indexed==0
