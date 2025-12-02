# -*- coding: utf-8 -*-
"""
渲染脚本：生成POD教学动画
"""
import os
import sys

def render_animation(quality="medium", preview=False):
    """
    渲染动画

    Args:
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
    preview_flag = "-ps" if preview else ""

    command = f"manim pod_educational.py PODEducational {quality_flag} {preview_flag}"

    print(f"开始渲染动画...")
    print(f"质量设置: {quality}")
    print(f"命令: {command}")
    print("-" * 50)

    os.system(command)

    print("-" * 50)
    print("渲染完成！")
    print(f"视频位置: media/videos/pod_educational/")

if __name__ == "__main__":
    # 默认设置
    quality = "medium"
    preview = False

    # 解析命令行参数
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["low", "medium", "high"]:
            quality = arg
        elif arg == "preview":
            preview = True

    if len(sys.argv) > 2:
        if sys.argv[2].lower() == "preview":
            preview = True

    render_animation(quality, preview)
