import sys
import subprocess
import PIL
from PIL import ImageGrab
import cv2
import numpy
import time
import pyautogui
from threading import Timer
from PIL import Image
from pytesseract import *
import random
from PIL import Image
from pytesseract import image_to_string
import discord

pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

Plan = '''Things to add...

    1.  Account name changer
    2.  Clan description changer
    3.  PLayer management
    4.  Automated application process
    5.  

'''

# >>> Tap Titans 2 bot by SilicalNZ#8156

# DO NOT CHANGE
Screen_Resolution = (1280, 720)
# Heavily repeated if cases
Home_Screen = (464, 663, (148, 60, 34))
Window_Screen = (720, 420, (83, 77, 75))
# Options
ClanQuest_DiamondCost = 5


# █▀▀█ █▀▀ █▀▀█ █▀▀ █▀▀█ ▀▀█▀▀ █▀▀
# █▄▄▀ █▀▀ █░░█ █▀▀ █▄▄█ ░░█░░ ▀▀█
# ▀░▀▀ ▀▀▀ █▀▀▀ ▀▀▀ ▀░░▀ ░░▀░░ ▀▀▀
def pixelMatchesColor_wait(x, y, rgb):
    while True:
        if pyautogui.pixelMatchesColor(x, y, rgb):
            return


def ocr(pos, ints):
    image = numpy.array(PIL.ImageGrab.grab(bbox=(pos[0], pos[1], pos[2], pos[3])))
    image = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2RGB)
    image = cv2.resize(image, (0, 0), fx=4, fy=4)
    ret, image = cv2.threshold(image, ints, 255, cv2.THRESH_BINARY)
    txt = pytesseract.image_to_string(PIL.Image.fromarray(image, 'RGB'), config='-psm 4')
    return txt


def MoveandDragTo(movex, movey, dragx, dragy, velocity):
    pyautogui.moveTo(movex, movey, velocity)
    pyautogui.dragTo(dragx, dragy, velocity)


def LN():
    pyautogui.keyDown('shift')
    pyautogui.press('enter')
    pyautogui.keyUp('shift')
    

# █▀▀▄ ░▀░ █▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀▄
# █░░█ ▀█▀ ▀▀█ █░░ █░░█ █▄▄▀ █░░█
# ▀▀▀░ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀ ▀▀▀░



# █▀▀ █░░ █▀▀█ █▀▀▄
# █░░ █░░ █▄▄█ █░░█
# ▀▀▀ ▀▀▀ ▀░░▀ ▀░░▀
clan_prefix = ("lly")


class Command:
    #   rank
    #   info
    message0 = ""
    message1 = ""
    message2 = ""

    def message_send(self):
        #Opens chat window
        pyautogui.click(745, 615)
        pixelMatchesColor_wait(700, 675, (255, 255, 255))
        pyautogui.typewrite("ıllıllı " + str(self.message0) + " ıllıllı", interval=0.16)
        LN()
        pyautogui.typewrite(self.message1, interval=0.16)
        if self.message2 != "":
            LN()
            pyautogui.typewrite(self.message2, interval=0.16)
        #Closes chat window and screen
        pyautogui.click(780, 645)
        pixelMatchesColor_wait(777, 630, (119, 106, 97))
        pyautogui.click(765, 65)
        time.sleep(1.5)


default = Command()
commands = ['Recruit', 'Knight', 'Captain', 'Master', 'Grand',
            'Rules', 'Requirements', 'Discord', 'Sheet', 'Options']
message_commands = [[['New to the clan. Will they last?'],
                     ['Unknown amount in clan, Immeasurable total']],
                    [['Lasted more than a week in TTU'],
                     ['Unknown amount in clan, Unknown total']],
                    [['60+ CQ per week, trusted member'],
                     ['11 active in clan, Unknown total']],
                    [['Unobtainable, decided purely by SilicalNZ'],
                     ['NULL active in clan, Abaines700 & Nyuctophilia & SilicalNZ have held this role']],
                    [['Decided by previous or acting GrandMaster'],
                     ['SilicalNZ holds this role, hdotfi & Laku & BrainStormX have held this role']],
                    [['Speak English and be considerate with language usage '
                      '| Treat all members with respect | No spam | Attack CQ']],
                    [['More than 3 attacks per boss | Attack boss when it spawns '
                      '| Attend 3 of every 4 bosses']],
                    [['Hero you go: https://discord.gg/VRnmHG3']],
                    [['Are you at the top yet?: http://bit.ly/TTU_Sheet_167']]]


class Memory(object):
    pass
memory_ = Memory()


def message_read(tag, intensity):
    text = ocr((462, 155, 775, 593), intensity)
    if text.count(tag) >= 1:
        while text.count(tag) >= 1:
            text = text[text.find(tag) + len(tag) + 1:]
            for x in range(2):
                if hasattr(memory_, tag):
                    if getattr(memory_, tag) != text[0:2]:
                        setattr(memory_, tag, text[0:2])
                        return True
                else:
                    setattr(memory_, tag, "NULL")
    return False


def clan_message():
    #Check for and open game
    if pyautogui.pixelMatchesColor(508, 64, (237, 66, 7)):
        pyautogui.click(490, 50)
        pixelMatchesColor_wait(526, 65, (126, 113, 105))
        #For user messages
        if message_read(clan_prefix, 215):
            #Goes through list, and matches groups to commands
            for x in range(0, len(commands)):
                if getattr(memory_,clan_prefix).startswith(commands[x])[0:2]:
                    default.message0 = commands[x]
                    default.message1 = message_commands[x][0]
                    if message_commands[x][1]:
                        default.message2 = message_commands[x][1]
        elif message_read("Welcome", 100):
            default.message0 = "Welcome"
            default.message1 = 'I am Silly BOT and I manage this clan'
            default.message2 = ("For a list of commands, type \'Silly Options\'. "
                                "Otherwise just hit the boss and be cool!")
            
# █░░ █▀▀█ █▀▀▀ █▀▀▀ ░▀░ █▀▀▄ █▀▀▀
# █░░ █░░█ █░▀█ █░▀█ ▀█▀ █░░█ █░▀█
# ▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀ ▀░░▀ ▀▀▀▀
            
# █▀▀ █▀▀█ █▀▀█ █▀▄▀█ ░▀░ █▀▀▄ █▀▀▀
# █▀▀ █▄▄█ █▄▄▀ █░▀░█ ▀█▀ █░░█ █░▀█
# ▀░░ ▀░░▀ ▀░▀▀ ▀░░░▀ ▀▀▀ ▀░░▀ ▀▀▀▀


def clan_quest():
    # Checks if active
    if pyautogui.pixelMatchesColor(493, 49, (116, 66, 63)):
        pyautogui.click(493, 49)
        pixelMatchesColor_wait(526, 65, (126, 113, 105))
        pyautogui.click(510, 620)
        pixelMatchesColor_wait(560, 350, (58, 58, 76))
        pyautogui.click(680, 620)
        while True:
            #           Waits for boss to appear
            time.sleep(5)
            #           Repeats until boss died
            while not pyautogui.pixelMatchesColor(598, 77, (255, 255, 255)):
                pyautogui.click(Screen_Resolution[0] / 2, Screen_Resolution[1] / 2)
                time.sleep(0.05)
            print(ocr((510, 100, 720, 150), 130))  # Attacks & Damage
            pyautogui.click(Screen_Resolution[0] / 2, Screen_Resolution[1] / 2)
            pixelMatchesColor_wait(560, 350, (58, 58, 76))
            #           How many repeats are wanted
            if ocr((680, 603, 695, 614), 202) <= ClanQuest_DiamondCost:
                pyautogui.click(675, 630)
                pixelMatchesColor_wait('Re-attack window')
                pyautogui.click('Attack button')
            else:
                pyautogui.click(760, 65)
                pyautogui.click(760, 65)
                pixelMatchesColor_wait(Home_Screen)
                return


def egg_gift():
    if pyautogui.pixelMatchesColor(472, 247, (237, 66, 7)):
        pyautogui.click(450, 260)
        pixelMatchesColor_wait(461, 662, (30, 12, 7))
        while not pixelMatchesColor_wait(Home_Screen):
            pyautogui.click(Screen_Resolution[0] / 2, Screen_Resolution[1] / 2)


def daily_gift():
    if pyautogui.pixelMatchesColor(455, 173, (236, 181, 181)):
        pyautogui.click(455, 173)
        pixelMatchesColor_wait(568, 462, (40, 160, 203))
        pyautogui.click(568, 462)
        pixelMatchesColor_wait(575, 456, (40, 160, 203))
        while not pyautogui.pixelMatchesColor(571, 473, (23, 81, 101)):
            pyautogui.click(Screen_Resolution[0] / 2, Screen_Resolution[1] / 2)
        pyautogui.click(775, 215)
        time.sleep(3)


def mana_check():
    if pyautogui.pixelMatchesColor(595, 548, (255, 255, 255)):
        return True


def hero_levelup():
    pyautogui.click(525, 665)
    pixelMatchesColor_wait(720, 420, (83, 77, 75))
    #   Looks for a fully upgraded hero
    while (ocr((717, 620, 787, 633), 210)[0:3]) != "MAX":
        MoveandDragTo(675, 640, 675, 571, 2)
        time.sleep(1)
    # Looks for the top of the window
    while (ocr((728, 498, 772, 510), 210)[0:3]) != "Asc":
        for x in range(0, 4):
            pyautogui.click(755, 625 - 60 * x)
            time.sleep(0.5)
        MoveandDragTo(675, 430, 675, 682, 2)
        time.sleep(1)
    pyautogui.click(770, 400)


def achievement_gift():
    if pyautogui.pixelMatchesColor(612, 435, (242, 116, 77)):
        pyautogui.click(595, 440)
        pixelMatchesColor_wait(726, 65, (120, 108, 98))
        pyautogui.click(730, 182)
        pyautogui.click(765, 65)
        pixelMatchesColor_wait(720, 420, (83, 77, 75))
        print("Attempted achievement_gift")


def swordmaster_levelup():
    pyautogui.click(460, 665)
    pixelMatchesColor_wait(720, 420, (83, 77, 75))
    pyautogui.click(755, 500)
    achievement_gift()
    pyautogui.click(770, 400)
    time.sleep(1)


def idle_disable():
    if pyautogui.pixelMatchesColor(808, 67, (184, 69, 10)):
        pyautogui.click(776, 60)
        time.sleep(0.25)


def ability_activate():
    for x in range(0, 5):
        pyautogui.click(525 + 60 * x, 610)
        time.sleep(0.5)
    pyautogui.click(Screen_Resolution[0] / 2, Screen_Resolution[1] / 2, 35)


def character_name():
    pyautogui.click(460, 665)
    pixelMatchesColor_wait(720, 420, (83, 77, 75))
    pyautogui.click(500, 500)
    pixelMatchesColor_wait(715, 150, (121, 108, 99))
    pyautogui.click(650, 220)
    pixelMatchesColor_wait(666, 324, (250, 129, 11))
    pyautogui.click(650, 256)
    pixelMatchesColor_wait(628, 623, (255, 255, 255))
    pyautogui.typewrite("Silly Bot", interval=0.15)
    pyautogui.click(780, 645)
    pyautogui.click(666, 324)
    time.sleep(1)
    pyautogui.click(775, 150)
    time.sleep(1)
    pyautogui.click(775, 400)
    
    
def prestige():
    if not pyautogui.pixelMatchesColor():
        pyautogui.click(460, 665)
        pixelMatchesColor_wait(720, 420, (83, 77, 75))
    else:
      



# █▀▀ █▀▀ █▀▀█ ░▀░ █▀▀█ ▀▀█▀▀
# ▀▀█ █░░ █▄▄▀ ▀█▀ █░░█ ░░█░░
# ▀▀▀ ▀▀▀ ▀░▀▀ ▀▀▀ █▀▀▀ ░░▀░░
Loop_Counter = 0
# character_name()
ability_timer = 1000
while True:
    clan_quest()
    egg_gift()
    daily_gift()
    if mana_check() and ability_timer >= (120 + 45 + 5):
        # hero_levelup()
        # swordmaster_levelup()
        idle_disable()
        ability_activate()
        Loop_Counter += 1
        print(">^<" + str(Loop_Counter) + "repeats")
        print("Waiting for ability timer")
        ability_timer = time.time()
    clan_message()
    time.sleep(random.randrange(2, 15))

