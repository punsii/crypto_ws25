import pytest

pytest.main(["./test_ecdsa.py", "-vv", "--durations=0", "-k", "test_ecdsa"])
