import requests
import subprocess
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("NTFY_LINK")

def get_kid_friendly_activity():
    while True:
        res = requests.get("https://bored-api.appbrewery.com/random")
        if res.status_code == 200:
            data = res.json()
            if data.get("kidFriendly"):
                msg = f"Are you Bored? Try this:\n {data['activity']}"
                link = data.get("link")
                if link:
                    msg += f"\n🔗 Learn more: {link}"
                return msg
        time.sleep(5)

def get_fun_fact():
    res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    if res.status_code == 200:
        fact = res.json().get("text")
        return f"do you know?\n{fact}"
    return None

def get_kid_joke():
    res = requests.get("https://official-joke-api.appspot.com/jokes/general/random")
    if res.status_code == 200:
        joke = res.json()[0]
        return f"here's a joke:\n{joke['setup']}\n {joke['punchline']}"
    return None

def get_random_dog():
    res = requests.get("https://dog.ceo/api/breeds/image/random")
    if res.status_code == 200:
        dog_url = res.json().get("message")
        return f"here's a cute dog for you!\n{dog_url}"
    return None

message_fetchers = [
    get_kid_friendly_activity,
    get_fun_fact,
    get_kid_joke,
    get_random_dog
]

while True:
    fetch_func = random.choice(message_fetchers)
    message = fetch_func()

    if message:
        print("Sending:\n", message)
        subprocess.run(["curl", "--max-time", "10", "-d", message, "https://ntfy.sh/bRg9quA4F2Sj2QQj"])
    else:
        print("failed to fetch data")

    time.sleep(7200)
