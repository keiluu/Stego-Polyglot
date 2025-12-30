from ..src.mem_loader import *

with open("/usr/bin/ls", "rb") as f:
    data = f.read()

load_and_exec(data)
