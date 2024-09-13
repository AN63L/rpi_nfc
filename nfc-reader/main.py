import RPi.GPIO as GPIO
from pn532 import *
import time
import binascii
import requests

# green -> free
# red -> in meeting
# white -> thinking or initial


def toggle_status():
    while get_status() == "WRITING":
        print("still writing text to lcd...\n")

    status = get_status()
    if status == "MEETING":
        print("status is MEETING - changing to AVAILABLE")
        set_available()
    elif status == "AVAILABLE":
        print("status is AVAILABLE - changing to MEETING")
        set_in_meeting()
    elif status == "INIT" or status == "RESET":
        print("status is INIT or RESET - changing to AVAILABLE")
        set_available()


def get_status():
    print("getting status...")
    leds_off()
    white_led_on()
    response = requests.get("http://lcddisplay.local:80/status")
    print("response: ", response.json())
    print("status: ", response.json()["status"])
    white_led_off()
    return response.json()["status"]


def set_available():
    print("setting available...")
    leds_off()
    white_led_on()
    response = requests.get("http://lcddisplay.local:80/available")
    white_led_off()
    print("response: ", response.json())


def set_in_meeting():
    print("setting in meeting...")
    leds_off()
    white_led_on()
    response = requests.get("http://lcddisplay.local:80/in_meeting")
    white_led_off()
    print("response: ", response.json())


def reset_status():
    print("resetting...")
    leds_off()
    white_led_on()
    response = requests.get("http://lcddisplay.local:80/reset")
    white_led_off()
    print("response: ", response.json())


# valid card UID: 80a84f3e
def nfc_reader():
    print("starting...")
    # pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    pn532 = PN532_I2C(debug=False, reset=20, req=16)
    # pn532 = PN532_UART(debug=False, reset=20)
    print("getting firmware version....")
    ic, ver, rev, support = pn532.get_firmware_version()
    print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

    print("configuring PN532....")
    # Configure PN532 to communicate with MiFare cards
    pn532.SAM_configuration()
    print("PN532 communicating with MiFare cards")

    print("Waiting for RFID/NFC card...")
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is None:
            continue

        print("uid: ", uid)
        print("Found card with UID:", [hex(i) for i in uid])
        print("Card UID 0x{0}".format(binascii.hexlify(uid)))
        print("Card UID => ", uid.hex())
        print("Card UID => ", str(uid.hex()))

        if str(uid.hex()) == "80a84f3e":
            print("CORRECT ID FOR TOGGLE")
            leds_off()
            blinking_green_led()
            toggle_status()
            handle_led_status()
        else:
            print("UNKNOWN ID - RESET")
            leds_off()
            blinking_red_led()
            reset_status()
            handle_led_status()


def blinking_white_led():
    print("blinking white led..")
    for i in range(3):
        white_led_on()
        white_led_off()


def blinking_red_led():
    print("blinking red led..")
    for i in range(3):
        red_led_on()
        red_led_off()


def blinking_green_led():
    print("blinking green led..")
    for i in range(3):
        green_led_on()
        green_led_off()


def green_led_on():
    print("GREEN LED on")
    GPIO.output(25, GPIO.HIGH)
    time.sleep(1)


def green_led_off():
    print("GREEN LED off")
    GPIO.output(25, GPIO.LOW)
    time.sleep(0.5)


def red_led_on():
    print("RED LED on")
    GPIO.output(22, GPIO.HIGH)
    time.sleep(1)


def red_led_off():
    print("RED LED off")
    GPIO.output(22, GPIO.LOW)
    time.sleep(0.5)


def white_led_on():
    print("WHITE LED on")
    GPIO.output(27, GPIO.HIGH)
    time.sleep(1)


def white_led_off():
    print("WHITE LED off")
    GPIO.output(27, GPIO.LOW)
    time.sleep(0.5)


def leds_off():
    print("turning LEDs off")
    white_led_off()
    red_led_off()
    green_led_off()


def handle_led_status():
    print("handling led status...")
    status = get_status()
    leds_off()
    if status == "MEETING":
        print("status is MEETING")
        red_led_on()
    elif status == "AVAILABLE":
        print("status is AVAILABLE")
        green_led_on()
    elif status == "INIT":
        print("status is INIT")
        white_led_on()
    elif status == "RESET":
        print("status is RESET")
        white_led_on()
    if status == "WRITING":
        print("status is WRITING")
        red_led_on()


def setup_leds():
    print("setting up LEDs")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    print("GREEN LED")
    GPIO.setup(25, GPIO.OUT)
    GPIO.output(25, GPIO.LOW)
    print("RED LED")
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, GPIO.LOW)
    print("WHITE LED")
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(22, GPIO.LOW)
    print("LEDs setup")

    white_led_on()
    handle_led_status()


def main():
    try:
        setup_leds()
        nfc_reader()
    except Exception as e:
        print("ERROR:", e)
        leds_off()
        blinking_red_led()
        main()


if __name__ == "__main__":
    main()
