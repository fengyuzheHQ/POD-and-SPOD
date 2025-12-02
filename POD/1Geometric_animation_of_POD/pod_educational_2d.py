# -*- coding: utf-8 -*-
"""
POD Educational Animation - 2D Part
2D场景: 数据引入、能量搜索、正交约束、数学公式
"""
from manim import *
import numpy as np
import platform

class PODEducational2D(Scene):
    def construct(self):
        self.setup_fonts()

        # 场景1: 物理实验引入
        self.scene1_introduction()

        # 场景2: 2D能量搜索
        self.scene2_energy_search()

        # 场景3: Mode 2正交约束
        self.scene3_orthogonal_mode2()

        # 场景4: 数学公式讲解
        self.scene4_mathematical_formulation()

    def setup_fonts(self):
        """配置中文字体"""
        sys_str = platform.system()
        if sys_str == "Windows":
            self.CN_FONT = "Microsoft YaHei"
        elif sys_str == "Darwin":
            self.CN_FONT = "PingFang SC"
        else:
            self.CN_FONT = "sans-serif"

    def scene1_introduction(self):
        """场景1: 从物理实验引入"""
        # 主标题
        title = Text("POD: 寻找数据的本质方向", font=self.CN_FONT, font_size=48, color=YELLOW)
        subtitle = Text("Proper Orthogonal Decomposition", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN)

        title_group = VGroup(title, subtitle)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(1)
        self.play(title_group.animate.to_edge(UP).scale(0.6))

        # 物理实验场景描述
        exp_text = Text(
            "场景: 物理实验中的两个传感器",
            font=self.CN_FONT,
            font_size=32
        ).shift(UP * 2)

        sensor_labels = VGroup(
            Text("传感器A（温度）", font=self.CN_FONT, font_size=24, color=BLUE),
            Text("传感器B（压力）", font=self.CN_FONT, font_size=24, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(exp_text, DOWN, buff=0.5)

        self.play(FadeIn(exp_text), run_time=1)
        self.play(Write(sensor_labels), run_time=1.5)
        self.wait(1.5)

        # 生成数据点云
        data_text = Text("采集100个数据点...", font=self.CN_FONT, font_size=28, color=TEAL)
        data_text.next_to(sensor_labels, DOWN, buff=0.8)
        self.play(Write(data_text))

        # 创建坐标系
        self.axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": GRAY, "stroke_width": 2},
            tips=False
        )

        x_label = Text("传感器A", font=self.CN_FONT, font_size=20).next_to(self.axes.x_axis, RIGHT)
        y_label = Text("传感器B", font=self.CN_FONT, font_size=20).next_to(self.axes.y_axis, UP)

        axes_group = VGroup(self.axes, x_label, y_label).scale(0.8).shift(DOWN * 0.5)

        self.play(
            FadeOut(exp_text),
            FadeOut(sensor_labels),
            FadeOut(data_text),
            FadeOut(title_group),
            run_time=0.8
        )
        self.play(Create(self.axes), Write(x_label), Write(y_label), run_time=1.5)

        # 生成椭圆点云
        np.random.seed(42)
        cov_matrix = [[2.5, 2.0], [2.0, 2.5]]
        self.data_points = np.random.multivariate_normal([0, 0], cov_matrix, 100)

        self.dots = VGroup(*[
            Dot(self.axes.c2p(x, y), color=BLUE_C, radius=0.06, fill_opacity=0.7)
            for x, y in self.data_points
        ])

        self.play(
            LaggedStart(*[FadeIn(dot) for dot in self.dots], lag_ratio=0.02),
            run_time=2
        )

        # 观察说明
        observation = Text(
            "数据呈椭圆形分布，传统X-Y轴并非最佳描述",
            font=self.CN_FONT,
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN)

        self.play(Write(observation))
        self.wait(2)
        self.play(FadeOut(observation), FadeOut(x_label), FadeOut(y_label))

        # 保存当前状态
        self.current_axes = axes_group

    def scene2_energy_search(self):
        """场景2: 2D能量搜索与可视化"""
        # 引入POD思想
        pod_intro = Text(
            "POD的核心思想：找到能量最大的方向",
            font=self.CN_FONT,
            font_size=32,
            color=YELLOW
        ).to_edge(UP)

        self.play(Write(pod_intro))
        self.wait(1.5)

        # 创建扫描向量
        self.theta_tracker = ValueTracker(0)

        # 创建扫描向量组件
        scan_line = Line(ORIGIN, ORIGIN, color=YELLOW, stroke_width=3, stroke_opacity=0.5)
        scan_arrow = Arrow(ORIGIN, ORIGIN, color=YELLOW, buff=0, stroke_width=5)
        scan_label = MathTex(r"\phi", color=YELLOW, font_size=36)

        def update_scan_vector(mob):
            angle = self.theta_tracker.get_value()
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            start_point = self.axes.c2p(-3.5 * direction[0], -3.5 * direction[1])
            end_point = self.axes.c2p(3.5 * direction[0], 3.5 * direction[1])
            arrow_end = self.axes.c2p(2.5 * direction[0], 2.5 * direction[1])
            label_pos = self.axes.c2p(3 * direction[0], 3 * direction[1])

            scan_line.put_start_and_end_on(start_point, end_point)
            scan_arrow.put_start_and_end_on(self.axes.c2p(0, 0), arrow_end)
            scan_label.move_to(label_pos)

        scan_line.add_updater(lambda m: update_scan_vector(m))
        scan_vector = VGroup(scan_line, scan_arrow, scan_label)

        # 投影线
        projection_lines = VGroup(*[
            DashedLine(ORIGIN, ORIGIN, color=ORANGE, stroke_width=1.5, stroke_opacity=0.4)
            for _ in self.data_points
        ])

        def update_projections(mob, dt=0):
            angle = self.theta_tracker.get_value()
            v_dir = np.array([np.cos(angle), np.sin(angle)])

            for line, (x, y) in zip(mob, self.data_points):
                point_orig = self.axes.c2p(x, y)
                proj_length = np.dot([x, y], v_dir)
                point_proj = self.axes.c2p(proj_length * v_dir[0], proj_length * v_dir[1])
                line.put_start_and_end_on(point_orig, point_proj)

        projection_lines.add_updater(update_projections)

        # 能量计算和显示
        energy_label = Text("投影能量 E:", font=self.CN_FONT, font_size=28, color=ORANGE)
        energy_label.to_corner(UR).shift(DOWN * 1.5 + LEFT * 0.5)

        energy_value = DecimalNumber(0, num_decimal_places=1, font_size=40, color=RED)
        energy_value.next_to(energy_label, DOWN)

        def update_energy(mob, dt=0):
            angle = self.theta_tracker.get_value()
            direction = np.array([np.cos(angle), np.sin(angle)])
            energy = float(np.sum((self.data_points @ direction) ** 2))
            mob.set_value(energy)

        energy_value.add_updater(update_energy)

        # 能量公式
        energy_formula = MathTex(
            r"E = \sum_{i=1}^{n} |\mathbf{u}_i \cdot \boldsymbol{\phi}|^2",
            font_size=32
        ).next_to(energy_value, DOWN, buff=0.5)

        formula_explanation = VGroup(
            Text("u: 数据点", font=self.CN_FONT, font_size=20, color=BLUE_C),
            Text("φ: 扫描方向", font=self.CN_FONT, font_size=20, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(energy_formula, DOWN, buff=0.3)

        # 显示扫描向量和公式
        self.play(Create(scan_vector), run_time=1)
        self.add(projection_lines)
        self.play(
            Write(energy_label),
            Write(energy_value),
            Write(energy_formula),
            Write(formula_explanation),
            run_time=2
        )

        self.wait(1)

        # 开始旋转搜索
        search_text = Text(
            "旋转搜索最大能量方向...",
            font=self.CN_FONT,
            font_size=24,
            color=TEAL
        ).next_to(pod_intro, DOWN)

        self.play(FadeIn(search_text))

        # 慢速旋转一圈展示能量变化
        self.play(
            self.theta_tracker.animate.set_value(2 * PI),
            run_time=6,
            rate_func=linear
        )

        self.wait(0.5)

        # 快速定位到最大值（约45度）
        max_angle = np.pi / 4
        self.play(
            self.theta_tracker.animate.set_value(max_angle),
            run_time=1.5,
            rate_func=smooth
        )

        # 锁定Mode 1
        found_text = Text(
            "找到了！第一模态 (Mode 1)",
            font=self.CN_FONT,
            font_size=32,
            color=GREEN
        ).move_to(search_text)

        self.play(
            FadeOut(search_text),
            Write(found_text),
            scan_vector.animate.set_color(GREEN),
            run_time=1.5
        )

        self.wait(2)

        # 清理并保存状态
        scan_line.clear_updaters()
        projection_lines.clear_updaters()
        energy_value.clear_updaters()
        self.remove(projection_lines)

        # 创建锁定的Mode 1向量
        direction = np.array([np.cos(max_angle), np.sin(max_angle), 0])
        mode1_line = Line(
            self.axes.c2p(-3.5 * direction[0], -3.5 * direction[1]),
            self.axes.c2p(3.5 * direction[0], 3.5 * direction[1]),
            color=GREEN, stroke_width=3, stroke_opacity=0.5
        )
        mode1_arrow = Arrow(
            self.axes.c2p(0, 0),
            self.axes.c2p(2.5 * direction[0], 2.5 * direction[1]),
            color=GREEN, buff=0, stroke_width=5
        )
        mode1_label = MathTex(r"\phi_1", color=GREEN, font_size=36)
        mode1_label.move_to(self.axes.c2p(3 * direction[0], 3 * direction[1]))

        self.mode1_vector = VGroup(mode1_line, mode1_arrow, mode1_label)
        self.mode1_angle = max_angle
        self.remove(scan_vector)
        self.add(self.mode1_vector)

        self.play(
            FadeOut(pod_intro),
            FadeOut(found_text),
            FadeOut(energy_label),
            FadeOut(energy_value),
            FadeOut(energy_formula),
            FadeOut(formula_explanation)
        )

    def scene3_orthogonal_mode2(self):
        """场景3: Mode 2的正交约束"""
        # 标题
        ortho_title = Text(
            "第二模态必须正交于第一模态",
            font=self.CN_FONT,
            font_size=32,
            color=YELLOW
        ).to_edge(UP)

        self.play(Write(ortho_title))
        self.wait(1)

        # 正交约束说明
        constraint_text = Text(
            "约束条件: φ₁ ⊥ φ₂",
            font=self.CN_FONT,
            font_size=28,
            color=ORANGE
        ).to_corner(UR).shift(DOWN)

        self.play(Write(constraint_text))

        # 生成Mode 2（垂直于Mode 1）
        mode2_angle = self.mode1_angle + PI / 2
        v2_dir = np.array([np.cos(mode2_angle), np.sin(mode2_angle)])

        mode2_line = Line(
            self.axes.c2p(-3 * v2_dir[0], -3 * v2_dir[1]),
            self.axes.c2p(3 * v2_dir[0], 3 * v2_dir[1]),
            color=RED,
            stroke_width=3,
            stroke_opacity=0.5
        )

        mode2_arrow = Arrow(
            self.axes.c2p(0, 0),
            self.axes.c2p(2.5 * v2_dir[0], 2.5 * v2_dir[1]),
            color=RED,
            buff=0,
            stroke_width=5
        )

        mode2_label = MathTex(r"\phi_2", color=RED, font_size=36)
        mode2_label.next_to(mode2_arrow, LEFT if v2_dir[0] < 0 else RIGHT)

        self.mode2_vector = VGroup(mode2_line, mode2_arrow, mode2_label)

        self.play(Create(self.mode2_vector), run_time=2)

        # 显示直角标记
        right_angle = RightAngle(
            Line(ORIGIN, RIGHT),
            Line(ORIGIN, UP),
            length=0.3,
            color=WHITE
        )
        right_angle.move_to(self.axes.c2p(0, 0)).rotate(self.mode1_angle)

        self.play(Create(right_angle))

        # 添加Mode标签
        mode1_label = Text("Mode 1 (最大能量)", font=self.CN_FONT, font_size=24, color=GREEN)
        mode2_label_text = Text("Mode 2 (次大能量)", font=self.CN_FONT, font_size=24, color=RED)

        labels = VGroup(mode1_label, mode2_label_text).arrange(DOWN, aligned_edge=LEFT)
        labels.to_corner(UL).shift(DOWN * 2 + RIGHT * 0.5)

        self.play(Write(labels))
        self.wait(2)

        # 清理
        self.play(
            FadeOut(ortho_title),
            FadeOut(constraint_text),
            FadeOut(labels),
            FadeOut(right_angle)
        )

    def scene4_mathematical_formulation(self):
        """场景4: 数学公式详解"""
        # 清空屏幕，只保留核心元素
        self.play(
            FadeOut(self.dots),
            FadeOut(self.axes),
            FadeOut(self.mode1_vector),
            FadeOut(self.mode2_vector)
        )

        # 标题
        math_title = Text(
            "POD的数学本质",
            font=self.CN_FONT,
            font_size=40,
            color=YELLOW
        ).to_edge(UP)

        self.play(Write(math_title))
        self.wait(1)

        # 步骤1: 数据矩阵
        step1_title = Text("步骤1: 构建数据矩阵", font=self.CN_FONT, font_size=28, color=BLUE)
        step1_title.shift(UP * 2)

        data_matrix = MathTex(
            r"\mathbf{A} = [\mathbf{u}_1, \mathbf{u}_2, \dots, \mathbf{u}_n]",
            font_size=36
        ).next_to(step1_title, DOWN, buff=0.5)

        data_explain = Text(
            "每列是一个数据点",
            font=self.CN_FONT,
            font_size=22,
            color=GRAY
        ).next_to(data_matrix, DOWN)

        self.play(Write(step1_title))
        self.play(Write(data_matrix), Write(data_explain))
        self.wait(2)

        # 步骤2: 协方差矩阵
        step2_title = Text("步骤2: 计算协方差矩阵", font=self.CN_FONT, font_size=28, color=BLUE)
        step2_title.move_to(step1_title)

        cov_matrix = MathTex(
            r"\mathbf{C} = \mathbf{A}\mathbf{A}^T = \sum_{i=1}^{n} \mathbf{u}_i \mathbf{u}_i^T",
            font_size=36
        ).next_to(step2_title, DOWN, buff=0.5)

        cov_explain = Text(
            "描述数据在各方向上的分布",
            font=self.CN_FONT,
            font_size=22,
            color=GRAY
        ).next_to(cov_matrix, DOWN)

        self.play(
            Transform(step1_title, step2_title),
            Transform(data_matrix, cov_matrix),
            Transform(data_explain, cov_explain)
        )
        self.wait(2)

        # 步骤3: 特征值分解
        step3_title = Text("步骤3: 特征值分解", font=self.CN_FONT, font_size=28, color=BLUE)
        step3_title.move_to(step1_title)

        eigen_eq = MathTex(
            r"\mathbf{C}\boldsymbol{\phi}_i = \lambda_i \boldsymbol{\phi}_i",
            font_size=40
        ).next_to(step3_title, DOWN, buff=0.5)

        eigen_parts = VGroup(
            MathTex(r"\boldsymbol{\phi}_i:", font_size=28).set_color(YELLOW),
            Text(" 第i个模态（特征向量）", font=self.CN_FONT, font_size=24),
            MathTex(r"\lambda_i:", font_size=28).set_color(RED),
            Text(" 该模态的能量（特征值）", font=self.CN_FONT, font_size=24)
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3))
        eigen_parts.next_to(eigen_eq, DOWN, buff=0.8)

        self.play(
            Transform(step1_title, step3_title),
            Transform(data_matrix, eigen_eq),
            FadeOut(data_explain)
        )
        self.play(Write(eigen_parts))
        self.wait(2)

        # 排序说明
        sort_box = SurroundingRectangle(eigen_eq, color=YELLOW, buff=0.2)
        sort_text = Text(
            "按能量降序: λ₁ > λ₂ > λ₃ > ...",
            font=self.CN_FONT,
            font_size=28,
            color=GREEN
        ).next_to(sort_box, DOWN, buff=0.5)

        self.play(Create(sort_box))
        self.play(Write(sort_text))
        self.wait(3)

        # 结束提示
        end_text = Text(
            "2D 部分完成！接下来观看 3D 扩展...",
            font=self.CN_FONT,
            font_size=32,
            color=TEAL
        ).to_edge(DOWN)

        self.play(Write(end_text))
        self.wait(2)

        # 清理
        self.play(
            *[FadeOut(mob) for mob in [
                math_title, step1_title, data_matrix,
                eigen_parts, sort_box, sort_text, end_text
            ]]
        )
