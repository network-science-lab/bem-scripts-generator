import sys
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from pathlib import Path
from uuid import uuid4

from jinja2 import Environment, PackageLoader
from pandas import Timedelta

from . import resource_map


def get_time_val(dataset: Path, threshold: float) -> str:
    threshold = max(threshold, 0.1)

    base = resource_map.time[dataset.stem]
    result = Timedelta(base) * 10 * threshold

    result = str(result).split()
    days = int(result[0])
    result = result[-1]

    if days > 0:
        result = result.split()
        hours = int(result[0])
        hours = hours + (24 * days)
        result[0] = str(hours)
        result = ":".join(result)

    return result.split(".", 1)[0]


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "dataset_dir", help="Directory containing network data."
    )
    parser.add_argument("output_dir", help="Dir to store sim results.")
    parser.add_argument(
        "-n",
        "--n-iter",
        type=int,
        default=20,
        help="Number of repeated sims.",
    )
    parser.add_argument(
        "-t", "--thresholds", type=float, nargs="+", default=[0.1, 0.2, 0.3]
    )

    return parser.parse_args()


def main(args: Namespace):
    scripts_dir = Path("./scripts")
    scripts_dir.mkdir(exist_ok=True, parents=True)

    config_dir = scripts_dir / "configs"
    config_dir.mkdir(exist_ok=True, parents=True)

    dataset_dir = Path(args.dataset_dir)
    output_dir = Path(args.output_dir)

    jinja_env = Environment(loader=PackageLoader("bem_scripts_generator"))
    runner_template = jinja_env.get_template("run_job.sh")
    config_template = jinja_env.get_template("simulation_config.json")

    for thresh in args.thresholds:
        config = config_template.render(threshold=thresh)

        (config_dir / f"config_{thresh}.json").write_text(
            config, encoding="utf-8"
        )

    for dataset in dataset_dir.glob("*"):
        for thresh in args.thresholds:
            for run_id in range(args.n_iter):

                run_id = f"{dataset.stem}_{thresh}_{uuid4()}"
                output_path = (
                    output_dir / dataset.stem / str(thresh) / (run_id + ".csv")
                )

                script = runner_template.render(
                    python_path=sys.executable,
                    dataset_path=str(dataset),
                    config_path=config_dir / f"config_{thresh}.json",
                    output_path=output_path,
                    job_name=run_id,
                    memory=resource_map.memory[dataset.stem],
                    time=get_time_val(dataset, thresh),
                )

                (scripts_dir / f"run_{run_id}.sh").write_text(
                    script, encoding="utf-8"
                )

    with (scripts_dir / "submit.sh").open("wt", encoding="utf-8") as handle:
        for script in sorted(scripts_dir.glob("*.sh")):
            handle.write(f"sbatch {script}\n")


def cli():
    main(parse_args())


if __name__ == "__main__":
    cli()
