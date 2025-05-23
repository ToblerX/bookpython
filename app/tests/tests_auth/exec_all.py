import pytest
from pathlib import Path

if __name__ == "__main__":
    current_dir = Path(__file__).parent
    raise SystemExit(pytest.main([str(current_dir), "-v"]))
