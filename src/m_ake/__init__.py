import m_ake.config
from m_ake import window
from m_ake.logic import event
from m_ake import gfx
from m_ake.state import State
from m_ake.state import state_change

CONFIG_FP = "res/config.txt"
config = m_ake.config.Config(CONFIG_FP)

import logging
logger = logging.getLogger('m_ake')

