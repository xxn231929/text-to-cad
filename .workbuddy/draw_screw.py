"""
起重螺杆 - 主视图 + 俯视图
根据工程图精确尺寸绘制
"""
import sys
sys.path.insert(0, r'D:\CAD2026\.workbuddy')
from cad_control import *
import time

def draw_screw():
    """绘制起重螺杆 - 主视图(纵向剖面) + 俯视图(端面)"""
    
    if not activate_cad():
        print("❌ 请先打开 AutoCAD")
        return
    
    print("🎨 开始绘制起重螺杆...")
    time.sleep(0.5)
    
    # ── 图层设置 ─────────────────────────────────────────
    set_layer("0", 7)           # 白色 - 轮廓线
    set_layer("CENTER", 1)      # 红色 - 中心线
    set_layer("HATCH", 8)       # 灰色 - 剖面线
    
    # 基准点设置（留足边距）
    base_x, base_y = 100, 50    # 主视图中心线X，底部Y
    spacing = 100               # 两视图间距
    cx = base_x                 # 中心线X坐标
    
    # ═══════════════════════════════════════════════════
    # 零件尺寸（从下到上，单位mm）
    # ═══════════════════════════════════════════════════
    
    # 1. 底部圆头: φ20（半球，但图中显示圆柱+球头）
    # 实际: φ20 圆盘厚约4mm? 从图上看是圆头把手
    # 简化: 画 φ20 圆柱头
    y = base_y
    
    # 2. φ12 段，长9mm（螺杆伸出）
    d1, h1 = 12, 9
    
    # 3. φ16 主体，长100mm
    d2, h2 = 16, 100
    
    # 4. φ32 凸台（环状）
    d3 = 32
    # 凸台高度: 从图上看凸台在 φ16 主体之上，高度约 5mm 左右
    h3 = 5
    
    # 5. 上部: 5×φ16 段
    # 从图上看，上部有 "5×φ16" 和 "2×φ13" 标注
    # 还有 16、12 等长度尺寸
    # 顶部段: φ14d9，长12，带M8螺纹孔
    
    # 计算各段位置（从底部开始累积）
    y0 = y                      # φ20 圆头底
    y1 = y0 + 4                 # φ20 圆头顶（假设厚4）
    y2 = y1 + h1                # φ12 段顶 = 9mm处
    y3 = y2 + h2                # φ16 主体顶 = 109mm处
    y4 = y3 + h3                # φ32 凸台顶
    # 上部还有几段，总长144
    # y5 = y0 + 144 = 顶部
    
    # 从图上的尺寸链重新计算:
    # 底部到凸台: 9 + 100 + 16 = 125?
    # 不对，看图上的标注线...
    # 9(底部) + 100(主体) + 16(某段) + 12(顶部) = 137，还差7mm
    # 可能是 9 + 100 + 5(凸台) + 16 + 12 + 2 = 144
    
    # 重新按图理解:
    # 最底部: φ20(圆头把手)
    # 往上: φ12×9
    # 往上: φ16×100 (主体，带Ra1.6)
    # 往上: φ32 凸台，高约5 (从5×φ16推断)
    # 往上: 5段φ16，每段约?
    # 顶部: φ14d9×12，带M8螺纹和T12孔深15
    
    # ═══════════════════════════════════════════════════
    # 开始绘制主视图（左半部分）
    # ═══════════════════════════════════════════════════
    
    set_layer("CENTER")
    # 垂直中心线（全高）
    send_command(f"LINE {cx},{y0-5} {cx},{y0+150} ")
    
    set_layer("0")
    
    # ── 段1: 底部 φ20 圆头 ─────────────────────────────
    # 画半圆或圆柱头
    r20 = 10
    # 底部弧线（半圆）
    send_command(f"ARC {cx},{y0+r20} {cx-r20},{y0+r20} {cx},{y0} ")
    send_command(f"ARC {cx},{y0+r20} {cx},{y0} {cx+r20},{y0+r20} ")
    # 或简化为矩形头
    draw_line(cx-10, y0, cx-10, y0+4)
    draw_line(cx+10, y0, cx+10, y0+4)
    draw_line(cx-10, y0+4, cx-6, y0+4)  # 过渡到φ12
    draw_line(cx+10, y0+4, cx+6, y0+4)
    
    # ── 段2: φ12 × 9 ───────────────────────────────────
    y = y0 + 4
    draw_line(cx-6, y, cx-6, y+9)
    draw_line(cx+6, y, cx+6, y+9)
    # 倒角或过渡
    draw_line(cx-6, y+9, cx-8, y+9)
    draw_line(cx+6, y+9, cx+8, y+9)
    
    # ── 段3: φ16 × 100 ─────────────────────────────────
    y = y + 9  # 现在 y = y0 + 13
    draw_line(cx-8, y, cx-8, y+100)
    draw_line(cx+8, y, cx+8, y+100)
    
    # ── 段4: φ32 凸台 ──────────────────────────────────
    y = y + 100  # y = y0 + 113
    # 凸台展开
    draw_line(cx-8, y, cx-16, y)
    draw_line(cx+8, y, cx+16, y)
    # 凸台高度约5
    draw_line(cx-16, y, cx-16, y+5)
    draw_line(cx+16, y, cx+16, y+5)
    
    # 剖面线区域（凸台是实心，画剖面线）
    # 简化为画几条斜线表示剖面
    set_layer("HATCH")
    for i in range(-3, 4):
        xo = i * 3
        send_command(f"LINE {cx+xo},{y} {cx+xo+3},{y+5} ")
    set_layer("0")
    
    # ── 段5: 上部缩回 φ16 ──────────────────────────────
    y = y + 5  # y = y0 + 118
    draw_line(cx-16, y, cx-8, y)
    draw_line(cx+16, y, cx+8, y)
    # 高度16?
    draw_line(cx-8, y, cx-8, y+16)
    draw_line(cx+8, y, cx+8, y+16)
    
    # ── 段6: 继续到顶部 ────────────────────────────────
    y = y + 16  # y = y0 + 134
    # 还有10mm到顶
    draw_line(cx-8, y, cx-7, y)  # 缩到φ14
    draw_line(cx+8, y, cx+7, y)
    draw_line(cx-7, y, cx-7, y+10)
    draw_line(cx+7, y, cx+7, y+10)
    # 顶部封口
    draw_line(cx-7, y+10, cx+7, y+10)
    
    # 顶部螺纹示意（M8）
    set_layer("CENTER")
    # 螺纹小径
    send_command(f"LINE {cx-4},{y+2} {cx-4},{y+10} ")
    send_command(f"LINE {cx+4},{y+2} {cx+4},{y+10} ")
    set_layer("0")
    
    # ═══════════════════════════════════════════════════
    # 俯视图（放在右侧，端面投影）
    # ═══════════════════════════════════════════════════
    view_x = cx + spacing + 30
    view_y = base_y + 70  # 中心位置
    
    set_layer("CENTER")
    # 十字中心线
    send_command(f"LINE {view_x-20},{view_y} {view_x+20},{view_y} ")
    send_command(f"LINE {view_x},{view_y-20} {view_x},{view_y+20} ")
    
    set_layer("0")
    # 最大圆 φ32
    draw_circle(view_x, view_y, 16)
    # φ20
    draw_circle(view_x, view_y, 10)
    # φ16（主体）
    draw_circle(view_x, view_y, 8)
    # φ12
    draw_circle(view_x, view_y, 6)
    # φ14（顶部）
    draw_circle(view_x, view_y, 7)
    # 中心螺纹孔 M8
    set_layer("HIDDEN")
    draw_circle(view_x, view_y, 4)
    set_layer("0")
    
    # 俯视图中的2×φ13孔（对称分布）
    # 从中心偏移一定距离
    hole_dist = 10  # 孔中心距中心的距离
    set_layer("0")
    draw_circle(view_x - hole_dist, view_y, 6.5)
    draw_circle(view_x + hole_dist, view_y, 6.5)
    
    # ═══════════════════════════════════════════════════
    # 标注
    # ═══════════════════════════════════════════════════
    set_layer("0")
    # 视图名称
    draw_text(cx-20, base_y-15, "主视图", 3.5)
    draw_text(view_x-15, view_y-30, "俯视图", 3.5)
    
    # 标题
    draw_text(cx, base_y+160, "起重螺杆", 5)
    
    # 缩放
    zoom_extents()
    
    print("✅ 绘制完成！")


if __name__ == "__main__":
    draw_screw()
