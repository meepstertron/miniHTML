import os
import time
import subprocess
import logging

def get_files_mod_times(directory):
    files_mod_times = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            files_mod_times[filepath] = os.path.getmtime(filepath)
    return files_mod_times

def has_any_file_changed(directory, last_mod_times):
    current_mod_times = get_files_mod_times(directory)
    for filepath, mod_time in current_mod_times.items():
        if filepath not in last_mod_times or last_mod_times[filepath] != mod_time:
            return True
    return False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("Starting minihtml webserver...")

if not os.path.exists("/app/html"):
    os.mkdir("/app/html")

if os.path.exists("/app/minihtml"):
    os.chdir("/app/minihtml")

else:
    os.mkdir("/app/minihtml")
    with open("/app/minihtml/index.minihtml", "w") as f:
        f.write("""
                [
                    p{Congratulations, mini html is up and running}
                ]
                """)
        


try:
    subprocess.run(["python", "/app/parse.py", "-d", "/app/minihtml", "-o", "/app/html"], check=True)
except subprocess.CalledProcessError as e:
    logger.error(f"Error running parse.py: {e}")

# Example usage
directory = "/app/minihtml"
last_mod_times = get_files_mod_times(directory)

while True:
    time.sleep(10)
    if has_any_file_changed(directory, last_mod_times):
        logger.info(f"Files in {directory} have been modified.")
        try:
            subprocess.run(["python", "/app/parse.py", "-d", directory, "-o", "/app/html"], check=True)
            last_mod_times = get_files_mod_times(directory)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running parse.py: {e}")
    else:
        logger.info(f"No files in {directory} have been modified.")