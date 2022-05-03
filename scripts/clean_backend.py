import os
import shutil
from glob import glob

os.chdir(os.path.dirname(os.path.dirname(__file__)))

shutil.rmtree("backend/dist/", ignore_errors=True)
shutil.rmtree("backend/build/", ignore_errors=True)
shutil.rmtree("backend/.pytest_cache/", ignore_errors=True)

for path in glob("backend/*.egg-info"):
    shutil.rmtree(path, ignore_errors=True)

for path in glob("backend/**/__pycache__/", recursive=True):
    shutil.rmtree(path, ignore_errors=True)
