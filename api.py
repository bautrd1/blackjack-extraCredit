import requests
import json
import os

fn = "deck.txt"
DATA = {}


def create_deck(fn="deck.txt", force=False):
    if not os.path.exists(fn) or force:
        if not force:
            return
        try:
            os.remove(fn)
        except Exception as e:
            return
        resp = requests.get("https://deckofcardsapi.com/api/deck/new/")
        with open(fn, "a") as f:
            data = resp.json()
            for k in data:
                f.write(f"{k}={data[k]}\n")


if os.path.exists(fn):
    with open("deck.txt", "r") as f:
        for i in f:
            key, value = i.split("=")
            key, value = key.strip(), value.strip()
            DATA[key] = value
else:
    create_deck()


def shuffle():
    _id = DATA.get("deck_id")
    return requests.get(f"https://deckofcardsapi.com/api/deck/{_id}/shuffle/")


def draw(count=52):
    _id = DATA.get("deck_id")
    shuffle()
    data = []
    resp = requests.get(
        f"https://deckofcardsapi.com/api/deck/{_id}/draw/?count={count}"
    ).json()
    for i in resp["cards"]:
        data.append((i.get("code"), i.get("value")))
    shuffle()

    return data


