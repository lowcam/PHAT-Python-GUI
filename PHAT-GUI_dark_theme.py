#-------------------------------------------------------------------------------
# PHAT  - Password Hashing Algorithm Tool Dark Theme
# GUI Python Version
# v 1.0
#
# The purpose of this tool is to let an individual enter text and have a hashed
# output to use as the password to the site or program. Initially the program
# will hash the input in SHA 256 and output in hexadecimal. THe plans for this
# program are to allow the selection of three different SHA lengths (256, 384,
# and 512). Also, the output numbering system will be selectable between
# hexadecimal, base64, and base58. Also, the number of digits in the ouput
# will be selectable in case a site can only have a certain number of digits
# in a password. THe last step will be for the output to be copied to the
# clipboard so if can be pasted into the program or site.
#
# Required to use:
# Python3
# Python3-tk
# Use pip3 to install base58
# Use pip3 to install appJar
#
# Icon made by Freepik from www.flaticon.com
#
#
# (C) 2020 Lorne Cammack, USA
# email lowcam.socailvideo@gmail.com
# Released under GNU Public License (GPL) v3
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

from appJar import gui
import codecs
import hashlib
import base58
from tkinter import Tk

# create a GUI variable called app
app = gui("PHAT v1.0", "500x500")
app.setBg("black")
app.setFg("#c6c6c6")
app.setFont(10)
app.showSplash("PHAT (Password Hashing Algorithm Tool)", fill='black', stripe='black', fg='white', font=44)

def press(button):
    if button == "Exit":
        app.stop()
    elif button == "About":
        app.infoBox("About PHAT", "PHAT (Password Hashing Algorithm Tool) Copyright (C) 2020 Lorne Cammack. This program comes with ABSOLUTELY NO WARRANTY; This is free software, and you are welcome to redistribute it under certain conditions. See https://www.gnu.org/licenses/ for more details.", parent=None)
    elif button == "Copy Result":
        copytext = app.getTextArea("calcResultMessage")
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(copytext)
        r.update()
        r.destroy()
    else:
        inputText = app.getEntry("TextString")
        shavalue = app.getOptionBox("SHA")
        valuesha = int(shavalue)
        numsystext = app.getOptionBox("NumberSystem")
        numsysvalue = 1
        if numsystext == "Base64":
            numsysvalue = 2
        elif numsystext == "Base58":
            numsysvalue = 3
        else:
            numsysvalue = 1
        valuenumsys = int(numsysvalue)
        finaldig = 0
        digfinalyn = app.getRadioButton("restrictDigitsYN")
        if digfinalyn == "No":
            finaldig = 0
        else:
            digfinal = app.getScale("restrictDigitScale")
            finaldig = int(digfinal)
        hashText = bytes(inputText, "ascii")
        outputText = 0
        if valuesha == 256:
            outputText = hashlib.sha256 (hashText).hexdigest()
        elif valuesha == 384:
            outputText = hashlib.sha384 (hashText).hexdigest()
        else:
            outputText = hashlib.sha512 (hashText).hexdigest()
        outputPrint = 0
        if numsysvalue == 1:
            outputPrint = outputText
        elif numsysvalue == 2:
            outputPrint = codecs.encode(codecs.decode(outputText, 'hex'), 'base64').decode()
            printreturnLen = len(outputPrint)
            if printreturnLen > 76:
                printreturnSide1 = outputPrint[:76]
                printreturnEndCalc = printreturnLen - 77
                printreturnSide2 = outputPrint[-printreturnEndCalc:]
                outputPrint = printreturnSide1 + printreturnSide2
        else:
            outputPrint = base58.b58encode(codecs.decode(outputText, 'hex'))
        lenhash = len(outputText)
        if finaldig == 0 or finaldig >=lenhash:
            app.clearTextArea("calcResultMessage")
            app.setTextArea("calcResultMessage", outputPrint)
        else:
            OutputPrintConcat = outputPrint[:finaldig]
            app.clearTextArea("calcResultMessage")
            app.setTextArea("calcResultMessage", OutputPrintConcat)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "PHAT v1.0")
app.setLabelBg("title", "green")
app.addLabelEntry("TextString")
app.setEntryBg("TextString","#202020")
app.setEntryFg("TextString","#c6c6c6")
app.addLabelOptionBox("SHA", ["256", "384", "512"])
app.addLabelOptionBox("NumberSystem", ["Hex", "Base64", "Base58"])
app.addLabel("restrictDigits", "Restrict the Number of Output Digits?")
app.addRadioButton("restrictDigitsYN", "Yes")
app.addRadioButton("restrictDigitsYN", "No")
app.setRadioButton("restrictDigitsYN", "No", callFunction=False)
app.setRadioButtonBg("restrictDigitsYN","#202020")
app.setRadioButtonFg("restrictDigitsYN","#787878")
app.addLabel("restrictDigitScaleText", "Number of Output Digits")
app.addScale("restrictDigitScale")
app.setScaleRange("restrictDigitScale", 1, 128, curr=128)
app.setScaleFg("restrictDigitScale", "#c6c6c6")
app.setScaleBg("restrictDigitScale", "#202020")
app.showScaleValue("restrictDigitScale", show=True)
app.addLabel("calcResult", "Calc Result")
app.addTextArea("calcResultMessage")
app.setTextArea("calcResultMessage", "Push the Calc Button to See the Result")
app.setTextAreaBg("calcResultMessage","#202020")
app.setTextAreaFg("calcResultMessage","#c6c6c6")
app.addButtons(["Calculate", "Copy Result", "About", "Exit"], press)
app.setFocus("TextString")


# start the GUI
app.go()
