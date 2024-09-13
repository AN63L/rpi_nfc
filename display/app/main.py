from RPLCD.i2c import CharLCD
from typing import Union
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from tinydb import TinyDB, Query

import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lcd = CharLCD(i2c_expander="PCF8574", address=0x3F, port=1, cols=16, rows=2, dotsize=10)
db = TinyDB("db.json")
db.truncate()
db.insert({"status": "INIT"})


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/status")
def status():
    status = get_status()
    return {"response": "ok", "status": status}


@app.get("/reset")
def reset():
    # set status to READY
    while get_status() == "WRITING":
        print("still writing text to lcd...\n")
    print("Long text written")
    # wait for message to end before clearing
    clear()
    db.update({"status": "RESET"}, Query().status.exists())
    print(db.all())
    return {"response": "ok"}


@app.get("/available")
def available():
    while get_status() == "WRITING":
        print("still writing text to lcd...\n")
    print("Long text written")
    clear()
    welcome_framebuffer = [
        "PLEASE COME IN !",
        "",
    ]
    concentrating = "I'm concentrating on something, I'd rather not get interrupted"
    display(concentrating, welcome_framebuffer, "AVAILABLE")

    print(db.all())
    return {"response": "ok"}


@app.get("/in_meeting")
def in_meeting():
    while get_status() == "WRITING":
        print("still writing text to lcd...\n")
    print("Long text written")
    clear()
    dnd_framebuffer = [
        "DO NOT DISTURB",
        "",
    ]
    meeting = "I'm in a meeting !"
    display(meeting, dnd_framebuffer, "MEETING")

    print(db.all())
    return {"response": "ok"}


def get_status():
    for item in db:
        print("item: ", item)
        status = item["status"]
    return status


def clear():
    lcd.close(clear=True)


def loop_string(string, lcd, framebuffer, row, num_cols, delay=0.2):
    padding = " " * num_cols
    s = padding + string + padding
    for i in range(len(s) - num_cols + 1):
        framebuffer[row] = s[i : i + num_cols]
        write_to_lcd(lcd, framebuffer, num_cols)
        time.sleep(delay)


def write_to_lcd(lcd, framebuffer, num_cols):
    """Write the framebuffer out to the specified LCD."""
    lcd.home()
    for row in framebuffer:
        lcd.write_string(row.ljust(num_cols)[:num_cols])
        lcd.write_string("\r\n")


def display(message, buffer, status):
    # set status to writing
    db.update({"status": "WRITING"}, Query().status.exists())

    # loop text second row
    loop_string(message, lcd, buffer, 1, 16)
    # set status to status
    db.update({"status": status}, Query().status.exists())
