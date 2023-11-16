from pybis import Openbis

from .utils import get_config

CONFIG = get_config()

if __name__ == "__main__":
    openbis = Openbis(CONFIG["host"]["host_name"])
    openbis.login(CONFIG["host"]["user"], CONFIG["host"]["password"])
