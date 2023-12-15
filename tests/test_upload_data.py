from pathlib import Path
from typing import List

from pybis import Openbis

from bode_loader.upload_data import (
    get_all_files,
    get_all_spaces,
    get_datasets,
    return_new_idx,
    upload_new_dataset,
)


def test_get_all_files(dataset_ab_dir: Path):
    """test get_all_files"""
    results = get_all_files(instrument_dir=dataset_ab_dir, hierarchy="BODE - OCHOUNG*")
    data_list = list(dataset_ab_dir.glob("BODE - OCHOUNG*"))
    assert len(results) == len(data_list)
    assert all([r in data_list for r in results])


def test_get_all_spaces(openbis: Openbis, key_users: List[str]):
    """test get_all_spaces"""
    results = get_all_spaces(openbis)
    assert all([u in results for u in key_users])


def test_upload_new_dataset(
    openbis: Openbis, ochoung_exp: str, dataset_ab_dir: Path, ochoung_data: str
):
    data_to_add = dataset_ab_dir / ochoung_data
    upload_res = upload_new_dataset(
        openbis=openbis,
        experiment=ochoung_exp,
        dataset_type="TEST",
        data_name=data_to_add,
    )
    assert upload_res is not None


def test_get_datasets(
    openbis: Openbis, ochoung_exp: str, dataset_ab_dir: Path, ochoung_data: str
):
    data_to_add = dataset_ab_dir / ochoung_data
    upload_new_dataset(
        openbis=openbis,
        experiment=ochoung_exp,
        dataset_type="TEST",
        data_name=data_to_add,
    )
    saved_dataset = get_datasets(
        openbis=openbis, experiment=ochoung_exp, dataset_type="TEST"
    )
    assert ochoung_data in saved_dataset


def test_return_new_idx(
    openbis: Openbis,
    ochoung_exp: str,
    dataset_ab_dir: Path,
    ochoung_data: str,
):
    data_names = list(dataset_ab_dir.glob("BODE - OCHOUNG*"))
    data_to_add = dataset_ab_dir / ochoung_data
    upload_new_dataset(
        openbis=openbis,
        experiment=ochoung_exp,
        dataset_type="TEST",
        data_name=data_to_add,
    )
    new_idx = return_new_idx(
        openbis=openbis,
        experiment=ochoung_exp,
        dataset_type="TEST",
        data_names=data_names,
    )
    assert len(new_idx) == len(data_names) - 1
    assert new_idx == [nn for nn in data_names if nn.name != ochoung_data]
