import pyautogui as pg
import time
import pyperclip
import ctypes
import keyboard as kbd


def main():
    kbd.add_hotkey('ctrl+q', do_swap)

    while True:
        time.sleep(1000000)


def do_swap():
    time.sleep(0.2)

    enable_num_at_end = False
    print('Num Lock:', get_numlock_state())
    if get_numlock_state():
        pg.press('numlock')
        enable_num_at_end = True

    print('Swapping...')
    current_lang = get_keyboard_language()
    print(current_lang)
    pg.hotkey('alt', 'shift')
    next_lang = get_keyboard_language()
    print(next_lang)
    pg.keyDown('shiftleft')
    pg.keyDown('shiftright')
    pg.hotkey('home')
    pg.keyUp('shiftleft')
    pg.keyUp('shiftright')
    pg.hotkey('ctrl', 'c')
    clip = pyperclip.paste()

    swapped_text = swap_chars(clip, current_lang, next_lang)
    pyperclip.copy(swapped_text)
    pg.hotkey('ctrl', 'v')

    if enable_num_at_end:
        pg.press('numlock')


def get_numlock_state():
    hllDll = ctypes.WinDLL("User32.dll")
    VK_NUMLOCK = 0x90
    return hllDll.GetKeyState(VK_NUMLOCK)


def get_keyboard_language():  # Gets the keyboard language in use by the current active window process.

    languages = {'0x409': "English - United States", '0x40d': "Hebrew"}

    user32 = ctypes.WinDLL('user32', use_last_error=True)

    # Get the current active window handle
    handle = user32.GetForegroundWindow()

    # Get the thread id from that window handle
    thread_id = user32.GetWindowThreadProcessId(handle, 0)

    # Get the keyboard layout id from the thread_id
    layout_id = user32.GetKeyboardLayout(thread_id)

    # Extract the keyboard language id from the keyboard layout id
    language_id = layout_id & (2 ** 16 - 1)

    # Convert the keyboard language id from decimal to hexadecimal
    language_id_hex = hex(language_id)

    # Check if the hex value is in the dictionary.
    if language_id_hex in languages.keys():
        return languages[language_id_hex]
    else:
        # Return language id hexadecimal value if not found.
        return str(language_id_hex)


def swap_chars(text, current_lang, next_lang):

    layouts = {"English - United States": r"`1234567890-=qwertyuiop[]asdfghjkl;'\zxcvbnm,./",
               "Hebrew": r";1234567890-=/'קראטוןםפ][שדגכעיחלךף,\זסבהנמצתץ."}
    swapped_text = ''
    for char in text:
        for i in range(len(layouts[current_lang])):  # Length of the keyboard layout string
            if char == layouts[current_lang][i]:
                swapped_text += layouts[next_lang][i]
                break
        else:
            swapped_text += char

    return swapped_text


if __name__ == '__main__':
    main()
