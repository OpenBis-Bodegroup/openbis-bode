import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List

from pybis import Openbis

from bode_loader.utils import get_config, timeit

CONFIG = get_config()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s"
)
for handler in logger.handlers:
    logger.removeHandler(handler)
handler_out = logging.StreamHandler(sys.stdout)
handler_out.setFormatter(log_formatter)
logger.addHandler(handler_out)


def get_openbis(config: Dict = CONFIG) -> Openbis:
    """get openbis instance

    Args:
        config (Dict, optional): config of openbis setting. Defaults to CONFIG.

    Returns:
        Openbis: openbis instance
    """
    return Openbis(config["host"]["host_name"], token=config["host"]["token"])


@timeit
def get_all_spaces(openbis: Openbis) -> List[str]:
    spaces = openbis.get_spaces()
    return [
        space["code"]
        for space in spaces.response["objects"]
        if space["registrator"]["userId"] != "system"
    ]


def get_projects(openbis: Openbis, user: str) -> List[str]:
    projects = openbis.get_projects(space=user)
    return [
        project["identifier"]["identifier"] for project in projects.response["objects"]
    ]


def get_experiments(openbis: Openbis, project: str) -> List[str]:
    experiments = openbis.get_experiments(project=project)
    return [
        experiment["identifier"]["identifier"]
        for experiment in experiments.response["objects"]
    ]


def get_datasets(openbis: Openbis, experiment: str, dataset_type: str) -> List[str]:
    datasets = openbis.get_datasets(
        experiment=experiment, type=dataset_type, props=["$NAME"]
    )
    return_datasets = []
    for dataset in datasets.response["objects"]:
        if "$NAME" in dataset["properties"].keys():
            return_datasets.append(dataset["properties"]["$NAME"])
    return return_datasets


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
        experiment (str): experiment code, e.t., "/{usr}/projectname/experimentname"
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


@timeit
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
        type=str,
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
        type=str,
        default="Bode - ",
        help="absolute prefix of the pdf file name",
    )
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace):
    dataset_ab_dir = Path(args.dataset_ab_dir)

    openbis = get_openbis(CONFIG)

    all_dataset = get_all_files(dataset_ab_dir, hierarchy=args.hierarchy)
    logger.info(f"Found {len(all_dataset)} matching files in {dataset_ab_dir}")
    if len(all_dataset) == 0:
        return 1

    users = get_all_spaces(openbis)  # all the users' spaces
    logger.info(f"There are {len(users)} registered users in openBIS: {users}")

    # space for all users
    # per user project/ experiment
    # per experiment upload dataset, but check if that dataset is already uploaded
    for user in users:
        user_files = [
            fn for fn in all_dataset if f"{user.upper()}" in str(fn.name).upper()
        ]
        logger.info(f"Processing user: {user}, has {len(user_files)} files")
        if len(user_files) == 0:
            continue
        for proj in get_projects(
            openbis=openbis, user=user
        ):  # proj = "/{usr}/projectname/"
            for exp in get_experiments(
                openbis=openbis, project=proj
            ):  # exp = "/{usr}/projectname/experimentname/"
                data_prefix = "-".join(exp.upper().split("/")[1:])
                data_names = [
                    fn
                    for fn in user_files
                    if f"{args.ab_prefix}{data_prefix}" in fn.name
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
    openbis.logout()


if __name__ == "__main__":
    args = get_args()
    openbis = get_openbis(CONFIG)
    # main(args)
