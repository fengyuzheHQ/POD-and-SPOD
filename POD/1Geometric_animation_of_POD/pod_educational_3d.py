# -*- coding: utf-8 -*-
"""
POD Educational Animation - 3D Part
3D场景: 3D扩展和总结
"""
from manim import *

try:
    from manim.scene.three_d_scene import ThreeDScene
except ImportError:
    try:
        from manimlib.scene.three_d_scene import ThreeDScene
    except ImportError as exc:
        raise ImportError(
            "ThreeDScene is unavailable in the current Manim installation. "
            "Please install Manim Community Edition with 3D support."
        ) from exc

import numpy as np
import platform

class PODEducational3D(ThreeDScene):
    def construct(self):
        self.setup_fonts()

        # 场景5: 3D扩展
        self.scene5_3d_extension()

        # 场景6: 总结
        self.scene6_conclusion()

    def setup_fonts(self):
        """配置中文字体"""
        sys_str = platform.system()
        if sys_str == "Windows":
            self.CN_FONT = "Microsoft YaHei"
        elif sys_str == "Darwin":
            self.CN_FONT = "PingFang SC"
        else:
            self.CN_FONT = "sans-serif"

    def scene5_3d_extension(self):
        """场景5: 3D空间的详细演示"""
        # 标题
        title_3d = Text(
            "从2D到3D的扩展",
            font=self.CN_FONT,
            font_size=36,
            color=YELLOW
        ).to_edge(UP)

        self.add_fixed_in_frame_mobjects(title_3d)
        self.play(Write(title_3d))
        self.wait(1)

        # 设置3D相机
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        # 创建3D坐标系
        axes_3d = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"color": GRAY}
        )

        self.play(Create(axes_3d), run_time=2)
        self.wait(1)

        # 生成3D椭球点云
        np.random.seed(123)
        cov_3d = [
            [3.0, 2.5, 0.5],
            [2.5, 3.0, 0.5],
            [0.5, 0.5, 1.0]
        ]
        data_3d = np.random.multivariate_normal([0, 0, 0], cov_3d, 150)

        dots_3d = VGroup(*[
            Dot3D(point=axes_3d.c2p(x, y, z), color=BLUE_C, radius=0.05)
            for x, y, z in data_3d
        ])

        cloud_label = Text(
            "3D数据点云",
            font=self.CN_FONT,
            font_size=24,
            color=BLUE_C
        ).to_corner(UL).shift(DOWN * 2)
        self.add_fixed_in_frame_mobjects(cloud_label)

        self.play(
            LaggedStart(*[FadeIn(dot) for dot in dots_3d], lag_ratio=0.01),
            Write(cloud_label),
            run_time=2.5
        )
        self.wait(1)

        # 计算真实的POD模态（基于协方差矩阵）
        cov_3d_matrix = np.cov(data_3d.T)
        eigvals, eigvecs = np.linalg.eigh(cov_3d_matrix)

        # 按特征值降序排列
        order = np.argsort(eigvals)[::-1]
        eigvals = eigvals[order]
        eigvecs = eigvecs[:, order]

        # 提取三个主模态
        v1_dir = eigvecs[:, 0]
        v2_dir = eigvecs[:, 1]
        v3_dir = eigvecs[:, 2]

        # 能量占比
        total_energy = np.sum(eigvals)
        energy_ratios = eigvals / total_energy

        # Mode 1: 主方向
        energy_text = Text(
            f"计算数据的协方差矩阵...",
            font=self.CN_FONT,
            font_size=24,
            color=YELLOW
        ).to_corner(UR).shift(DOWN)
        self.add_fixed_in_frame_mobjects(energy_text)
        self.play(Write(energy_text))
        self.wait(1.5)

        mode1_3d = Arrow3D(
            start=ORIGIN,
            end=v1_dir * 3,
            color=GREEN,
            resolution=20,
            thickness=0.02
        )

        mode1_text = Text(
            f"Mode 1: {energy_ratios[0]*100:.1f}% 能量",
            font=self.CN_FONT,
            font_size=24,
            color=GREEN
        ).move_to(energy_text)
        self.add_fixed_in_frame_mobjects(mode1_text)

        self.play(
            FadeOut(energy_text),
            GrowFromPoint(mode1_3d, mode1_3d.get_start()),
            Write(mode1_text)
        )
        self.remove_fixed_in_frame_mobjects(energy_text)
        self.wait(1.5)

        # 显示正交平面
        plane_desc = Text(
            "在正交空间中搜索Mode 2...",
            font=self.CN_FONT,
            font_size=22,
            color=YELLOW
        ).next_to(mode1_text, DOWN)
        self.add_fixed_in_frame_mobjects(plane_desc)
        self.play(Write(plane_desc))

        # 构建正交平面（使用Mode 2和Mode 3张成的空间）
        plane_corners = [
            2.5 * v2_dir + 2.5 * v3_dir,
            -2.5 * v2_dir + 2.5 * v3_dir,
            -2.5 * v2_dir - 2.5 * v3_dir,
            2.5 * v2_dir - 2.5 * v3_dir
        ]

        ortho_plane = Polygon(
            *plane_corners,
            color=BLUE,
            stroke_width=1,
            fill_color=BLUE,
            fill_opacity=0.3
        )
        ortho_plane.set_shade_in_3d(True)

        self.play(DrawBorderThenFill(ortho_plane))
        self.wait(1.5)

        # Mode 2
        mode2_3d = Arrow3D(
            start=ORIGIN,
            end=v2_dir * 2.5,
            color=RED,
            resolution=20,
            thickness=0.02
        )

        mode2_text = Text(
            f"Mode 2: {energy_ratios[1]*100:.1f}% 能量",
            font=self.CN_FONT,
            font_size=24,
            color=RED
        ).next_to(mode1_text, DOWN, buff=1.5)
        self.add_fixed_in_frame_mobjects(mode2_text)

        self.play(
            FadeOut(plane_desc),
            GrowFromPoint(mode2_3d, mode2_3d.get_start()),
            Write(mode2_text)
        )
        self.remove_fixed_in_frame_mobjects(plane_desc)
        self.wait(1)

        # Mode 3
        mode3_desc = Text(
            f"Mode 3: {energy_ratios[2]*100:.1f}% 能量",
            font=self.CN_FONT,
            font_size=22,
            color=ORANGE
        ).next_to(mode2_text, DOWN)
        self.add_fixed_in_frame_mobjects(mode3_desc)

        mode3_3d = Arrow3D(
            start=ORIGIN,
            end=v3_dir * 2.0,
            color=ORANGE,
            resolution=20,
            thickness=0.02
        )

        self.play(
            FadeOut(ortho_plane),
            GrowFromPoint(mode3_3d, mode3_3d.get_start()),
            Write(mode3_desc)
        )
        self.wait(1)

        # 相机旋转展示
        rotate_text = Text(
            "三个模态两两正交",
            font=self.CN_FONT,
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(rotate_text)
        self.play(Write(rotate_text))

        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        # 清理
        cleanup_mobjects = [
            dots_3d, axes_3d, mode1_3d, mode2_3d, mode3_3d,
            title_3d, cloud_label, mode1_text, mode2_text,
            mode3_desc, rotate_text
        ]
        self.play(
            *[FadeOut(mob) for mob in cleanup_mobjects],
            run_time=1.5
        )
        # 移除所有固定帧对象
        self.remove_fixed_in_frame_mobjects(
            title_3d, cloud_label, mode1_text, mode2_text,
            mode3_desc, rotate_text
        )

    def scene6_conclusion(self):
        """场景6: 总结"""
        # 重置相机到2D
        self.move_camera(phi=0, theta=-90 * DEGREES)

        # 总结标题
        conclusion_title = Text(
            "POD的核心要点",
            font=self.CN_FONT,
            font_size=48,
            color=YELLOW
        ).to_edge(UP)

        self.add_fixed_in_frame_mobjects(conclusion_title)
        self.play(Write(conclusion_title))
        self.wait(1)

        # 要点列表
        points = VGroup(
            Text("1. 按能量从大到小排序", font=self.CN_FONT, font_size=32, color=GREEN),
            Text("2. 所有模态两两正交", font=self.CN_FONT, font_size=32, color=RED),
            Text("3. 用最少的维度捕获最多的信息", font=self.CN_FONT, font_size=32, color=BLUE),
            Text("4. 本质是协方差矩阵的特征值分解", font=self.CN_FONT, font_size=32, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6)

        self.add_fixed_in_frame_mobjects(points)
        self.play(
            LaggedStart(*[FadeIn(point, shift=RIGHT) for point in points], lag_ratio=0.4),
            run_time=4
        )
        self.wait(2)

        # 最终总结
        final_summary = Text(
            "POD = 数据的最优正交坐标系",
            font=self.CN_FONT,
            font_size=40,
            color=YELLOW
        ).to_edge(DOWN)

        self.add_fixed_in_frame_mobjects(final_summary)
        self.play(Write(final_summary))
        self.wait(3)

        # 结束
        self.play(
            *[FadeOut(mob) for mob in [conclusion_title, points, final_summary]],
            run_time=2
        )
        self.wait(1)
