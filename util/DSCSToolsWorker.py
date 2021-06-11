import subprocess

class DSCSToolsWorker:
    def __init__(self):
        self.dscstools_location = "lib/DSCSTools/DSCSToolsCLI.exe"
        self.dscstools_folder = "lib/DSCSTools/"

    def decrypt_save(self, origin, destination):
        subprocess.call([self.dscstools_location, f'--savedecrypt', origin, destination],
                        creationflags=subprocess.CREATE_NO_WINDOW, cwd=self.dscstools_folder)
