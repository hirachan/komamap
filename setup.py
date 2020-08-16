from typing import List
import re
import os
from setuptools import find_packages
from setuptools import setup
import glob


INSTALL_REQUIRES = [
    "folium",
    "selenium",
    "chromedriver-binary==84.0.4147.30.0",
    "Pillow",
    "gpxpy",
    "geopy",
    "requests",
    "xlrd",
]
EXTRA_REQUIRES = {
    "test": [
        "pytest",
        "pylint",
        "flake8",
        "autopep8",
    ],
}
CONSOLE_SCRIPTS = [
    "komamap = komamap.cli:main",
]
DATA_DIRS = []


def get_data_files(data_dirs: List[str]) -> List[str]:
    data_files = []
    cwd = os.getcwd()
    os.chdir(os.path.join("src", "komamap"))
    for data_dir in data_dirs:
        data_files += glob.glob(os.path.join(data_dir, "**"), recursive=True)
    os.chdir(cwd)

    return data_files


def main():
    if os.path.exists("src/komamap/__init__.py"):
        with open("src/komamap/__init__.py", "rt", encoding="utf8") as f:
            version = re.search(r"""__version__\s*=\s*["']([^"']+)["']""", f.read()).group(1)
    else:
        version = "0.0.0"

    if DATA_DIRS:
        data_files = get_data_files(DATA_DIRS)
    else:
        data_files = []

    setup(
        name="komamap",
        version=version,
        packages=find_packages("src"),
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRA_REQUIRES,
        package_dir={"": "src"},
        package_data={
            'komamap': data_files
        },
        python_requires=">=3.6",
        entry_points={
            "console_scripts": CONSOLE_SCRIPTS
        },
    )


if __name__ == "__main__":
    main()
