import argparse

from toncenter.__meta__ import __version__


def main() -> None:
    """CLI entry-point."""
    parser = argparse.ArgumentParser(
        prog="toncenter",
        description="toncenter CLI.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"toncenter {__version__}",
    )
    parser.parse_args()


if __name__ == "__main__":
    main()
