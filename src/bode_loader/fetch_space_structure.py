import argparse
import json
from pathlib import Path

from pybis import Openbis

from bode_loader.openbis_helper import (
    get_all_spaces,
    get_experiments,
    get_openbis,
    get_projects,
)
from bode_loader.utils import get_bode_logger, timeit

LOGGER = get_bode_logger(__name__)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch space structure")
    parser.add_argument(
        "--save_path",
        type=Path,
        default="space_structure.json",
        help="save path",
    )
    return parser.parse_args()


@timeit(LOGGER)
def main(args: argparse.Namespace, openbis: Openbis):
    structure = {"users": []}
    for user in get_all_spaces(openbis):
        experiments = []
        midfix = []

        for project in get_projects(openbis, user):
            for experiment in get_experiments(openbis, project):
                experiments.append(experiment)
                midfix.append("-".join(experiment.upper().split("/")[1:]))

        user_structure = {
            "name": user,
            "experiments": experiments,
            "midfix": midfix,
            "total_experiments": len(experiments),
        }
        structure["users"].append(user_structure)
    with open(args.save_path, "w") as f:
        json.dump(structure, f, indent=4)


if __name__ == "__main__":
    args = get_args()
    openbis = get_openbis()
    main(args, openbis)
    openbis.logout()
