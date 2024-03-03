import RPi.GPIO as GPIO
from pn532 import *
import time
import binascii
import nfc
import ndef

if __name__ == "__main__":
    try:
        print("starting...")
        clf = nfc.ContactlessFrontend()
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

        print("setting up LEDs")
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        GPIO.setup(25, GPIO.OUT)
        GPIO.output(25, GPIO.LOW)
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, GPIO.LOW)
        GPIO.setup(27, GPIO.OUT)
        print("LEDs setup")

        print("WHITE LED on")
        GPIO.output(27, GPIO.HIGH)

        print("Waiting for RFID/NFC card...")
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            # print(".", end="")
            # Try again if no card is available.
            if uid is None:
                continue
            print("uid: ", uid)

            print("Found card with UID:", [hex(i) for i in uid])
            print("Card UID 0x{0}".format(binascii.hexlify(uid)))
            for i in uid:
                print("i: ", i, end="\n")
                print("hex(i)", hex(i), end="\n")
                # octets = bytearray.fromhex(hex(i))
                # for record in ndef.message_decoder(octets):
                #     print(record)
                data = pn532.mifare_classic_read_block(4)
                print("data: ", data)
                print("length: ", len(data))
                print("decode: ", data.decode("ascii"))
                # octets = bytearray.fromhex(hex(i))
                # for record in ndef.message_decoder(data):
                #     print(record)
                # value = pn532.mifare_classic_get_value_block(hex(i))
                # print("value: ", value)
            #     # , 196, 112, 209
            #     if i == 0:
            #         print("i: ", i, end="\n")
            #         print("hex(i)", hex(i), end="\n")
            #         data = pn532.mifare_classic_read_block(4)
            #         print("data: ", data)
            # print("decode: ", data.decode("utf-8"))
            # value = pn532.mifare_classic_get_value_block(data)
            # print("value: ", value)
            # # block = pn532.ntag2xx_read_block(i)
            # # print("block: ", block)

            print("WHITE LED off")
            GPIO.output(27, GPIO.LOW)

            print("GREEN LED on")
            GPIO.setup(25, GPIO.OUT)
            GPIO.output(25, GPIO.HIGH)
            time.sleep(1)

            print("GREEN LED off")
            GPIO.output(25, GPIO.LOW)
            GPIO.setup(27, GPIO.OUT)

            print("WHITE LED on")
            GPIO.output(27, GPIO.HIGH)

    except Exception as e:
        print("ERROR:", e)
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        GPIO.setup(27, GPIO.OUT)
        print("RED LED on")
        GPIO.output(27, GPIO.HIGH)
        time.sleep(1)
    finally:
        GPIO.cleanup()
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        # GPIO.setup(22, GPIO.OUT)
        # print("LED on")
        # GPIO.output(22, GPIO.HIGH)
# import RPi.GPIO as GPIO
# from pn532 import *

# # nfcpy module
# import nfc

# # ndeflib module
# import ndef

# from binascii import hexlify
# import logging
# import sys
# import time

# if __name__ == "__main__":
#     try:
#         print("starting...")
#         clf = nfc.ContactlessFrontend()

#         print("setting up LEDs")
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setwarnings(False)
#         GPIO.setup(25, GPIO.OUT)
#         GPIO.output(25, GPIO.LOW)
#         GPIO.setup(22, GPIO.OUT)
#         GPIO.output(22, GPIO.LOW)
#         GPIO.setup(27, GPIO.OUT)
#         print("LEDs setup")

#         print("WHITE LED on")
#         GPIO.output(27, GPIO.HIGH)

#         print("Waiting for RFID/NFC card...")
#         while True:
#             #     target = None
#             try:
#                 tta_bitrate = 212
#                 print("setting target...")
#                 target = nfc.clf.LocalTarget(str(tta_bitrate) + "A")
#                 print("target set")
#                 print("target: ", target)
#                 target.sens_res = bytearray(b"\x01\x01")
#                 # target.sdd_res = uid
#                 target.sel_res = bytearray(b"\x00")
#                 target = clf.listen(target, 3600)
#                 if target and target.tt2_cmd:
#                     logging.debug("rcvd TT2_CMD %s", hexlify(target.tt2_cmd).decode())
#                     print("{0} {1}".format(time.strftime("%X"), target))
#             except nfc.clf.CommunicationError as error:
#                 logging.error("%r", error)
#             except AssertionError as error:
#                 print(str(error), file=sys.stderr)

#         print("WHITE LED off")
#         GPIO.output(27, GPIO.LOW)

#         print("GREEN LED on")
#         GPIO.setup(25, GPIO.OUT)
#         GPIO.output(25, GPIO.HIGH)
#         time.sleep(1)

#         print("GREEN LED off")
#         GPIO.output(25, GPIO.LOW)
#         GPIO.setup(27, GPIO.OUT)

#         print("WHITE LED on")
#         GPIO.output(27, GPIO.HIGH)

#     except Exception as e:
#         print("ERROR:", e)
#         # GPIO.setmode(GPIO.BCM)
#         # GPIO.setwarnings(False)
#         GPIO.setup(27, GPIO.OUT)
#         print("RED LED on")
#         GPIO.output(27, GPIO.HIGH)
#         time.sleep(1)
#     finally:
#         GPIO.cleanup()
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(22, GPIO.OUT)
# print("LED on")
# GPIO.output(22, GPIO.HIGH)
