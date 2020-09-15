#!/bin/env python3
import sys
import argparse

from . import api


def get_opt() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='API')

    args = parser.parse_args()

    return args


def main() -> int:
    args = get_opt()

    api.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
