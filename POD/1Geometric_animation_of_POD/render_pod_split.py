# -*- coding: utf-8 -*-
"""
渲染脚本：生成POD教学动画（分离版本）
分为2D和3D两部分渲染，避免ThreeDScene的坐标系冲突
"""
import importlib.util
import os
from pathlib import Path
import shutil
import sys
import subprocess


def _resolve_manim_command():
    """
    动态查找 manim 命令，确保跨平台兼容性

    搜索顺序（优先使用 python -m manim，因为更稳定）：
    1. MANIM_EXECUTABLE 环境变量（手动指定）
    2. 在 manim_env 中使用 python -m manim
    3. 系统 PATH 中的 manim 命令
    4. 当前 Python 环境的 python -m manim
    """
    # 1. 检查环境变量
    manual_exec = os.environ.get("MANIM_EXECUTABLE")
    if manual_exec:
        manual_path = Path(manual_exec).expanduser()
        if manual_path.is_file():
            return [str(manual_path)]

    # 2. 优先在 manim_env 中查找 Python 并使用 python -m manim
    # 搜索所有 Conda 环境，优先搜索名称包含 'manim' 的环境
    envs_dirs = [
        Path(sys.prefix) / "envs",          # Conda base 环境下
        Path(sys.prefix).parent / "envs"    # 与当前环境同级
    ]

    def _find_python_in_env(env_path):
        """在环境中查找 Python 可执行文件"""
        if not env_path or not Path(env_path).is_dir():
            return None
        python_names = ["python.exe", "python3.exe", "python"] if os.name == "nt" else ["python3", "python"]
        for subdir in ("Scripts", "bin", ""):
            for python_name in python_names:
                if subdir:
                    candidate = Path(env_path) / subdir / python_name
                else:
                    candidate = Path(env_path) / python_name
                if candidate.is_file():
                    # 检查这个 Python 环境是否有 manim 模块
                    try:
                        result = subprocess.run(
                            [str(candidate), "-c", "import manim; print('OK')"],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if result.returncode == 0 and "OK" in result.stdout:
                            return str(candidate)
                    except (subprocess.TimeoutExpired, FileNotFoundError):
                        pass
        return None

    # 搜索 manim 环境
    possible_envs = []
    for envs_dir in envs_dirs:
        if envs_dir.is_dir():
            # 优先搜索名称包含 'manim' 的环境
            manim_envs = [p for p in envs_dir.iterdir() if p.is_dir() and "manim" in p.name.lower()]
            other_envs = [p for p in envs_dir.iterdir() if p.is_dir() and "manim" not in p.name.lower()]
            possible_envs.extend(manim_envs + other_envs)

    for env_path in possible_envs:
        python_exe = _find_python_in_env(env_path)
        if python_exe:
            return [python_exe, "-m", "manim"]

    # 3. 检查系统 PATH
    manim_exec = shutil.which("manim")
    if manim_exec:
        return [manim_exec]

    # 4. 尝试当前 Python 环境的 python -m manim
    if importlib.util.find_spec("manim"):
        return [sys.executable, "-m", "manim"]

    # 所有方法都失败，抛出错误
    raise RuntimeError(
        "无法找到 manim 可执行文件。\n"
        "请安装 manim 或设置 MANIM_EXECUTABLE 环境变量。"
    )


def _build_manim_args(scene_file, scene_class, quality_flag, preview_flag):
    """构建 manim 渲染命令的完整参数列表"""
    cmd = _resolve_manim_command() + [scene_file, scene_class, quality_flag]
    if preview_flag:
        cmd.append(preview_flag)
    return cmd


def _format_command(cmd_parts):
    """格式化命令用于控制台显示"""
    return " ".join(
        f'"{part}"' if " " in part else part
        for part in cmd_parts
    )


def render_animation(part="both", quality="medium", preview=False):
    """
    渲染动画

    Args:
        part: 渲染部分
            - "2d": 只渲染2D部分 (Scene1-4)
            - "3d": 只渲染3D部分 (Scene5-6)
            - "both": 渲染全部
        quality: 渲染质量
            - "low": 480p15 (快速预览)
            - "medium": 720p30 (标准质量)
            - "high": 1080p60 (高质量)
        preview: 是否只预览最后一帧
    """
    quality_settings = {
        "low": "-ql",
        "medium": "-qm",
        "high": "-qh"
    }

    quality_flag = quality_settings.get(quality, "-qm")
    preview_flag = "-ps" if preview else None

    print("=" * 60)
    print("POD 教学动画渲染（分离版本）")
    print("=" * 60)
    print(f"渲染部分: {part}")
    print(f"质量设置: {quality}")
    print(f"预览模式: {preview}")
    print("=" * 60)

    success = True

    # 渲染2D部分
    if part in ["2d", "both"]:
        print("\n[1/2] 渲染 2D 部分 (Scene1-4: 引入、能量搜索、正交约束、数学公式)...")
        print("-" * 60)
        cmd_2d = _build_manim_args(
            "pod_educational_2d.py",
            "PODEducational2D",
            quality_flag,
            preview_flag
        )
        print(f"命令: {_format_command(cmd_2d)}")
        result = subprocess.run(cmd_2d)
        if result.returncode != 0:
            print("[FAIL] 2D部分渲染失败!")
            success = False
        else:
            print("[OK] 2D部分渲染完成!")
        print("-" * 60)

    # 渲染3D部分
    if part in ["3d", "both"] and success:
        print("\n[2/2] 渲染 3D 部分 (Scene5-6: 3D扩展、总结)...")
        print("-" * 60)
        cmd_3d = _build_manim_args(
            "pod_educational_3d.py",
            "PODEducational3D",
            quality_flag,
            preview_flag
        )
        print(f"命令: {_format_command(cmd_3d)}")
        result = subprocess.run(cmd_3d)
        if result.returncode != 0:
            print("[FAIL] 3D部分渲染失败!")
            success = False
        else:
            print("[OK] 3D部分渲染完成!")
        print("-" * 60)

    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] 渲染完成!")
        print("\n视频位置:")
        if part in ["2d", "both"]:
            print("  - 2D部分: media/videos/pod_educational_2d/")
        if part in ["3d", "both"]:
            print("  - 3D部分: media/videos/pod_educational_3d/")
    else:
        print("[ERROR] 渲染过程中出现错误，请检查上面的输出")
    print("=" * 60)

    return success

if __name__ == "__main__":
    # 默认设置
    part = "both"
    quality = "medium"
    preview = False

    # 解析命令行参数
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["2d", "3d", "both"]:
            part = arg
        elif arg in ["low", "medium", "high"]:
            quality = arg
        elif arg == "preview":
            preview = True

    if len(sys.argv) > 2:
        arg = sys.argv[2].lower()
        if arg in ["low", "medium", "high"]:
            quality = arg
        elif arg == "preview":
            preview = True

    if len(sys.argv) > 3:
        if sys.argv[3].lower() == "preview":
            preview = True

    # 显示使用说明
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
POD 教学动画渲染脚本（分离版本）

用法:
    python render_pod_split.py [部分] [质量] [预览]

参数:
    部分 (可选):
        2d      - 只渲染2D部分 (Scene1-4)
        3d      - 只渲染3D部分 (Scene5-6)
        both    - 渲染全部 (默认)

    质量 (可选):
        low     - 480p15 快速预览
        medium  - 720p30 标准质量 (默认)
        high    - 1080p60 高质量

    预览 (可选):
        preview - 只预览最后一帧

示例:
    python render_pod_split.py                    # 渲染全部，标准质量
    python render_pod_split.py 2d low             # 只渲染2D部分，低质量
    python render_pod_split.py 3d high            # 只渲染3D部分，高质量
    python render_pod_split.py both medium preview # 渲染全部，标准质量，预览模式
        """)
        sys.exit(0)

    render_animation(part, quality, preview)
