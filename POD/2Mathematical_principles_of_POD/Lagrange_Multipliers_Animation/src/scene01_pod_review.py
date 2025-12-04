# -*- coding: utf-8 -*-
"""Scene 1: POD 回顾场景

时长: 0:00 - 0:40 (40 秒)
内容: 快速回顾 POD 的核心思想 - 通过约束最优化寻找主方向
"""

from __future__ import annotations
import numpy as np
from manim import (
    Arrow,
    Ellipse,
    FadeIn,
    FadeOut,
    LaggedStart,
    MathTex,
    NumberPlane,
    ORIGIN,
    RoundedRectangle,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    DR,
    DL,
    there_and_back,  # rate function
    smooth,  # rate function
)

from .base_scenes import BaseLagrangeScene, SimpleDot
from .constants import (
    GRID_COLOR,
    POINT_CLOUD_COLOR,
    PRIMARY_RED,
    TEXT_COLOR,
    SCENE_DURATIONS,
    themed_text,
)


class Scene01PODReview(BaseLagrangeScene):
    """Scene 1: POD 回顾

    展示内容:
    1. 2D 椭圆点云
    2. 旋转的主方向向量
    3. 实时能量计量器
    4. POD 问题公式
    5. 核心问题: 为什么约束最优化 → 特征值问题?
    """

    def construct(self) -> None:
        """场景主流程"""
        # ===== 1. 场景标题 =====
        header = self.add_scene_header(
            "Scene 1 · POD 回顾",
            subtitle="约束最优  →  特征值直觉",
        )
        header.shift(DOWN * 0.2)  # 给 HUD 留出空间

        # ===== 2. 创建坐标平面 =====
        main_plane = self._create_number_plane()

        intro_text = themed_text("POD：寻找捕获最多能量的方向", font_size=34, color=TEXT_COLOR)
        # 调整位置：更靠下，避免和标题重叠
        intro_text.next_to(main_plane, UP, buff=0.7).shift(RIGHT * 0.3)

        self.play(FadeIn(main_plane, run_time=1.0), Write(intro_text))

        # ===== 3. 椭圆和点云 =====
        ellipse = Ellipse(
            width=8.0,
            height=4.2,
            stroke_color=TEXT_COLOR,
            stroke_opacity=0.5,
            stroke_width=2.5,
        )
        ellipse.move_to(ORIGIN)
        self.play(FadeIn(ellipse, run_time=0.8))

        # 生成点云
        point_cloud, samples = self._create_point_cloud(ellipse)
        self.play(
            LaggedStart(
                *(FadeIn(dot, scale=0.2) for dot in point_cloud),
                lag_ratio=0.01,
                run_time=1.4,
            )
        )

        # ===== 4. 主方向向量 =====
        # 从 -π/4 开始（对齐椭圆主轴），避免从 0° 开始的突兀感
        angle_tracker = ValueTracker(-np.pi / 4)
        principal_arrow = self._create_principal_axis(angle_tracker)
        label_u = self._create_axis_label(principal_arrow)  # 改进标签跟随逻辑

        self.play(
            FadeIn(principal_arrow, shift=RIGHT * 0.5),
            FadeIn(label_u, shift=UP * 0.1)
        )
        self.wait(0.8)  # 停顿观察初始状态

        # ===== 5. 能量计量器（在椭圆出现后才显示，避免和标题重叠）=====
        energy_meter = self.build_energy_meter(samples, angle_tracker)
        # 调整位置：更靠右下，留出更多边距
        energy_meter.to_corner(UP + RIGHT).shift(LEFT * 1.2 + DOWN * 1.2)

        # 淡出 intro_text，为 HUD 腾出视觉空间
        self.play(
            FadeIn(energy_meter, shift=LEFT * 0.3),
            FadeOut(intro_text),
            run_time=1.0
        )

        # ===== 6. 旋转动画 =====
        # 旋转到垂直方向（平滑过渡）
        self.play(
            angle_tracker.animate.set_value(np.pi / 2),
            run_time=3.5,
            rate_func=smooth
        )
        self.wait(1.2)  # 观察垂直方向的能量

        # 来回摆动展示能量变化
        self.play(
            angle_tracker.animate.set_value(-np.pi / 3),
            run_time=4.0,
            rate_func=there_and_back,
        )
        self.wait(0.8)  # 停顿

        # ===== 7. 能量提示 =====
        energy_hint = themed_text("最大能量投影 = 主模态", font_size=28, color=TEXT_COLOR)
        # 调整位置：更多向下间距，避免和卡片/公式冲突
        energy_hint.next_to(main_plane, DOWN, buff=0.8)
        self.play(Write(energy_hint))
        self.wait(1.8)  # 强调这个重要概念

        # ===== 8. POD 公式 =====
        formula = MathTex(
            r"\max_{u} \; u^{\top} C u",
            r"\quad \text{s.t.} \quad \|u\| = 1",
            color=TEXT_COLOR,
        )
        formula.scale(0.8)  # 再缩小一点
        # 调整位置：更靠下，和能量提示对齐
        formula.to_corner(DR).shift(LEFT * 0.8 + UP * 0.3)
        self.play(Write(formula))
        self.wait(1.2)  # 停顿以便观看公式

        # ===== 9. 核心问题卡片（在公式出现后才显示，避免底部过于拥挤）=====
        question_card = self._build_question_card()
        # 调整位置和大小
        self.play(FadeIn(question_card, shift=UP * 0.4), run_time=0.8)
        self.wait(3.5)  # 留出时间思考核心问题

        # ===== 10. 淡出所有元素 =====
        all_elements = VGroup(
            main_plane, ellipse, point_cloud, principal_arrow, label_u,
            energy_meter, formula, energy_hint, question_card
        )
        self.play(FadeOut(all_elements), run_time=1.0)
        self.play(FadeOut(header), run_time=0.5)

    # ========== 辅助方法 ==========

    def _create_number_plane(self) -> NumberPlane:
        """创建数值坐标平面"""
        plane = NumberPlane(
            x_range=[-4.5, 4.5, 1],
            y_range=[-3.0, 3.0, 1],
            faded_line_ratio=2,
            axis_config={"stroke_color": GRID_COLOR, "stroke_opacity": 0.7},
            background_line_style={
                "stroke_color": GRID_COLOR,
                "stroke_opacity": 0.2,
                "stroke_width": 1,
            },
        )
        plane.scale(0.95)
        return plane

    def _create_point_cloud(self, ellipse: Ellipse, num_samples: int = 160) -> tuple[VGroup, np.ndarray]:
        """创建椭圆点云

        Args:
            ellipse: 椭圆对象
            num_samples: 采样点数量

        Returns:
            (点云 VGroup, 坐标数组)
        """
        rng = np.random.default_rng(seed=8)
        dots = VGroup()
        coords = []

        for _ in range(num_samples):
            theta = rng.uniform(0, 2 * np.pi)
            radius = 0.35 + 0.6 * rng.random()  # 半径在 [0.35, 0.95] 之间

            x = 0.5 * ellipse.width * radius * np.cos(theta)
            y = 0.5 * ellipse.height * radius * np.sin(theta)

            coord = np.array([x, y, 0.0])
            dot = SimpleDot(position=coord, color=POINT_CLOUD_COLOR)
            dots.add(dot)
            coords.append([x, y])  # 只保存 x, y 用于能量计算

        return dots, np.array(coords)

    def _create_principal_axis(self, tracker: ValueTracker) -> Arrow:
        """创建动态主方向箭头

        Args:
            tracker: 角度 ValueTracker

        Returns:
            动态更新的箭头
        """
        def make_arrow():
            arrow = Arrow(
                ORIGIN,
                RIGHT * 3.5,
                buff=0,
                stroke_width=6,
                color=PRIMARY_RED,
            )
            arrow.rotate(tracker.get_value(), about_point=ORIGIN)
            return arrow

        return always_redraw(make_arrow)

    def _create_axis_label(self, arrow: Arrow):
        """创建箭头标签（智能跟随箭头方向）

        Args:
            arrow: 箭头对象

        Returns:
            动态跟随的标签
        """
        def make_label():
            # 计算箭头方向向量
            arrow_dir = arrow.get_end() - arrow.get_start()
            # 归一化
            if np.linalg.norm(arrow_dir) > 0.01:
                arrow_dir = arrow_dir / np.linalg.norm(arrow_dir)
            else:
                arrow_dir = RIGHT

            # 标签沿箭头方向偏移，避免和能量计量器碰撞
            label = themed_text("u", font_size=32, color=PRIMARY_RED)
            label.next_to(arrow.get_end(), arrow_dir, buff=0.2)
            return label

        return always_redraw(make_label)

    def _build_question_card(self) -> VGroup:
        """创建问题卡片

        Returns:
            问题卡片 VGroup
        """
        # 进一步缩小尺寸避免冲突
        card = RoundedRectangle(
            width=4.6,
            height=1.5,
            corner_radius=0.2,
            stroke_color=PRIMARY_RED,
            stroke_width=2.5,
        )
        card.set_fill(color="#050C1D", opacity=0.85)

        # 使用两行分别创建，避免换行符问题
        line1 = themed_text("为什么约束问题", font_size=26, color=TEXT_COLOR)
        line2 = themed_text("等价为特征值问题？", font_size=26, color=TEXT_COLOR)
        prompt = VGroup(line1, line2).arrange(DOWN, buff=0.15)
        prompt.move_to(card.get_center())

        group = VGroup(card, prompt)
        # 调整位置：更靠下，避免和能量提示重叠
        group.to_corner(DL).shift(UP * 0.5 + RIGHT * 0.3)
        return group
