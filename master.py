import sys
import subprocess
import atexit


def cleanup():
    for process in processes:
        process.kill()


atexit.register(cleanup)


tokens = []
with open("./tokens.txt", "r") as f:
    for line in f.readlines():
        if not line or line == "":
            continue
        tokens.append(line.replace('\n', '').strip())

print("Bots starting...")

processes = []
while len(tokens) > 0:
    token = tokens[0]
    tokens.pop(0)
    try:
        processes.append(subprocess.Popen([sys.executable, "bot.py", token, str(len(processes) + 1)]))
    except Exception as e:
        pass

exit_codes = [p.wait() for p in processes]

print("All bots finished running")
