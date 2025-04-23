from mouse import get_position
from pygetwindow import getActiveWindow
from pynput import keyboard

last_mouse_pos = (0, 0)
last_active_window = None
keyboard_activity = False


def on_press(_):
    global keyboard_activity
    keyboard_activity = True


keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()


def user_is_active():
    global last_mouse_pos, last_active_window, keyboard_activity

    # Movimiento de mouse
    current_mouse_pos = get_position()
    mouse_moved = current_mouse_pos != last_mouse_pos
    last_mouse_pos = current_mouse_pos

    # Cambio de ventana
    try:
        current_window = getActiveWindow().title
    except:
        current_window = None

    window_changed = current_window != last_active_window
    last_active_window = current_window

    # Uso del teclado
    keyboard_used = keyboard_activity
    keyboard_activity = False

    return mouse_moved or window_changed or keyboard_used
