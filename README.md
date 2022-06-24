# DeepLabCut WebUI

[![License](https://img.shields.io/github/license/jcwillox/deeplabcut-webui?style=for-the-badge)](https://github.com/jcwillox/deeplabcut-webui/blob/main/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/jcwillox/deeplabcut-webui?style=for-the-badge)](https://github.com/jcwillox/deeplabcut-webui/releases)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

[![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)](https://vuejs.org)
[![Vuetify](https://img.shields.io/badge/Vuetify-1867C0?style=for-the-badge&logo=vuetify&logoColor=AEDDFF)](https://vuetifyjs.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)

## Docs

For more information on how to use this software, check out the online documentation.
https://jcwillox.github.io/deeplabcut-webui/docs

## Setup

<details open>
<summary>Requirements</summary>

- `node`, we are targeting the latest LTS version, currently [NodeJS 16](https://nodejs.org/en/download/).
- `pnpm`, is the frontend package manager, just enable [corepack](https://nodejs.org/api/corepack.html) using `corepack enable` and it will automatically be installed when you try to use it. See [pnpm.io/installation#using-corepack](https://pnpm.io/installation#using-corepack) for more info.
- `task`, this is optional but is needed for running the scripts in [Taskfile.yaml](Taskfile.yaml), see [taskfile.dev/#/installation](https://taskfile.dev/#/installation). For Windows users we have a script to download task and add it to the system path, see [scripts/install-task.ps1](scripts/install-task.ps1).

</details>

<details>
<summary>Using a Virtual Environment</summary>

- Install **Python 3.8+**, on debian you may also need to install the `python3-venv` package.
- Install [`ffmpeg`](https://ffmpeg.org/download.html), if you are on Windows and used the `install-task.ps1` script you can download ffmpeg-full from [gyan.dev](https://www.gyan.dev/ffmpeg/builds) and place the exe files in `~/.local/bin`.
- Clone and `cd` into the repository.
- Run `task setup`, this will create a Python virtual environment in `.venv` and install the frontend and backend dependencies.
  - This can also be run to update the environments/dependencies after pulling the project.
- Everything is set up now, however, you will need to change the Python interpreter inside your editor manually to use the virtual environment.
  - **VSCode**: open the `backend/app/main.py` file, press `F1`, find "Python: Select interpreter", select the interpreter called `.venv`, you may need to click the refresh icon in the top-right first.
- You can start the frontend and backend with `task fullstack`, run `task -l` to see additional scripts.
- Additionally, when using **VSCode** you can press `F1` and search for `Task: Run Task`, then select whether you'd like to run the frontend, backend or both.

```bash
# after installing node and python
corepack enable
git clone https://github.com/jcwillox/deeplabcut-webui
cd deeplabcut-webui
task setup
# run frontend & backend
task fullstack
```

</details>

<details>
<summary>Using Conda (inc. DeepLabCut)</summary>

- Install `conda`, it's recommended to install [miniconda](https://docs.conda.io/en/latest/miniconda.html). Make sure you tell it to add `conda` to your `PATH`.
- **GPU Support** (optional) you will need to install your graphics card driver (you likely already have) and then install cuda support https://developer.nvidia.com/cuda-downloads. See [here](https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/installation.md#gpu-support) for more info.
- After installing conda run `conda init <shell>`, e.g. `conda init powershell`.
  - You can revert this later with `conda init <shell> --reverse`.
- _Optional_: Run `conda config --set auto_activate_base false` this will stop conda from switching to the default conda `(base)` environment whenever you open PowerShell.
- Clone and `cd` into the repository.
- Run `task setup-conda-node`, this will set up the environments/dependencies for the project.
  - This can also be run to update the environments/dependencies after pulling the project.
- Run `conda activate dlc-webui`.
- Everything is set up now, however, you will need to change the Python interpreter inside your editor manually to use the conda environment.
  - **VSCode**: open the `backend/app/main.py` file, press `F1`, find "Python: Select interpreter", select the interpreter called `dlc-webui`, you may need to click the refresh icon in the top-right first.
- You can start the DeepLabCut GUI with `task dlc-gui`, or start the frontend and backend with `task fullstack`, run `task -l` to see additional scripts.
- Additionally, when using **VSCode** you can press `F1` and search for `Task: Run Task`, then select whether you'd like to run the frontend, backend or both.

```bash
# after installing node and conda
corepack enable
git clone https://github.com/jcwillox/deeplabcut-webui
cd deeplabcut-webui
task setup-conda-node
# run frontend & backend
conda activate dlc-webui
task fullstack
```

</details>
