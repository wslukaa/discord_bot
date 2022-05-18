import datetime
import os
import random
import signal
import sys
import threading
import time
import discum
import config


bot = discum.Client(token=sys.argv[1], log={"console": False, "file": False})


@bot.gateway.command
def on_event(resp):
    if resp.event.ready_supplemental:
        try:
            user = bot.gateway.session.user
            print(f"Bot {sys.argv[2]}: Logged in as {user['username']}#{user['discriminator']}")
            thread = threading.Thread(target=send_msgs, args=())
            thread.start()
            guilds = bot.gateway.session.guilds
            for guild_id, guild in guilds.items():
                bot.gateway.request.lazyGuild(guild_id, {1: [[0, 99]]}, typing=True, threads=False, activities=True, members=[])
        except Exception as e:
            print(f"Bot {sys.argv[2]}: Critical error! Failed to start")


def send_msgs():
    while True:
        try:
            time_to_wait = random.randint(config.min_wait_time, config.max_wait_time)
            print(f"Bot {sys.argv[2]}: Waiting {time_to_wait}s before sending the next message...")
            time.sleep(time_to_wait)

            with open("./msgs.txt", "r") as f:
                lines = []
                for line in f.readlines():
                    lines.append(line.replace('\n', '').strip())
                msg = random.choice(lines)

            print(f"Bot {sys.argv[2]}: Sending message '{msg}'")
            bot.sendMessage(str(config.channel_id), message=msg)
        except Exception as e:
            pass


# Start bot
try:
    random.seed(int(sys.argv[2]) + int(datetime.datetime.utcnow().timestamp()))
    bot.gateway.run()
except Exception as e:
    print(f"Bot {sys.argv[2]}: Critical error! Token is probably dead")
    os.kill(os.getppid(), signal.SIGINT)
