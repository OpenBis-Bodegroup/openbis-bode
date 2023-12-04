import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List

from pybis import Openbis
from utils import get_config, timeit

CONFIG = get_config()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
LOGGER = logging.getLogger(
    __name__,
)

# "/Volumes/compact-20260/*/pdf/Bode - *.pdf"
# "/Volumes/compact-20260/*/pdf/Bode - AEM-05-093-A-depro-16-3_P1-F-2_1_3336_OA-LCMS-Report.pdf"

# data_name = "Bode - USER_name-PRO_CODE-EXP_CODE-(description).pdf"
# encode_name = data_name.spilt(".")[0]


def get_openbis(config: Dict = CONFIG) -> Openbis:
    return Openbis(config["host"]["host_name"], token=config["host"]["token"])


def get_all_users(openbis: Openbis) -> List[str]:
    # TODO: get all users, not ideal
    spaces = openbis.get_spaces()
    return spaces.df["code"][spaces.df["registrator"] != "system"].tolist()


def get_projects(openbis: Openbis, user: str) -> List[str]:
    projects = openbis.get_projects(space=user)
    return projects.df["identifier"].tolist()


def get_experiments(openbis: Openbis, project: str) -> List[str]:
    experiments = openbis.get_experiments(project=project)
    return experiments.df["identifier"].tolist()


def get_datasets(openbis: Openbis, experiment: str, dataset_type: str) -> List[str]:
    datasets = openbis.get_datasets(
        experiment=experiment, type=dataset_type, props=["$NAME"]
    )
    return datasets.df["$NAME"].tolist()


@timeit
def get_all_pdf_files(
    instrument_dir: Path, hierarchy: str = "*/pdf/*.pdf"
) -> List[Path]:
    return list(instrument_dir.glob(hierarchy))


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
        default="*/pdf/*.pdf",
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


if __name__ == "__main__":
    args = get_args()
    dataset_ab_dir = Path(args.dataset_ab_dir)

    openbis = get_openbis(CONFIG)

    users = get_all_users(openbis)
    LOGGER.info(f"There are {len(users)} registered users in openBIS: {users}")
    all_dataset = get_all_pdf_files(dataset_ab_dir, hierarchy=args.hierarchy)
    LOGGER.info(f"Found {len(all_dataset)} pdf files in {dataset_ab_dir}")

    # space for all users
    # per user project/ experiment
    # per experiment upload dataset, but check if that dataset is already uploaded
    for user in users:
        user_files = [
            fn for fn in all_dataset if f"{user.upper()}" in str(fn.name).upper()
        ]
        LOGGER.info(f"Processing user: {user}, has {len(user_files)} files")
        for proj in get_projects(
            openbis=openbis, user=user
        ):  # proj = "/{usr}/projectname/"
            for exp in get_experiments(
                openbis=openbis, project=proj
            ):  # exp = "/{usr}/projectname/experimentname/"
                data_prefix = "-".join(exp.upper().split("/")[1:])
                data_names = [
                    str(fn)
                    for fn in user_files
                    if f"{args.ab_prefix}{data_prefix}" in fn.name
                ]
                # check if dataset already exists
                for existing_fn in get_datasets(
                    openbis=openbis, experiment=exp, dataset_type=args.dataset_type
                ):
                    for dn in data_names:
                        if existing_fn in dn:
                            # if existing_fn in dn, then remove it from data_names
                            data_names.remove(dn)
                # upload new datasets
                for data_name in data_names:
                    ds_new = openbis.new_dataset(
                        type=args.dataset_type,
                        experiment=openbis.get_experiment(exp),
                        files=data_name,
                        props={
                            "$name": data_name.split("/")[-1].split(".")[0],
                        },
                    )
                    ds_new.save()
