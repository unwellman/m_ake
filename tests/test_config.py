import pytest
from m_ake.config import Config

def test_config_init ():
    config = Config(fp="tests/config.txt")
    assert config.parameter_int == 1280
    assert config.parameter_float == pytest.approx(0.7)
    assert config.parameter_str == "hello world"


