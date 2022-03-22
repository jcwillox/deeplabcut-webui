# DeepLabCut WebUI

## Setup

- Install the [requirements](#requirements) listed below.
- After installing conda run `conda init <shell>`, e.g. `conda init powershell`.
  - You can revert this later with `conda init <shell> --reverse`.
- *Optional*: Run `conda config --set auto_activate_base false` this will stop conda from switching to the default conda `(base)` environment whenever you open PowerShell.
- Clone and `cd` into the repository.
- Run `task setup-conda`, this will create the conda environment for this project.
- Run `conda activate dlc-webui`.
- Run `cd frontend` and `pnpm install` to install the frontend packages.
- Everything is set up now, however, you will need to change the python interpreter inside your editor manually to use the conda environment.
  - **VSCode**: open the `backend/main.py` file, press `F1`, find "Python: Select interpreter", select the interpreter called `dlc-webui`, you may need to click the refresh icon in the top-right first.
- You can start the DeepLabCut GUI with `task dlc-gui`, or start the frontend and backend with `task fullstack`, run `task -l` to see additional scripts.
- Additionally, when using **VSCode** you can press `F1` and search for `Task: Run Task`, then select whether you'd like to run the frontend, backend or both.

## Requirements

- `conda`, it's recommended to install [miniconda](https://docs.conda.io/en/latest/miniconda.html).
- `node`, we are targeting the latest LTS version, currently [NodeJS 16](https://nodejs.org/en/download/).
- `pnpm`, is the frontend package manager, just enable [corepack](https://nodejs.org/api/corepack.html) `corepack enable` and node will install it for you when you try to use it. See [pnpm.io/installation#using-corepack](https://pnpm.io/installation#using-corepack) for more info.
- `task`, this is optional but is needed for running the scripts in [Taskfile.yaml](Taskfile.yaml), see [taskfile.dev/#/installation](https://taskfile.dev/#/installation). For Windows users we have a script to download task and add it to the system path, see [scripts/install-task.ps1](scripts/install-task.ps1).
- **GPU Support** (optional) you will need to install your graphics card driver (you likely already have) and then install cuda support https://developer.nvidia.com/cuda-downloads. See [here](https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/installation.md#gpu-support) for more info.
