"""Scene 1: POD Review - 顶层场景文件

这个文件用于 manim 命令行直接渲染
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入 src 模块中的场景类并重新定义在当前命名空间
from src.scene01_pod_review import Scene01PODReview as _Scene01PODReview

class Scene01PODReview(_Scene01PODReview):
    """Scene 1: POD 回顾场景 - 暴露给 manim"""
    pass

