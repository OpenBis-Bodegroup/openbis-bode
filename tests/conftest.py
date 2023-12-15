from pybis import Openbis
from pytest import fixture

from bode_loader.path import TEST_PATH
from bode_loader.utils import get_config


@fixture
def dataset_ab_dir():
    return TEST_PATH / "assets"


@fixture
def key_users():
    return ["OCHOUNG", "ASERRANO", "NARDOC"]


@fixture
def openbis():
    config = get_config()
    return Openbis(config["host"]["host_name"], token=config["host"]["token"])


@fixture
def ochoung_exp():
    return "/OCHOUNG/DEBUG/000"


@fixture
def ochoung_data():
    return "BODE - OCHOUNG-DEBUG-000-1h.txt"
