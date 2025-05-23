import pytest
from pathlib import Path

current_dir = Path(__file__).parent
raise SystemExit(pytest.main([str(current_dir), "-v"]))
