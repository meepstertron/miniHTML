import os

print("Starting minihtml webserver...")

if os.path.exists("/app/minihtml"):
    os.chdir("/app/minihtml")
else:
    os.mkdir("/app/minihtml")
    with open("/app/minihtml/index.", "w") as f:
        f.write("""
                """)