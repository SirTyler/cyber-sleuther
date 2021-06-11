# Cyber Sleuther
A save viewer for Digimon Story: Cyber Sleuth.
Currently in a alpha stage with more features planned. Should be cross-platform compatible but I've only tested Windows, other operating systems may experience unintended bugs.

## Features
- Graphical display of all Digimon both in Party and in Bank based on the current save file.
- Ability to switch between different save files for viewing.

## Planned Features
- Automatic reloading of currently selected save file if the file is changed (new save from in game).
- Improvements in reading save file information, specifically missing Digimon information.
- Generate an image of current party and bank for use in easily sharing information.
- Generate an image of singular Digimon for use in easily sharing information.
- Display current progress in story (chapters) and current player location.
- Overall Improved GUI

## Installation
1. Install [Python 3.8.X](https://www.python.org/downloads/) or newer.
2. Open a Command Prompt and type 'pip install PyQt5' to install the dependency of PyQt5.
3. Download the Cyber Sleuther source code and unzip it. Create a text file in the downloaded folder and type 'python CyberSleuther.py' into the file. If you are on Windows, rename this file so that it has a '.bat' extension.
4. You can run Cyber Sleuther by running the '.bat' file. You can also create a shortcut to this '.bat' file and run that instead.

## Usage
On launch of the program, it may delay as it checks for an updated copy of [DSCSTools](https://github.com/SydMontague/DSCSTools). If none is found, or there is an update the program will automatically begin downloading this.
Afterwards, the program will open the ability to select your save folder, it defaults to "%LOCALAPPDATA%\BANDAI NAMCO Entertainment\Digimon Story Cyber Sleuth Complete Edition\Saved\SaveGames but if for whatever reason this is not your save location please feel free to choose another one.
It will then list out all save files found, select the one you would like to view and it will automatically decrypt and load the save information, no information is ever written to your existing save, but feel free to back up your saves before use if you feel so inclined.

## Acknoledgements
1. [SydMontague](https://github.com/SydMontague) for creating [DSCSTools](https://github.com/SydMontague/DSCSTools) and producing the Python API for it.
2. [SydMontague](https://github.com/SydMontague), [Pherakki](https://github.com/Pherakki), [Green Mii](https://gbatemp.net/members/green-mii.364451/), and [AnalogMan151](https://github.com/AnalogMan151) whose information and code I studied and reused for this project.
3. [AngelofHope](https://withthewill.net/members/angelofhope.1510/) for a [collection](https://withthewill.net/threads/digimon-sprite-animation-thread-read-first-post-fully-working.10472/) of great Digimon Animated Sprites used as icons in this project
