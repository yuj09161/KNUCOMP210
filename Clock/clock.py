from datetime import datetime
import os
import time

from pyfiglet import Figlet


if __name__ == "__main__":
    figlet = Figlet(font='big')
    os.system("cls")

    try:
        while True:
            print(figlet.renderText(
                datetime.today().strftime('%I : %M : %S %p')
            ))
            time.sleep(1)
            os.system("cls")
    except KeyboardInterrupt as e:
        print(f"CTRL-C로 중단 되었습니다. {e}")
