# opensim.py
import subprocess
from config import OPENSIM_PATH, OPENSIM_DIR

def start_opensim():
    return subprocess.Popen(
        [OPENSIM_PATH, "-console=basic"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=OPENSIM_DIR
    )