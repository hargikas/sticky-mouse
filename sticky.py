import threading

import keyboard
import pyautogui


class StickyClick(object):
    def __init__(self):
        self._esc_toggle = False
        self._position = (0, 0)
        self._default_pause = pyautogui.PAUSE
        self._child_thread = threading.Thread(target=self._clicking)

    def _clicking(self):
        i = 0
        while self._esc_toggle:
            pyautogui.click(x=self._position[0], y=self._position[1])
            i += 1
        print("Clicked %d times" % (i))

    def esc_pressed(self):
        self._position = pyautogui.position()
        self._esc_toggle = not self._esc_toggle
        if self._esc_toggle:
            print("Starting sticky clicking on position:", self._position)
            print("Press ESC to stop clicking.")
            self._child_thread.start()
        else:
            self._child_thread.join()
            print("Reseting...")
            self._child_thread = threading.Thread(target=self._clicking)
            print("Press CTRL+ALT to exit.")
            print("Press ESC to start again.")

    def change_speed(self, change):
        clicks_per_sec = 1.0 / pyautogui.PAUSE

        if (clicks_per_sec < 1.0) or ((clicks_per_sec == 1.0) and (change < 0)):
            tmp = pyautogui.PAUSE - change
            clicks_per_sec = 1.0 / tmp
        else:
            clicks_per_sec += change

        if clicks_per_sec > 0:
            tmp = 1.0 / clicks_per_sec
            if change == 0 or tmp <= 0:
                tmp = self._default_pause
            pyautogui.PAUSE = tmp

        clicks_per_sec = 1.0 / pyautogui.PAUSE
        print("Current clicks per second:", clicks_per_sec)

    def start(self):
        # The main hot_key
        keyboard.add_hotkey('esc', self.esc_pressed)
        # Hotkeys for changing speed
        keyboard.add_hotkey('right', self.change_speed, args=(-1,))
        keyboard.add_hotkey('left', self.change_speed, args=(1,))
        keyboard.add_hotkey('up', self.change_speed, args=(0,))
        keyboard.add_hotkey('down', self.change_speed, args=(0,))
        print("Stick Click is ready.")
        print("Press CTRL+ALT to exit.")
        print("Press ESC to start/stop clicking.")
        # Exit Hotkey
        keyboard.wait('ctrl+alt')


def main():
    obj = StickyClick()
    obj.start()


if __name__ == '__main__':
    main()
