# Text-to-CAD

AI-powered AutoCAD drawing tools — convert engineering drawings to DWG files using Python + key/mouse simulation.

## Features

- **AutoCAD Control** — Send drawing commands to AutoCAD via Windows API (WM_CHAR messages), works with portable/绿色版 installations
- **SCR Script Generation** — Generate `.scr` script files from image analysis for batch drawing in AutoCAD
- **Drawing Primitives** — Line, Circle, Rectangle, Arc, Polyline, Text, Layer management

## Files

| File | Description |
|------|-------------|
| `.workbuddy/cad_control.py` | Core CAD control library (Windows API key/mouse simulation) |
| `.workbuddy/draw_screw.py` | Screw/螺杆 drawing script |
| `drawing.scr` | Auto-generated SCR script from engineering drawing image |
| `起重螺杆_主视图俯视图.scr` | SCR script for lifting screw front/top view |

## Requirements

- **AutoCAD 2026** (portable/免安装 version)
- **Python 3.9+** with `pyautogui`, `ctypes`
- **Windows** (uses Win32 API for keyboard simulation)

## Quick Start

```bash
# Run a drawing script in AutoCAD
python .workbuddy/cad_control.py

# Or use the module directly
from .workbuddy.cad_control import activate_cad, run_script
activate_cad()
run_script("drawing.scr")
```

## Usage Notes

- Ensure AutoCAD window is open with a drawing (not the start page)
- Do not move keyboard/mouse while commands are being sent
- After running SCR scripts, use `SCALE` command to adjust to real dimensions
