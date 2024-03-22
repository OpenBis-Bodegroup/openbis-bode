from typing import Dict, List

from pybis import Openbis

from bode_loader.utils import CONFIG


def get_openbis(config: Dict = CONFIG) -> Openbis:
    """get openbis instance

    Args:
        config (Dict, optional): config of openbis setting. Defaults to CONFIG.

    Returns:
        Openbis: openbis instance
    """
    return Openbis(config["host"]["host_name"], token=config["host"]["token"])


def get_all_spaces(openbis: Openbis) -> List[str]:
    """get all spaces (in bode group structure, users)

    Args:
        openbis (Openbis): Openbis instance

    Returns:
        List[str]: List if space names (user names)
    """
    spaces = openbis.get_spaces()
    return [
        space["code"]
        for space in spaces.response["objects"]
        if space["registrator"]["userId"] != "system"
    ]


def get_projects(openbis: Openbis, user: str) -> List[str]:
    """get project codes of a user
    This function directly use json response from openbis

    Args:
        openbis (Openbis): Openbis instance
        user (str): user name (identifier)

    Returns:
        List[str]: a list of project codes
            e.g., ["/{usr}/projectcode/", "/{usr}/projectcode2/"]
    """
    projects = openbis.get_projects(space=user)
    return [
        project["identifier"]["identifier"] for project in projects.response["objects"]
    ]


def get_experiments(openbis: Openbis, project: str) -> List[str]:
    """get experiment codes of a project

    Args:
        openbis (Openbis): Openbis instance
        project (str): project code

    Returns:
        List[str]: a list of experiment codes
            e.g., ["/{usr}/projectcode/experimentcode/", "/{usr}/projectcode/experimentcode2/"]
    """
    experiments = openbis.get_experiments(project=project)
    return [
        experiment["identifier"]["identifier"]
        for experiment in experiments.response["objects"]
    ]


def get_datasets(openbis: Openbis, experiment: str, dataset_type: str) -> List[str]:
    """get dataset names of an experiment

    Args:
        openbis (Openbis): Openbis instance
        experiment (str): experiment code
        dataset_type (str): dataset type

    Returns:
        List[str]: list of dataset names in the experiment
    """

    datasets = openbis.get_datasets(
        experiment=experiment, type=dataset_type, props=["$NAME"]
    )
    return_datasets = []
    for dataset in datasets.response:
        if "$NAME" in dataset["properties"].keys():
            return_datasets.append(dataset["properties"]["$NAME"])
    return return_datasets
