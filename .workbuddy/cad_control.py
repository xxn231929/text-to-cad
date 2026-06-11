"""
CAD Control v2 - 通过 Windows API 键鼠消息直接控制 AutoCAD
适用于未注册 COM 的绿色版/免安装版 AutoCAD

改进点：
1. send_command 每段参数之间用 Enter 分隔
2. 使用 WM_CHAR 直接发送字符，跳过输入法拦截
3. 命令末尾自动确认
"""
import ctypes
import time
from ctypes import wintypes

# ── Windows API ──────────────────────────────────────────────
user32 = ctypes.windll.user32

WM_CHAR      = 0x0102
WM_KEYDOWN   = 0x0100
WM_KEYUP     = 0x0101
VK_RETURN    = 0x0D
VK_ESCAPE    = 0x1B
VK_SPACE     = 0x20

# 缓存当前 CAD 窗口句柄
_cad_hwnd = None


def find_cad_window():
    """查找 AutoCAD 主窗口"""
    windows = []
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    
    def callback(hwnd, lparam):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            if ('AutoCAD' in title or 'acad' in title.lower()) and user32.IsWindowVisible(hwnd):
                windows.append((hwnd, title))
        return True
    
    user32.EnumWindows(WNDENUMPROC(callback), 0)
    return windows


def activate_cad():
    """激活 AutoCAD 窗口"""
    global _cad_hwnd
    windows = find_cad_window()
    if not windows:
        print("❌ 未找到 AutoCAD 窗口")
        return False
    _cad_hwnd = windows[0][0]
    if user32.IsIconic(_cad_hwnd):
        user32.ShowWindow(_cad_hwnd, 9)
    user32.SetForegroundWindow(_cad_hwnd)
    time.sleep(0.3)
    print(f"✅ 已激活: {windows[0][1]}")
    return True


def _send_key(hwnd, vk_code):
    """发送一次按键事件 (keydown + keyup)"""
    user32.PostMessageW(hwnd, WM_KEYDOWN, vk_code, 0)
    time.sleep(0.01)
    user32.PostMessageW(hwnd, WM_KEYUP, vk_code, 0)


def _send_char(hwnd, ch):
    """发送单个字符"""
    user32.PostMessageW(hwnd, WM_CHAR, ord(ch), 0)
    time.sleep(0.003)


def _send_text(hwnd, text):
    """逐字符发送文本"""
    for ch in text:
        _send_char(hwnd, ch)


def send_enter(hwnd=None):
    """发送回车"""
    if hwnd is None:
        hwnd = _cad_hwnd
    _send_key(hwnd, VK_RETURN)
    time.sleep(0.08)


def send_esc(times=3):
    """发送 ESC 取消当前命令"""
    for _ in range(times):
        _send_key(_cad_hwnd, VK_ESCAPE)
        time.sleep(0.03)
    time.sleep(0.05)


def send_command(cmd):
    """
    发送完整CAD命令。
    命令用空格分隔为多段，每段发送后按 Enter 确认。
    例如 "LINE 0,0 100,100 " 会依次：
      LINE <Enter> 0,0 <Enter> 100,100 <Enter> <Enter>结束
    末尾连续空格=额外Enter结束命令
    """
    global _cad_hwnd
    # 先取消当前命令
    send_esc()
    
    # 解析命令：以空格分隔
    parts = cmd.strip().split()
    for part in parts:
        _send_text(_cad_hwnd, part)
        time.sleep(0.02)
        send_enter(_cad_hwnd)
    
    # 命令末尾总是多一个 Enter 来确认/结束
    send_enter(_cad_hwnd)
    time.sleep(0.1)


# ── 封装函数 ──────────────────────────────────────────────────

def draw_line(x1, y1, x2, y2):
    send_command(f"LINE {x1},{y1} {x2},{y2}")

def draw_circle(cx, cy, radius):
    send_command(f"CIRCLE {cx},{cy} {radius}")

def draw_rectangle(x1, y1, x2, y2):
    send_command(f"RECTANGLE {x1},{y1} {x2},{y2}")

def draw_arc(cx, cy, radius, start_angle, end_angle):
    from math import cos, sin, radians
    sx = cx + radius * cos(radians(start_angle))
    sy = cy + radius * sin(radians(start_angle))
    ex = cx + radius * cos(radians(end_angle))
    ey = cy + radius * sin(radians(end_angle))
    send_command(f"ARC C {cx},{cy} {sx:.2f},{sy:.2f} {ex:.2f},{ey:.2f}")

def draw_polyline(points):
    cmd = "PLINE " + " ".join(f"{x},{y}" for x, y in points)
    send_command(cmd)

def draw_text(x, y, text, height=2.5, rotation=0):
    send_command(f"TEXT {x},{y} {height} {rotation} {text}")

def set_layer(layer_name, color=None):
    if color:
        send_command(f"-LAYER M {layer_name} C {color}")
    else:
        send_command(f"-LAYER M {layer_name}")

def zoom_extents():
    send_command("ZOOM E")

def zoom_window(x1, y1, x2, y2):
    send_command(f"ZOOM W {x1},{y1} {x2},{y2}")

def erase_all():
    send_command("ERASE ALL")

def new_drawing():
    import pyautogui
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(0.5)
    send_esc()
    send_enter()

def run_script(script_path):
    send_command(f"SCRIPT {script_path}")

def regen():
    send_command("REGEN")


if __name__ == "__main__":
    if activate_cad():
        print("测试：画一个矩形+圆...")
        draw_rectangle(0, 0, 200, 100)
        time.sleep(0.3)
        draw_circle(100, 50, 40)
        time.sleep(0.3)
        zoom_extents()
        print("✅ 完成")
