import argparse
import json
from pathlib import Path
from typing import List

from pybis import Openbis

from bode_loader.openbis_helper import get_datasets, get_openbis
from bode_loader.utils import get_bode_logger, timeit

LOGGER = get_bode_logger(__name__)


def upload_new_dataset(
    openbis: Openbis, experiment: str, dataset_type: str, data_name: Path
) -> int:
    ds_new = openbis.new_dataset(
        type=dataset_type,
        experiment=openbis.get_experiment(experiment),
        files=str(data_name),
        props={
            "$name": data_name.name,
        },
    )
    ds_new.save()
    # return the dataset id
    return ds_new.data["code"]


def return_new_idx(
    openbis: Openbis, experiment: str, dataset_type: str, data_names: List[Path]
) -> List[int]:
    """Get all the existing datasets in OpenBis and return only the new data's index

    Args:
        openbis (Openbis): openbis instance
        experiment (str): experiment code, e.t., "/{usr}/projectcode/experimentcode"
        dataset_type (str): dataset type, e.g., "COMPACT", "RAW", etc.
        data_names (List[Path]): list of data names

    Returns:
        List[int]: list of new dataset index
    """
    saved_datasets = get_datasets(
        openbis=openbis, experiment=experiment, dataset_type=dataset_type
    )
    new_idx = []
    for ii, dn in enumerate(data_names):
        if all([dn.name not in sd for sd in saved_datasets]):
            new_idx.append(ii)
    return new_idx


@timeit(LOGGER)
def get_all_files(
    instrument_dir: Path, hierarchy: List[str] = ["*/pdf/*.pdf"]
) -> List[Path]:
    """get all the files in the instrument directory

    Args:
        instrument_dir (Path): dir to the instrument folder
        hierarchy (List[str], optional): list of the file hierarchy. Defaults to ["*/pdf/*.pdf"].

    Returns:
        List[Path]: list of the flies that match the hierarchy
    """
    return_list: List[Path] = []
    for hier in hierarchy:
        return_list.extend(list(instrument_dir.glob(hier)))
    return return_list


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_type",
        type=str,
        default="COMPACT",
        help="dataset type, e.g. COMPACT, RAW, etc.",
    )
    parser.add_argument(
        "--dataset_ab_dir",
        type=Path,
        default="/Volumes/Bruker-Compact-1/",
        help="absolute path to the dataset directory",
    )
    parser.add_argument(
        "--hierarchy",
        type=str,
        nargs="+",
        default=["*/pdf/*.pdf"],
        help="hierarchy to search for pdf files",
    )
    parser.add_argument(
        "--ab_prefix",
        type=Path,
        default="Bode - ",
        help="absolute prefix of the pdf file name",
    )
    parser.add_argument(
        "--space_structure_path",
        type=Path,
        default="space_structure.json",
        help="path to the space structure json",
    )
    args = parser.parse_args()
    return args


@timeit(LOGGER)
def main(args: argparse.Namespace, openbis: Openbis):
    dataset_ab_dir = Path(args.dataset_ab_dir)

    all_dataset = get_all_files(dataset_ab_dir, hierarchy=args.hierarchy)
    LOGGER.info(f"Found {len(all_dataset)} matching files in {dataset_ab_dir}")
    if len(all_dataset) == 0:
        raise FileNotFoundError(f"No files found in {dataset_ab_dir}")

    # load space structure
    if not args.space_structure_path.exists():
        raise FileNotFoundError(
            f"{args.space_structure_path} does not exist, run fetch_space_structure.py first."
        )
    with open(args.space_structure_path, "r") as f:
        space_structure = json.load(f)

    for user_structure in space_structure["users"]:
        user = user_structure["name"]
        midfix = user_structure["midfix"]

        user_files = []
        user_exp_fix = set()
        for fn in all_dataset:
            for exp, fix in zip(user_structure["experiments"], midfix):
                if (f"{user.upper()}" in str(fn.name).upper()) and (
                    fix in str(fn.name).upper()
                ):
                    user_files.append(fn)
                    user_exp_fix.add((exp, fix))
                    break
        LOGGER.info(
            f"Processing user: {user}, has {len(user_files)} files \
in {len(user_exp_fix)} experiments."
        )
        if len(user_files) == 0:
            continue
        for exp, fix in user_exp_fix:
            data_names = [
                fn for fn in user_files if f"{args.ab_prefix}{fix}" in fn.name
            ]
            # check if dataset already exists
            new_idx = return_new_idx(
                openbis=openbis,
                experiment=exp,
                dataset_type=args.dataset_type,
                data_names=data_names,
            )
            data_names = [data_names[idx] for idx in new_idx]
            # upload new datasets
            for data_name in data_names:
                upload_new_dataset(
                    openbis=openbis,
                    experiment=exp,
                    dataset_type=args.dataset_type,
                    data_name=data_name,
                )


if __name__ == "__main__":
    args = get_args()
    openbis = get_openbis()
    main(args, openbis)
    openbis.logout()
