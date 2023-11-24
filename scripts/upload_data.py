from pathlib import Path
from typing import Dict, List

from pybis import Openbis

from scripts.utils import get_config

CONFIG = get_config()

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
        experiment=experiment, type=dataset_type, attrs=["name"]
    )
    return datasets.df["name"].tolist()


def get_all_pdf_files(instrument_dir: Path) -> List[Path]:
    return list(instrument_dir.glob("**/pdf/*.pdf"))


if __name__ == "__main__":
    dataset_type = "COMPACT"
    dataset_ab_dir = Path("/Volumes/compact-20260/")

    openbis = get_openbis(CONFIG)

    users = get_all_users(openbis)
    all_dataset = get_all_pdf_files(dataset_ab_dir)

    # space for all users
    # per user project/ experiment
    # per experiment upload dataset, but check if that dataset is already uploaded
    for user in users:
        user_files = [fn for fn in all_dataset if f"Bode - {user}-" in fn.name]
        for proj in get_projects(openbis=openbis, user=user):
            for exp in get_experiments(openbis=openbis, user=user, project=proj):
                data_names = [
                    str(fn)
                    for fn in user_files
                    if f"Bode - {user}-{proj}-{exp}" in fn.name
                ]
                for existing_fn in get_datasets(
                    openbis=openbis, experiment=exp, dataset_type=dataset_type
                ):
                    if existing_fn in data_names:
                        data_names.remove(existing_fn)
                ds_new = openbis.new_dataset(
                    type=dataset_type,
                    experiment=openbis.get_experiment(f"/{user}/{proj}/{exp}"),
                    files=data_names,
                    props=[
                        {
                            "$name": fn.split("/")[-1].split(".")[0],
                        }
                        for fn in data_names
                    ],
                )
                ds_new.save()
