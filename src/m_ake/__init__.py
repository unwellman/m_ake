import m_ake.config
from m_ake import window
from m_ake.logic import event
from m_ake import gfx
from m_ake.state import State
from m_ake.state import state_change
from m_ake.file_io import get_path

def init (file):
    """
    Initialize the file abstraction layer and grab the config file

    Parameters:
        file: __file__ attribute of the entry point module

    This function must be called before any module that relies on global config
    """
    m_ake.file_io.set_file(file)

    CONFIG_FP = get_path("res/config.txt")
    # This is terrible namespace management but don't question it
    m_ake.config = m_ake.config.Config(CONFIG_FP)


