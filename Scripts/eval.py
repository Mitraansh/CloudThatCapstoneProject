import argparse
from pathlib import Path

from Backend import db


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple Flower Shop project evaluator")
    parser.add_argument("--repo", default=".", help="Repository root")
    args = parser.parse_args()
    repo = Path(args.repo)
    db_path = repo.joinpath("Database", "flower_shop.db")
    print("Flower Shop evaluator")
    print("DB exists:", db_path.exists())
    print("Schema exists:", repo.joinpath("Database", "schema.sql").exists())


if __name__ == "__main__":
    main()
