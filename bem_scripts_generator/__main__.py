import sys
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from pathlib import Path
from uuid import uuid4

from jinja2 import Environment, PackageLoader
from pandas import Timedelta

from . import resource_map


def get_time_val(dataset: Path, threshold: float) -> str:
    base = resource_map.time[dataset.stem]
    base = Timedelta(base) * 10
    result = base * threshold
    result = str(result).split()[-1]
    result = result.split(".", 1)[0]

    return result


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

        outfile = config_dir / f"config_{thresh}.json"
        outfile.write_text(config, encoding="utf-8")

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

                script_file = scripts_dir / f"run_{run_id}.sh"
                script_file.write_text(script, encoding="utf-8")

    scripts = list(scripts_dir.glob("*.sh"))
    with (scripts_dir / "submit.sh").open("wt", encoding="utf-8") as handle:
        for script in scripts:
            handle.write(f"sbatch {script}\n")


def cli():
    main(parse_args())


if __name__ == "__main__":
    cli()
