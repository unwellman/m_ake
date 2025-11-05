import os
import logging
logger = logging.getLogger('m_ake')

file = ""

def set_file (fp):
    global file
    dirname = os.path.dirname(fp)
    dirs = dirname.split(os.sep)
    if dirs[-1] == "m_ake" and dirs[-2] == "src":
        logger.debug(f"Detected Python module runtime; __file__ = {fp}")
        file = os.path.dirname(f"{os.sep}".join(dirs[0:len(dirs) - 1]))
    else:
        logger.debug(f"Detected PyInstaller runtime; __file__ = {fp}")
        file = dirname

def get_path (fp):
    """
    Get absolute path of a resource depending on the runtime environment

    There are probably gonna be some very dirty hacks in this function
    """
    logger.debug(f"Requested {fp} from searchpath {file}")
    return os.path.abspath(os.path.join(file, fp))

