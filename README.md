# TIA-Portal-Co-Pilot

Let’s build a mini-version of **TIA-Pilot AI-agent** as a Python script—a proof-of-concept plug-in for TIA Portal that acts as a co-pilot for PLC programmers. This won’t be a full native plug-in (Siemens locks that down), but a standalone tool that watches your TIA screen, suggests basic PLC/WinCC actions, and types them in. We’ll keep it simple, beginner-friendly, and tied to your skills (e.g., Python, GUI tinkering), with a nod to your job tasks (e.g., Task 1, 3, 8). I’ll explain it in spoken terms, then give you the script to run and tweak.

---

### The Mini-Version: TIA-Pilot Lite

#### What It Does
- **Watches**: Reads what’s on your TIA Portal screen (e.g., “PLC Tags” window).
- **Listens**: You type a command in a little Python GUI—like “Add RPM tag” or “Debug this.”
- **Suggests**: Pops a suggestion—like `MW10, Int` for a tag or “Check `M0.0`”—based on basic TIA rules.
- **Types**: Pastes it into TIA for you (you hit “Apply” to confirm).
- **Goal**: Mimics a co-pilot—small scope (tags, basic debug), but shows the AI vibe.

#### Tools
- **Python**: Your go-to (3.7+).
- **Libraries**:
  - `pyautogui`: Moves the mouse, types stuff—our hack to “plug in” to TIA.
  - `pytesseract`: Reads TIA’s screen text (OCR)—crude but works.
  - `tkinter`: Simple GUI for your commands.
  - `PIL` (Pillow): Grabs screenshots for OCR.
- **No AI Yet**: We’ll fake it with rules (e.g., “RPM = Int tag”)—add GPT later if you want.

#### Setup
- **Install**: `pip install pyautogui pytesseract Pillow tkinter` (run in terminal).
- **Tesseract**: Grab Tesseract OCR (free)—Windows: `chocolatey install tesseract` or download from `github.com/tesseract-ocr/tesseract`.
- **TIA Portal**: Trial open (your sim from last time—S7-1200 + WinCC).

---

### Python Script: TIA-Pilot Lite

```python
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
```

---

### How to Run It

#### Step 1: Prep TIA
- Open TIA Portal (your “Drill_Sim_Test” project).
- Go to “PLC_1” > “PLC Tags” > “Default Tag Table”—keep this window visible.
- Resize TIA to fit your screen top-left (e.g., 500x300 pixels)—makes OCR easier.

#### Step 2: Run the Script
- Save the script as `tia_pilot.py`.
- Terminal: `python tia_pilot.py`—GUI pops up.
- TIA open, cursor in “PLC Tags” table.

#### Step 3: Test It
1. **Command**: Type “Add RPM tag” > click “Go!”
   - GUI says: “Suggestion: Tag `Drill_RPM`, Type: Int, Address: MW10 - Apply?”
   - Hit “Yes”—watch it type `Drill_RPM`, `Int`, `MW10` into TIA’s tag table.
   - You press Enter in TIA to save it.
2. **Command**: “Debug this” > “Go!”
   - GUI: “Suggestion: Check if `M0.0` is set - common start bit missing.”
   - No typing—just a tip for now.
3. **Wrong Spot**: Move TIA to “Program Blocks” > type “Add RPM tag.”
   - GUI: “Suggestion: Open PLC Tags or HMI Tags first!”

---

### How It Works

#### The Pieces
- **GUI**: Tkinter box—your command hub, like your FLEX drill tracker.
- **Screen Read**: `pytesseract` scans TIA—checks if you’re in “PLC Tags” (crude but functional).
- **Fake AI**: `suggest_action`—hard-coded rules for now (RPM = `MW10`, etc.)—mimics Copilot’s smarts.
- **Action**: `pyautogui` moves the mouse, types—like a robot typist for TIA.

#### Your Tie-In
- Like your MCP/Copilot play—AI guesses your next move, saves typing.
- Ties to WinCC tags (Task 3)—`MW10` matches your sim setup.

---

### Tuning It

#### Adjust Coordinates
- **OCR Box**: `bbox=(100, 100, 500, 300)`—tweak x, y, width, height to catch TIA’s tag window (trial and error—watch `print(tia_text)` output).
- **Mouse Move**: `moveTo(200, 400)`—adjust to click your TIA tag table (test with `pyautogui.position()` in a separate script—hover, print coords).

#### Add Smarts
- More Commands: Edit `suggest_action`—e.g., “Add Start button” → “WinCC Button, SetBit `M0.0`.”
- Real AI: Swap rules for GPT (e.g., `openai` API)—feed it TIA snippets, ask “Suggest a tag.”

#### Debug
- **OCR Fails**: Text blurry? Zoom TIA, adjust `bbox`. Install Tesseract right (path set?).
- **Typing Off**: Mouse coords wrong—recalibrate with your screen.

---

### Why It’s Cool
- **Proof**: Shows an AI co-pilot in action—small but wild for Task 8 creativity.
- **Demo**: Record this (OBS Studio)—“Here’s my TIA-Pilot typing a tag!”—interview gold.
- **Scalable**: Add servo tuning tips (Task 4) or safety checks (Task 5) later.

#### Next Level
- **HMI Tags**: Add “Add Torque tag to WinCC”—types `HMI_Torque, Real, MD14`.
- **AI Boost**: Hook up a free GPT (e.g., Hugging Face)—train on your sim code.
