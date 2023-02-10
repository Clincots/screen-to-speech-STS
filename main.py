from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
import cv2
import pynput
import pyperclip
from PIL import ImageGrab
import pytesseract
import pyttsx3
import subprocess





# path for pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# vars
scanning = True
keykey = "'`'"
change = False
tcopy = ""


# does the preprocessing
def preprocess(im):
    # grayscale
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # binarize
    im = cv2.GaussianBlur(im, (5, 5), 1)
    im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2)

    return im


# takes a screenshot
def on_press(key):
    global scanning
    global change
    global keykey
    #print(str(key))

    if str(key) == keykey:
        subprocess.call([r'C:\\Windows\System32\SnippingTool.exe', '/clip'])

        screenshot = ImageGrab.grabclipboard()
        screenshot.save('temp/screenshot.png', 'Png')
        read()

    if change: # for changing the key
        keykey = str(key)
        change = False


# reads the screenshot
def read():
    global tcopy
    # opens the screenshot
    image_file = 'temp/screenshot.png'
    im = cv2.imread(image_file)

    # preprocesses it, does ocr, and speaks it
    preprocess(im)
    text = pytesseract.image_to_string(im)

    # removes tabs
    text = text.splitlines()
    text = " ".join(text)
    #print(text)
    tcopy = text
    say(text)


engine = pyttsx3.init()  # object creation


# speaking
def say(text):
    engine.say(text)
    engine.runAndWait()
    engine.stop()


# sets the speed
def setSpeed(speed):
    speed = 100 + int(speed)*2
    engine.setProperty('rate', speed)


# volume (between 1 and 0)
engine.setProperty('volume',1.0)


# sets the volume
def setSound(volume):
    volume = int(volume)/100
    engine.setProperty('volume', volume)


# voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 for female, 0 for male


# keyboard listener
listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()


# GUI #------------------------------------------------------------------------------------
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
whar = False
whar2 = False
trueornot = False

class FloatLayout(FloatLayout):

    def update(self):
        global volume
        global speed
        global keykey
        volume = self.ids.volume_label.text
        speed = self.ids.speed_label.text

        #print("volume:" + volume)
        #print("speed:" + speed)
        #set volume and speed to volume and speed of actual tts

        setSpeed(speed)
        setSound(volume)
        #print(keykey)


    def copy(self):
        global tcopy
        #print("you pressed copy wow amazing ")
        pyperclip.copy(tcopy)


    def L_plus_radio(self): #right
        global ineedthis
        global ineedthis2
        global whar
        global whar2
        ineedthis = False
        if whar:
            ineedthis = False
            ineedthis2 = False
            whar = False
            #print("Voice 1 and 2 are not on!")
            return

        if not ineedthis:
            ineedthis = True
            ineedthis2 = False
            whar = True
            whar2 = False
            #print("Voice 2 is off, and voice 1 is on!")
            engine.setProperty('voice', voices[1].id)


    def L_plus_radio2(self): #left
        global ineedthis
        global ineedthis2
        global whar2
        global whar
        ineedthis2 = False

        if whar2:
            ineedthis = False
            ineedthis2 = False
            whar2 = False
            #print("Voice 1 and 2 are not on!")
            return

        if not ineedthis2:
            ineedthis2 = True
            ineedthis = False
            whar2 = True
            whar = False
            #print("Voice 1 is off, and voice 2 is on!")
            engine.setProperty('voice', voices[0].id)

    def changeKey(self):
        #print("pressed")
        global change
        change = True



class CustomButtonApp(App):
    def build(self):
        return FloatLayout()


if __name__ == '__main__':
    CustomButtonApp().run()
#-----------------------------------------------------------------------------------
