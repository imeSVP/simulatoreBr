import sys
import time
import globals_and_constants


def update_heartbeat():
    workGroup = globals_and_constants.get_value("workGroup")
    HEARTBEAT_FILE = f"heartbeat_{workGroup}.txt"
    with open(HEARTBEAT_FILE, "w") as f:
        f.write(str(int(time.time())))
