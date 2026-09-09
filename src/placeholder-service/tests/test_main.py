
from main import get_status

def test_get_status():
    """Test that the status function returns the expected dictionary."""
    result = get_status()
    assert result["status"] == "ok"
    assert result["service"] == "placeholder"
