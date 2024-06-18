from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from csv import writer as csv_writer
from pathlib import Path
from typing import NamedTuple


class ResultItem(NamedTuple):
    dataset: str
    threshold: int
    count: int


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument("directory")
    parser.add_argument("-o", "--output", type=str, default="./summary.csv")

    return parser.parse_args()


def threhsold_key(path: Path) -> float:
    return float(path.name)


def main(args: Namespace):
    root = Path(args.directory)
    result = []

    for dataset in sorted(root.glob("*")):
        for threshold in sorted(dataset.glob("*"), key=threhsold_key):
            result.append(
                ResultItem(
                    dataset=dataset.name,
                    threshold=threshold.name,
                    count=len(tuple(threshold.glob("*.csv"))),
                )
            )

    with open(args.output, "wt", encoding="utf-8") as handle:
        writer = csv_writer(handle)
        writer.writerow(ResultItem._fields)
        writer.writerows(result)


def cli():
    main(parse_args())


if __name__ == "__main__":
    cli()
