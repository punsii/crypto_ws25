import pytest

pytest.main(["./test_ec.py", "-vv", "--durations=0", "-k", "test_ec_add"])
