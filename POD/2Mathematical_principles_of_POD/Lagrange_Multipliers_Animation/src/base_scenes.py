# -*- coding: utf-8 -*-
"""拉格朗日乘子法动画 - 基础场景类

包含 2D 和 3D 场景基类，以及可复用的 HUD 组件
"""

from __future__ import annotations
import numpy as np
from manim import (
    MovingCameraScene,
    ThreeDScene,
    DecimalNumber,
    Rectangle,
    RoundedRectangle,
    VGroup,
    Dot,
    always_redraw,
    ValueTracker,
    RIGHT,
    UP,
    DOWN,
    LEFT,
    UL,
)

from .constants import (
    BACKGROUND_COLOR,
    DIM_TEXT_COLOR,
    POINT_CLOUD_COLOR,
    PRIMARY_RED,
    TEXT_COLOR,
    TITLE_FONT_SIZE,
    SUBTITLE_FONT_SIZE,
    themed_text,
)


# ============ 2D 场景基类 ============

class BaseLagrangeScene(MovingCameraScene):
    """2D 场景基类 (带移动相机)

    提供统一的背景、相机设置和文本样式
    """

    def setup(self) -> None:
        """初始化场景"""
        super().setup()
        self.camera.background_color = BACKGROUND_COLOR
        self.camera.frame.set(width=14)

    def add_scene_header(self, title: str, subtitle: str | None = None) -> VGroup:
        """添加场景标题

        Args:
            title: 主标题
            subtitle: 副标题 (可选)

        Returns:
            标题组 VGroup
        """
        title_text = themed_text(title, font_size=TITLE_FONT_SIZE, color=PRIMARY_RED)
        title_text.to_corner(UL).shift(0.4 * RIGHT + 0.35 * DOWN)

        group = VGroup(title_text)

        if subtitle:
            subtitle_text = themed_text(subtitle, font_size=SUBTITLE_FONT_SIZE, color=TEXT_COLOR)
            subtitle_text.next_to(title_text, DOWN, aligned_edge=LEFT, buff=0.1)
            group.add(subtitle_text)

        self.add(group)
        return group

    def build_energy_meter(self, samples: np.ndarray, angle_tracker: ValueTracker) -> VGroup:
        """构建能量计量器 HUD (用于 POD 回顾)

        显示投影能量占总能量的比例

        Args:
            samples: 点云数据 (N x 2 数组)
            angle_tracker: 角度 ValueTracker

        Returns:
            能量计量器 VGroup
        """
        samples = np.asarray(samples)
        total_energy = np.sum(np.linalg.norm(samples, axis=1) ** 2) + 1e-6

        # 外框（调整位置，避免和标题重叠）
        meter_outline = RoundedRectangle(width=3.6, height=0.6, corner_radius=0.15)
        meter_outline.set_fill(BACKGROUND_COLOR, opacity=0.6)
        meter_outline.set_stroke(color=TEXT_COLOR, width=2)
        # 增加边距
        meter_outline.to_corner(UP + RIGHT).shift(LEFT * 1.2 + DOWN * 1.2)

        # 能量比例计算函数
        def energy_ratio() -> float:
            angle = angle_tracker.get_value()
            direction = np.array([np.cos(angle), np.sin(angle)])
            projections = samples @ direction
            energy = np.sum(projections**2)
            return float(np.clip(energy / total_energy, 0.0, 1.0))

        # 动态进度条（修复：align_to 必须传入 Mobject 而不是坐标点）
        progress_bar = always_redraw(
            lambda: Rectangle(
                width=max(0.02, energy_ratio() * (meter_outline.width - 0.12)),
                height=meter_outline.height - 0.08,
                fill_color=PRIMARY_RED,
                fill_opacity=0.85,
                stroke_width=0,
            ).align_to(meter_outline, LEFT).shift(RIGHT * 0.06)  # 修复：传入对象而不是坐标
        )

        # 标签
        meter_label = themed_text("能量投影", font_size=30, color=DIM_TEXT_COLOR)
        meter_label.next_to(meter_outline, UP, buff=0.15)

        # 数值显示
        value_number = DecimalNumber(0, num_decimal_places=0, include_sign=False)
        value_number.set_color(PRIMARY_RED)
        value_number.scale(0.7)
        value_number.add_updater(lambda mob: mob.set_value(100 * energy_ratio()))
        value_number.next_to(meter_outline, RIGHT, buff=0.2)

        percent_sign = themed_text("%", font_size=30, color=DIM_TEXT_COLOR)
        percent_sign.next_to(value_number, RIGHT, buff=0.05)

        # 图例
        legend = themed_text("主方向能量捕获", font_size=28, color=DIM_TEXT_COLOR)
        legend.next_to(meter_outline, DOWN, buff=0.1)

        hud = VGroup(meter_label, meter_outline, progress_bar, value_number, percent_sign, legend)
        return hud


# ============ 3D 场景基类 ============

class BaseLagrangeThreeDScene(ThreeDScene):
    """3D 场景基类

    提供统一的 3D 相机设置和背景
    """

    def setup(self) -> None:
        """初始化 3D 场景"""
        super().setup()
        self.camera.background_color = BACKGROUND_COLOR

    def add_scene_header(self, title: str, subtitle: str | None = None) -> VGroup:
        """添加场景标题 (与 2D 场景一致)

        Args:
            title: 主标题
            subtitle: 副标题 (可选)

        Returns:
            标题组 VGroup
        """
        title_text = themed_text(title, font_size=TITLE_FONT_SIZE, color=PRIMARY_RED)
        title_text.to_corner(UL).shift(0.4 * RIGHT + 0.35 * DOWN)
        title_text.fix_in_frame()  # 固定在相机坐标系

        group = VGroup(title_text)

        if subtitle:
            subtitle_text = themed_text(subtitle, font_size=SUBTITLE_FONT_SIZE, color=TEXT_COLOR)
            subtitle_text.next_to(title_text, DOWN, aligned_edge=LEFT, buff=0.1)
            subtitle_text.fix_in_frame()
            group.add(subtitle_text)

        self.add(group)
        return group

    def smooth_camera_transition(self, phi: float = 45, theta: float = -45,
                                gamma: float = 0, distance: float = 8,
                                run_time: float = 2.0):
        """平滑相机过渡

        Args:
            phi: 仰角 (度)
            theta: 方位角 (度)
            gamma: 滚转角 (度)
            distance: 相机距离
            run_time: 动画时长
        """
        self.move_camera(
            phi=phi * np.pi / 180,
            theta=theta * np.pi / 180,
            gamma=gamma * np.pi / 180,
            frame_center=[0, 0, 0],
            zoom=distance,
            run_time=run_time,
        )


# ============ 可复用组件 ============

class SimpleDot(Dot):
    """简化的点对象 (用于点云)

    Args:
        position: 位置
        color: 颜色
        radius: 半径
        opacity: 不透明度
    """

    def __init__(self, position: np.ndarray, color: str = POINT_CLOUD_COLOR,
                 radius: float = 0.04, opacity: float = 0.7):
        super().__init__(point=position, color=color, radius=radius)
        self.set_opacity(opacity)
