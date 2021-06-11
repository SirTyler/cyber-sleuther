import os
from os import path
import sys
import fnmatch
import struct
import random
import subprocess

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from util.DSCSToolsUpdater import DSCSToolsUpdater
from util.DSCSToolsWorker import DSCSToolsWorker
from util.Data import Digimon

party = []
bank = []

def build_digimon(digimon: bytearray, mode = 0):
    #id name
    #hp max_hp sp max_sp
    #atk def int spd abi cam
    #skills
    #known skills [1-10]
    #known skills [11-20]
    #slots equipment accessory
    switcher={
    0: '? 15x i 12x 20s 78x 6x' + \
            'i i 4x i i xx' + \
            'h xx h xx h xx h xx h h 6x' + \
            'i 4x i 4x i 4x i 4x i 4x i 4x' + \
            'i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x' + \
            'i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x' + \
            '160x h h h h xx h 12x',
    1: '12x ? 15x i 12x 20s 78x 6x' + \
            'i i 4x i i xx' + \
            'h xx h xx h xx h xx h h 6x' + \
            'i 4x i 4x i 4x i 4x i 4x i 4x' + \
            'i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x' + \
            'i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x i 4x' + \
            '160x h h h h xx h'
    }
    pack = switcher.get(mode)
    digimon = struct.unpack(pack, digimon)
    ACTIVE = digimon[0]
    ID = digimon[1]
    NAME = bytearray()
    for i in digimon[2]:
        if(i == 0x00): break
        else:
            NAME.append(i)
    NAME = NAME.decode()
    HP = [digimon[3],digimon[4]*10]
    SP = [digimon[5],digimon[6]]
    ATK = digimon[7]
    DEF = digimon[8]
    INT = digimon[9]
    SPD = digimon[10]
    ABI = digimon[11]
    CAM = digimon[12]
    skills = [digimon[13],digimon[14],digimon[15],digimon[16],digimon[17],digimon[18]]
    known = [digimon[19],digimon[20],digimon[21],digimon[22],digimon[23],digimon[24],digimon[25],digimon[26],digimon[27],digimon[28],
            digimon[29],digimon[30],digimon[31],digimon[32],digimon[33],digimon[34],digimon[35],digimon[36],digimon[37],digimon[38],]
    slots = digimon[39]
    equipment = [digimon[40],digimon[41],digimon[42]]
    return Digimon(ID, NAME, HP, SP, ATK, DEF, INT, SPD, ABI, CAM, skills, known, slots, equipment)

def read_bank(file):
    with open(file, 'rb') as file_t:
        digimon = bytearray()
        blob_data = bytearray(file_t.read())
        start_line = 0x0000B650 # Start of Bank
        end_line = 0x00035940   # End of Bank
        current_line = start_line
        current_offset = 0x00
        line_count:int = 0
        max_lines:int = 35
        while(current_line < end_line):
            if(current_offset == 0x00 and line_count == 0):
                if(not bool(blob_data[current_line+current_offset])):
                    break
            if(current_offset > 0x0F):
                line_count += 1
                current_line += 0x00000010
                current_offset = 0x00
                if(line_count > max_lines):
                    line_count = 0
                    bank.append(build_digimon(digimon))
                    digimon.clear()
            else:
                digimon.append(blob_data[current_line+current_offset])
                current_offset += 0x01

def read_party(file):
    with open(file, 'rb') as file_t:
        digimon = bytearray()
        blob_data = bytearray(file_t.read())
        start_line = 0x0003CA90 # Start of Party
        end_line = 0x0004B980  # End of Party
        current_line = start_line
        current_offset = 0x00
        line_count:int = 0
        max_lines:int = 35
        while(current_line < end_line):
            if(current_offset == 0x0C and line_count == 0):
                if(not bool(blob_data[current_line+current_offset])):
                    break
            if(current_offset > 0x0F):
                line_count += 1
                current_line += 0x00000010
                current_offset = 0x00
                if(line_count > max_lines):
                    line_count = 0
                    current_offset = 0x00
                    party.append(build_digimon(digimon, 1))
                    digimon.clear()
            else:
                digimon.append(blob_data[current_line+current_offset])
                current_offset += 0x01

def write_output(file):
    with open(file, 'w', encoding='Latin1') as file_t:
        file_t.write("PARTY\n")
        for mon in party:
            lines = ["","","","",""]
            lines[0] = "#{}\t{}\t\t{}\t{}\n".format(mon.ID, mon.NAME, mon.HP, mon.SP)
            lines[1] = "\t{}|{}|{}|{}\t{}|{}\n".format(mon.ATK, mon.DEF, mon.INT, mon.SPD, mon.ABI, mon.CAM)
            lines[2] = "\t{}\n".format(mon.skills)
            #lines[3] = "\t{}\n".format(mon.known_skills)
            lines[4] = "\t{} {}\n".format(mon.equipment_slots, mon.equipment)
            file_t.writelines(lines)
        file_t.write("BANK\n")
        for mon in bank:
            lines = ["","","","",""]
            lines[0] = "#{}\t{}\t\t{}\t{}\n".format(mon.ID, mon.NAME, mon.HP, mon.SP)
            lines[1] = "\t{}|{}|{}|{}\t{}|{}\n".format(mon.ATK, mon.DEF, mon.INT, mon.SPD, mon.ABI, mon.CAM)
            lines[2] = "\t{}\n".format(mon.skills)
            #lines[3] = "\t{}\n".format(mon.known_skills)
            lines[4] = "\t{} {}\n".format(mon.equipment_slots, mon.equipment)
            file_t.writelines(lines)
    file_t.close()

class MainWindow(QtWidgets.QMainWindow):
    def updateIcon(self):
        icon = QIcon()
        icon.addPixmap(self.iconMovie.currentPixmap())
        self.setWindowIcon(icon)

    def __init__(self, parent=None):
        super().__init__(parent)

        i = random.randint(1,3)
        m_gif = QMovie(f"logo/logo{i}.gif")
        self.iconMovie = m_gif
        self.iconMovie.start()
        self.iconMovie.frameChanged.connect(self.updateIcon)

        self.dscstools_worker = DSCSToolsWorker()
        self.update_dscs()
        self.loading_ui()

    def loading_ui(self):
        self.window = QWidget()
        self.setWindowTitle("Cyber Sleuther")
        self.setCentralWidget(self.window)
        self.resize(650, 650)

        layout = QVBoxLayout()
        self._label = QLabel("Checking for Update")
        layout.addWidget(self._label)
        self.window.setLayout(layout)
        self.show()

    def init_ui(self):
        self.window = QtWidgets.QWidget()
        self.setWindowTitle("Cyber Sleuther")
        self.setCentralWidget(self.window)
        self.resize(1260, 650)

        grid = QGridLayout()
        grid.setSpacing(10)

        _l = QLabel("Folder:")
        self.label = QLabel("Test")
        grid.addWidget(_l, 0, 0, 1, 1)
        grid.addWidget(self.label, 0, 1, 1, 5)

        self.button = QPushButton('Select Folder')
        grid.addWidget(self.button, 0, 6, 1, 9)
        self.button.clicked.connect(self.on_click)
        self.dialog = QFileDialog(self)
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        self.dialog.setFileMode(QFileDialog.Directory)
        self.dialog.setOptions(options)
        self.dialog.setDirectory(path.expandvars(r"%LOCALAPPDATA%\BANDAI NAMCO Entertainment\Digimon Story Cyber Sleuth Complete Edition\Saved\SaveGames"))

        self.save_box = QVBoxLayout()
        self.party_box = QGridLayout()
        self.bank_box = QGridLayout()
        grid.addLayout(self.save_box, 1, 0)
        grid.addLayout(self.party_box, 1, 1)
        grid.addLayout(self.bank_box, 2, 1)
        self.window.setLayout(grid)
        self.show()

    def update_dscs(self):
        self.thread = QtCore.QThread()
        self.worker = DSCSToolsUpdater()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.init_ui)
        self.worker.log.connect(self.log)
        self.worker.lock.connect(self.lock)
        self.worker.unlock.connect(self.unlock)
        self.thread.start()

    def log(self, message):
        self._label.setText(message)
    def lock(self):
        pass
    def unlock(self):
        pass
    def display(self):
        while self.party_box.count():
            child = self.party_box.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        while self.bank_box.count():
            child = self.bank_box.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        x = 0
        y = 0
        for i in range(len(party)):
            d = party[i]
            id = d.ID + 1000
            disp = QWidget()
            disp.setLayout(QVBoxLayout())

            top = QHBoxLayout()
            disp.layout().addLayout(top)
            label_id = QLabel(f"#{d.ID}")
            top.addWidget(label_id)
            #label_level = QLabel(f"Lv.{d.LEVEL}")
            #top.addWidget(label_level)
            label_name = QLabel(d.NAME)
            top.addWidget(label_name)

            mid = QHBoxLayout()
            disp.layout().addLayout(mid)
            disp.setGeometry(0,0,128,128)
            label_img = QLabel(disp)
            img = QPixmap(f"res/_chara/ui_chara_icon_{id}.png")
            img = img.scaled(128, 128, Qt.KeepAspectRatio, Qt.FastTransformation)
            label_img.setPixmap(img)
            mid.addWidget(label_img)

            bot = QVBoxLayout()
            disp.layout().addLayout(bot)
            hpsp = QGridLayout()
            label_hp = QLabel(f"HP{d.HP}")
            bar_hp = QProgressBar()
            bar_hp.setGeometry(0,0,64,25)
            bar_hp.setMaximum(d.HP[1])
            bar_hp.setValue(d.HP[0])
            bar_hp.setTextVisible(False)
            label_sp = QLabel(f"SP{d.SP}")
            bar_sp = QProgressBar()
            bar_sp.setGeometry(0,0,64,25)
            bar_sp.setMaximum(d.SP[1])
            bar_sp.setValue(d.SP[0])
            bar_sp.setTextVisible(False)
            hpsp.addWidget(bar_hp, 0, 0)
            hpsp.addWidget(bar_sp, 1, 0)
            hpsp.addWidget(label_hp, 0, 0)
            hpsp.addWidget(label_sp, 1, 0)
            bot.addLayout(hpsp)
            stats = QGridLayout()
            label_atk = QLabel(f"ATK:{d.ATK}")
            stats.addWidget(label_atk, 0,0)
            label_def = QLabel(f"DEF:{d.DEF}")
            stats.addWidget(label_def, 0,1)
            label_int = QLabel(f"INT:{d.INT}")
            stats.addWidget(label_int, 0,2)
            label_spd = QLabel(f"SPD:{d.SPD}")
            stats.addWidget(label_spd, 1,0)
            label_abi = QLabel(f"ABI:{d.ABI}")
            stats.addWidget(label_abi, 1,1)
            label_cam = QLabel(f"CAM:{d.CAM}")
            stats.addWidget(label_cam, 1,2)
            bot.addLayout(stats)

            self.party_box.addWidget(disp, x, y)
            if(y > 3):
                y = 0
                x += 1
            else:
                y += 1
        x = 0
        y = 0
        for i in range(len(bank)):
            d = bank[i]
            id = d.ID + 1000
            label = QLabel()
            img = QPixmap(f"res/_chara/ui_chara_icon_{id}.png")
            img = img.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)
            label.setPixmap(img)
            self.bank_box.addWidget(label, x, y)
            if(y > 6):
                y = 0
                x += 1
            else:
                y += 1

    def read_file(self, file):
        _file = os.path.join(*os.path.split(file)[:-1])
        self.dscstools_worker.decrypt_save(file, _file+"_decrypt.bin")
        party.clear()
        read_party(_file+"_decrypt.bin")
        bank.clear()
        read_bank(_file+"_decrypt.bin")
        os.remove(_file+"_decrypt.bin")

    def load_save_0(self, folder):
        self.read_file(os.path.abspath(folder)+os.path.sep+"0000.bin")
        self.display()
    def load_save_1(self, folder):
        self.read_file(os.path.abspath(folder)+os.path.sep+"0001.bin")
        self.display()
    def load_save_2(self, folder):
        self.read_file(os.path.abspath(folder)+os.path.sep+"0002.bin")
        self.display()

    def get_saves(self, folder):
        files = fnmatch.filter(os.listdir(folder), "[0-9]*.bin")
        while self.save_box.count():
            child = self.save_box.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        save_count = 0
        for f in files:
            button = QPushButton(f)
            if(save_count == 0):
                button.clicked.connect(lambda: self.load_save_0(folder))
            elif(save_count == 1):
                button.clicked.connect(lambda: self.load_save_1(folder))
            elif(save_count == 1):
                button.clicked.connect(lambda: self.load_save_2(folder))
            save_count += 1
            self.save_box.addWidget(button)

    @pyqtSlot()
    def on_click(self):
        if self.dialog.exec_():
            folder = self.dialog.directory()
            self.label.setText(folder.absolutePath())
            self.get_saves(folder.absolutePath())

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
