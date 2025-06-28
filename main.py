import cv2
import subprocess
import time
import os
import sys
import pyautogui

VALID_COMMANDS = {
    "click_on": "click_on <image.png>        → Click on a template image.",
    "wait": "wait <milliseconds>            → Wait for a specified time.",
    "press_key": "press_key <keycombo>      → Press a key or key combination (e.g. enter, ctrl+s)."
}

def take_screenshot():
    result = subprocess.run([
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-File", "Take-Screenshot.ps1"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[ERROR] Failed to take screenshot:\n{result.stderr}")
        sys.exit(1)

def find_template_coordinates(screenshot_path, template_path, threshold=0.9):
    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    if screenshot is None:
        print(f"[ERROR] Could not load screenshot from '{screenshot_path}'")
        sys.exit(1)

    if template is None:
        print(f"[ERROR] Could not load template image from '{template_path}'")
        sys.exit(1)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        print(f"[MATCH] Found '{os.path.basename(template_path)}' with confidence {max_val:.2f}")
        return max_loc
    else:
        print(f"[ERROR] Template '{os.path.basename(template_path)}' not found on screen.")
        sys.exit(1)

def click_at_coordinates(x, y):
    result = subprocess.run([
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-File", "Click-At-Coordinates.ps1",
        "-X", str(x),
        "-Y", str(y)
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[ERROR] Failed to click at coordinates ({x}, {y}):\n{result.stderr}")
        sys.exit(1)

def press_key(key_combo):
    try:
        keys = key_combo.lower().split("+")
        print(f"[INFO] Pressing keys: {keys}")
        pyautogui.hotkey(*keys)
    except Exception as e:
        print(f"[ERROR] Failed to press key(s) '{key_combo}': {e}")
        sys.exit(1)

def show_valid_commands_and_exit(line_num, command):
    print(f"\n[ERROR] Unknown command on line {line_num}: '{command}'")
    print("[INFO] Valid commands are:")
    for cmd in VALID_COMMANDS.values():
        print("  -", cmd)
    sys.exit(1)

def process_commands(input_file, template_dir="templates"):
    if not os.path.exists(input_file):
        print(f"[ERROR] Input file '{input_file}' not found.")
        sys.exit(1)

    with open(input_file, "r") as f:
        lines = f.readlines()

    for line_num, line in enumerate(lines, start=1):
        command = line.strip()
        if not command or command.startswith("#"):
            continue  # Skip empty or comment lines

        print(f"\n[INFO] Processing line {line_num}: {command}")

        if command.startswith("click_on "):
            image_name = command[len("click_on "):].strip()
            template_path = os.path.join(template_dir, image_name)

            if not os.path.exists(template_path):
                print(f"[ERROR] Template image '{template_path}' not found.")
                sys.exit(1)

            take_screenshot()
            time.sleep(1)

            coords = find_template_coordinates("screenshot.png", template_path)
            click_at_coordinates(coords[0], coords[1])
            time.sleep(0.5)

        elif command.startswith("wait "):
            try:
                wait_time_ms = int(command[len("wait "):].strip())
                print(f"[INFO] Waiting {wait_time_ms}ms")
                time.sleep(wait_time_ms / 1000.0)
            except ValueError:
                print(f"[ERROR] Invalid wait time on line {line_num}: '{command}'")
                sys.exit(1)

        elif command.startswith("press_key "):
            key_combo = command[len("press_key "):].strip()
            if not key_combo:
                print(f"[ERROR] Missing key in 'press_key' command on line {line_num}")
                sys.exit(1)
            press_key(key_combo)
            time.sleep(0.2)

        else:
            show_valid_commands_and_exit(line_num, command)

# Entry point
if __name__ == "__main__":
    try:
        import pyautogui
    except ImportError:
        print("[ERROR] pyautogui not installed. Please run: pip install pyautogui")
        sys.exit(1)

    process_commands("input.txt")
  
