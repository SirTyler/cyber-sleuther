import math
import os
import shutil
import urllib.request
import zipfile

from PyQt5 import QtCore

class DSCSToolsUpdater(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    log = QtCore.pyqtSignal(str)
    lock = QtCore.pyqtSignal()
    unlock = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tag = None

    def run(self):
        try:
            self.lock.emit()
            path = "lib/DSCSTools/DSCSTools.zip"
            url, tag = get_dscstools_download_url()
            _exists = True
            if(os.path.exists("lib/DSCSTools.version")):
                with open("lib/DSCSTools.version", 'r') as file_t:
                    data = file_t.read()
                    if(data == tag):
                        _exists = False
            if(_exists):
                os.makedirs("lib/DSCSTools", exist_ok=True)
                with urllib.request.urlopen(url) as req, open(path, 'ab') as f:
                    chunk_size = 1024 * 256
                    total_size = int(req.info()['Content-Length'])

                    total_read = 0
                    num_packets = int(math.ceil(total_size / chunk_size))
                    packet_number = 1
                    chunk = None
                    while chunk != b'':
                        chunk = req.read(chunk_size)
                        f.write(chunk)
                        progress = math.ceil(20 * packet_number / num_packets)
                        filled = '-'*(progress-1)
                        empty = '  '*(20-progress)
                        self.log.emit(f"Downloading DSCSTools... [{filled}|{empty}]")
                        total_read += len(chunk)
                        packet_number += 1
                with zipfile.ZipFile(path, 'r') as f:
                        f.extractall("lib/DSCSTools")
                with open("lib/DSCSTools.version", 'w') as file_t:
                    file_t.write(tag)
                    file_t.close()
                os.remove("lib/DSDSTools/DSCSTools.zip")
                #if(os.path.exists("lib/DSCSTools.pyd")):
                #    os.remove("lib/DSCSTools.pyd")
                #os.rename("lib/DSCSTools/DSCSTools.dll","lib/DSCSTools.pyd")
                #shutil.rmtree("lib/DSCSTools/")
                self.log.emit("Updated DSCSTools")
            else:
                self.log.emit("DSCSTools is up to date")
        except Exception as e:
            self.log.emit(f"Error: {e}")
            raise e
        finally:
            self.unlock.emit()
            self.finished.emit()

def get_dscstools_tag():
    dscstools_url = r"https://github.com/SydMontague/DSCSTools/releases/latest"
    if dscstools_url[:19] != r"https://github.com/":
        raise ValueError("Download URL is not on GitHub.")
    url = urllib.request.urlopen(dscstools_url).geturl()
    return url.split('/')[-1]

def get_dscstools_download_url():
    tag = get_dscstools_tag()
    tag2 = tag.replace("v","")
    return rf"https://github.com/SydMontague/DSCSTools/releases/download/{tag}/DSCSTools_{tag2}_win64-shared.zip", tag
