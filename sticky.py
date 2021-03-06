"""A script that simulates multiple clicking in the position of the mouse"""
import threading

import keyboard
import pyautogui


class StickyClick(object):
    """The base class that simulated the clicking in a separate thread"""
    def __init__(self, register_position):
        self._esc_toggle = False
        self._position = (0, 0)
        self._default_pause = pyautogui.PAUSE
        self._child_thread = threading.Thread(target=self._clicking)
        self._save_position = register_position

    def _clicking(self):
        i = 0
        while self._esc_toggle:
            if self._save_position:
                pyautogui.click(x=self._position[0], y=self._position[1])
            else:
                pyautogui.click()
            i += 1
        print("Clicked %d times" % (i))

    def toggle_clicking(self):
        """Toggles On/Off the automatic clicking"""
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
        """Changes the speed of the clicking"""
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
        """Register hotkeys and waits for exit"""
        # The main hot_key
        keyboard.add_hotkey('esc', self.toggle_clicking)
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
    """The main function"""
    obj = StickyClick(True)
    obj.start()


if __name__ == '__main__':
    main()
