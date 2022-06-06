from setuptools import setup

REQUIRES = [
    "fastapi==0.75.2",
    "pydantic>=1.9.0,<2",
    "pandas>=1.4.2,<2",
    "tables>=3.7.0,<4",
    "python-dotenv==0.20.0",
    "uvicorn[standard]==0.17.6",
    "opencv-python>=4.5.5.64,<5",
    "natsort>=8.1.0,<9",
    "numpy>=1.22.3,<2",
    "decord==0.6.0",
    "PyYAML>=6.0,<7.0",
]

DLC_REQUIRES = [
    "deeplabcut[gui]>=2.2.1,<3",
]

with open("requirements-docs.txt") as file:
    DOCS_REQUIRES = file.read().splitlines(keepends=False)

BUILD_REQUIRES = [
    "pyinstaller>=5.1,<6",
]

EXTRAS_REQUIRE = {
    "dlc": DLC_REQUIRES,
    "docs": DOCS_REQUIRES,
    "build": BUILD_REQUIRES,
}

if __name__ == "__main__":
    setup(install_requires=REQUIRES, extras_require=EXTRAS_REQUIRE)
