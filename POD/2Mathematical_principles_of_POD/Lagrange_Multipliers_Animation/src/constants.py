"""拉格朗日乘子法动画 - 配色和样式常量

3Blue1Brown 风格的数学可视化配色方案
"""

from manim import Text

# ============ 字体配置 ============
CN_FONT = "Microsoft YaHei"  # Windows 中文字体
# 如果在 macOS 上运行，使用: "PingFang SC"
# 如果安装了 Source Han Sans，使用: "Source Han Sans CN"

# ============ 配色方案 ============
BACKGROUND_COLOR = "#050C1D"  # 深海军蓝背景

# 核心元素颜色
PRIMARY_RED = "#F45B69"  # 约束路径颜色 (鲜艳红色)
TARGET_GRADIENT_COLOR = "#F7C873"  # 目标梯度 ∇f (金色)
CONSTRAINT_GRADIENT_COLOR = "#50A7F6"  # 约束梯度 ∇g (电蓝色)

# 辅助元素颜色
POINT_CLOUD_COLOR = "#9FD8FF"  # 点云颜色 (淡蓝)
GRID_COLOR = "#1D2433"  # 网格线颜色
CONTOUR_COLOR = "#FFFFFF"  # 等高线颜色 (低透明度白色)
CLIMBER_COLOR = "#FCE76C"  # 登山者颜色 (黄色)

# 文字颜色
TEXT_COLOR = "#F4F4F5"  # 主要文字颜色
DIM_TEXT_COLOR = "#A2A7B4"  # 次要文字颜色
HIGHLIGHT_COLOR = "#FF6B9D"  # 高亮颜色

# ============ 字号配置 ============
TITLE_FONT_SIZE = 46
SUBTITLE_FONT_SIZE = 34
BODY_FONT_SIZE = 32
LABEL_FONT_SIZE = 28
CAPTION_FONT_SIZE = 24

# ============ 动画时长配置 ============
# Scene 时长 (秒)
SCENE_DURATIONS = {
    "scene01": 40,  # POD 回顾
    "scene02": 60,  # 3D 山地
    "scene03": 90,  # 2D 梯度
    "scene04": 80,  # 几何洞察
    "scene05": 75,  # 连接 POD
    "scene06": 45,  # 数学总结
}

# ============ 文本工厂函数 ============
def themed_text(message: str, *, font_size: int = BODY_FONT_SIZE, color: str = TEXT_COLOR, **kwargs) -> Text:
    """创建统一风格的文本对象

    Args:
        message: 文本内容
        font_size: 字号
        color: 颜色
        **kwargs: 其他 Text 参数

    Returns:
        配置好的 Text 对象
    """
    return Text(message, font=CN_FONT, font_size=font_size, color=color, **kwargs)
