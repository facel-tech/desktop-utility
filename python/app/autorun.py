import os
from os.path import expanduser
from sys import platform

CONTENTS = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>tech.facel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Applications/Facel.app/Contents/MacOS/Facel</string>
    </array>
    <key>ProcessType</key>
    <string>Interactive</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
"""

PATH_LA = expanduser("~/Library/LaunchAgents")
PATH = "{}/Facel.plist".format(PATH_LA)

LINUX_CONTENT = """
[Desktop Entry]
Encoding=UTF-8
Name=Facel
Comment=Facel
Icon=gnome-info
Exec=~/Applications/Facel
Terminal=false
Type=Application
Categories=

X-GNOME-Autostart-enabled=true
X-GNOME-Autostart-Delay=0
"""

LINUX_PATH = expanduser("~/.config/autostart/Facel.desktop")


def create_mac_file():
    if not os.path.isdir(PATH_LA):
        os.makedirs(PATH_LA)

    if not os.path.isfile(PATH):
        with open(PATH, "w+") as f:
            f.write(CONTENTS)
            f.close()


def create_linux_file():
    if not os.path.exists(LINUX_PATH):
        with open(LINUX_PATH, "w+") as f:
            f.write(LINUX_CONTENT)
            f.close()


def set_autostart_registry(app_name, key_data=None, autostart: bool = True) -> bool:
    import winreg

    with winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=r'Software\Microsoft\Windows\CurrentVersion\Run',
            reserved=0,
            access=winreg.KEY_ALL_ACCESS,
    ) as key:
        try:
            if autostart:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, key_data)
            else:
                winreg.DeleteValue(key, app_name)
        except OSError:
            return False

    return True


def check_autostart_registry(value_name):
    import winreg

    with winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=r'Software\Microsoft\Windows\CurrentVersion\Run',
            reserved=0,
            access=winreg.KEY_ALL_ACCESS,
    ) as key:
        idx = 0
        while idx < 1_000:  # Max 1.000 values
            try:
                key_name, _, _ = winreg.EnumValue(key, idx)
                if key_name == value_name:
                    return True
                idx += 1
            except OSError:
                break
    return False


def add_to_autostart():
    if platform == "darwin":
        create_mac_file()

    elif platform == "win32":
        set_autostart_registry("Facel")

    else:
        create_linux_file()
