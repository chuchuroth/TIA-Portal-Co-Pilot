import pyautogui
import pytesseract
import tkinter as tk
from PIL import ImageGrab
import time

# Setup GUI window
root = tk.Tk()
root.title("TIA-Pilot Lite")
root.geometry("300x200")

# Label and input field
label = tk.Label(root, text="Tell me what to do in TIA:", font=("Arial", 12))
label.pack(pady=10)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

output = tk.Label(root, text="Suggestion: None yet", font=("Arial", 10))
output.pack(pady=10)

# Fake AI "brain" - simple rules for now
def suggest_action(command):
    command = command.lower()
    if "add rpm tag" in command:
        return "Suggestion: Tag `Drill_RPM`, Type: Int, Address: MW10 - Apply?"
    elif "add torque tag" in command:
        return "Suggestion: Tag `Drill_Torque`, Type: Real, Address: MD14 - Apply?"
    elif "debug" in command:
        return "Suggestion: Check if `M0.0` is set - common start bit missing."
    else:
        return "Suggestion: I don’t get it yet - try 'Add RPM tag' or 'Debug this'."

# Read TIA screen (OCR) - basic check
def read_tia_screen():
    # Grab small screen chunk (adjust x, y, width, height to your TIA window)
    screenshot = ImageGrab.grab(bbox=(100, 100, 500, 300))  # Top-left TIA area
    text = pytesseract.image_to_string(screenshot)
    return text.lower()

# Act on suggestion - types it into TIA
def apply_suggestion(suggestion):
    # Move mouse to TIA (adjust x, y to your TIA tag window)
    pyautogui.moveTo(200, 400, duration=0.5)  # Click into tag table
    pyautogui.click()
    time.sleep(0.5)
    # Type suggestion (just the tag part for now)
    if "MW10" in suggestion:
        pyautogui.typewrite("Drill_RPM\nInt\nMW10", interval=0.1)
    elif "MD14" in suggestion:
        pyautogui.typewrite("Drill_Torque\nReal\nMD14", interval=0.1)
    # Leaves you to hit Enter in TIA

# Main button action
def process_command():
    command = entry.get()
    tia_text = read_tia_screen()
    print(f"TIA says: {tia_text}")  # Debug - see what it reads
    
    # Check if we're in the right spot
    if "plc tags" in tia_text or "hmi tags" in tia_text:
        suggestion = suggest_action(command)
        output.config(text=suggestion)
        if "Apply?" in suggestion and tk.messagebox.askyesno("TIA-Pilot", "Apply this?"):
            apply_suggestion(suggestion)
    else:
        output.config(text="Suggestion: Open PLC Tags or HMI Tags first!")

# Button to trigger
button = tk.Button(root, text="Go!", command=process_command)
button.pack(pady=10)

# Run the GUI
root.mainloop()
