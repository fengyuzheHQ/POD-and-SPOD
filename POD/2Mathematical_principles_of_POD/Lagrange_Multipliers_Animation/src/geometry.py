"""拉格朗日乘子法动画 - 几何对象定义

包含约束路径、等高线、3D 曲面等几何对象的参数化定义
"""

from typing import Callable
import numpy as np
from manim import ParametricFunction, ImplicitFunction, ParametricSurface, ValueTracker


# ============ 约束路径定义 ============

def wavy_ellipse_path(scale: float = 1.0, wave_amplitude: float = 0.3) -> Callable[[float], np.ndarray]:
    """波浪椭圆路径 (用于 Scene 2/3)

    Args:
        scale: 椭圆缩放
        wave_amplitude: 波浪幅度

    Returns:
        参数化路径函数 t -> [x, y, 0]
    """
    def path(t: float) -> np.ndarray:
        # 基础椭圆
        x = scale * 3.0 * np.cos(t)
        y = scale * 1.8 * np.sin(t)

        # 添加波浪扰动
        x += wave_amplitude * np.sin(3 * t)
        y += wave_amplitude * np.cos(2 * t)

        return np.array([x, y, 0.0])

    return path


def perfect_circle_path(radius: float = 2.5) -> Callable[[float], np.ndarray]:
    """完美圆形路径 (用于 Scene 5 变形目标)

    Args:
        radius: 圆半径

    Returns:
        参数化路径函数 t -> [x, y, 0]
    """
    def path(t: float) -> np.ndarray:
        x = radius * np.cos(t)
        y = radius * np.sin(t)
        return np.array([x, y, 0.0])

    return path


def create_morphing_path(tracker: ValueTracker,
                        path_start: Callable[[float], np.ndarray],
                        path_end: Callable[[float], np.ndarray]) -> Callable[[float], np.ndarray]:
    """创建可变形的路径

    Args:
        tracker: 插值参数 ValueTracker (0 -> 1)
        path_start: 起始路径
        path_end: 目标路径

    Returns:
        插值路径函数
    """
    def morphing_path(t: float) -> np.ndarray:
        alpha = tracker.get_value()
        point_start = path_start(t)
        point_end = path_end(t)
        return (1 - alpha) * point_start + alpha * point_end

    return morphing_path


# ============ 3D 曲面定义 ============

def abstract_landscape_surface(u_range: tuple = (-4, 4), v_range: tuple = (-3, 3)) -> ParametricSurface:
    """抽象数学地形曲面 (用于 Scene 2)

    组合高斯峰和正弦波，创建有趣的 3D 地形

    Args:
        u_range: u 参数范围
        v_range: v 参数范围

    Returns:
        ParametricSurface 对象
    """
    def surface_func(u: float, v: float) -> np.ndarray:
        x = u
        y = v

        # 主高斯峰
        z_gaussian = 0.8 * np.exp(-(u**2 / 9 + v**2 / 4))

        # 正弦波起伏
        z_wave = 0.4 * np.sin(0.8 * u) * np.cos(0.6 * v)

        z = z_gaussian + z_wave

        return np.array([x, y, z])

    return ParametricSurface(
        surface_func,
        u_range=u_range,
        v_range=v_range,
        resolution=(30, 30),
    )


def project_path_to_surface(path_2d: Callable[[float], np.ndarray],
                           surface_func: Callable[[float, float], float]) -> Callable[[float], np.ndarray]:
    """将 2D 路径投影到 3D 曲面

    Args:
        path_2d: 2D 路径函数 t -> [x, y, 0]
        surface_func: 曲面高度函数 (x, y) -> z

    Returns:
        3D 路径函数 t -> [x, y, z]
    """
    def path_3d(t: float) -> np.ndarray:
        point_2d = path_2d(t)
        x, y = point_2d[0], point_2d[1]
        z = surface_func(x, y)
        return np.array([x, y, z])

    return path_3d


# ============ 等高线定义 ============

def gaussian_level_set(level: float, sigma_x: float = 3.0, sigma_y: float = 2.0,
                      amplitude: float = 0.8) -> Callable[[float, float], float]:
    """高斯函数的等高线

    Args:
        level: 等高线值
        sigma_x, sigma_y: 标准差
        amplitude: 振幅

    Returns:
        隐式函数 f(x, y) = level
    """
    def implicit_func(x: float, y: float) -> float:
        z = amplitude * np.exp(-(x**2 / (2 * sigma_x**2) + y**2 / (2 * sigma_y**2)))
        return z - level

    return implicit_func


def quadratic_form_level_set(matrix: np.ndarray, level: float = 1.0) -> Callable[[float, float], float]:
    """二次型等高线: x^T Q x = level

    用于 POD 能量椭圆等高线

    Args:
        matrix: 2x2 对称矩阵 Q
        level: 等高线值

    Returns:
        隐式函数
    """
    def implicit_func(x: float, y: float) -> float:
        vec = np.array([x, y])
        value = vec @ matrix @ vec
        return value - level

    return implicit_func


def create_pod_covariance_matrix(theta: float, lambda1: float = 4.0, lambda2: float = 1.0) -> np.ndarray:
    """创建 POD 协方差矩阵

    C = R(θ) Λ R(θ)^T，其中 Λ = diag(λ1, λ2)

    Args:
        theta: 主轴角度
        lambda1, lambda2: 特征值

    Returns:
        2x2 协方差矩阵
    """
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    # 旋转矩阵
    R = np.array([
        [cos_t, -sin_t],
        [sin_t, cos_t]
    ])

    # 特征值矩阵
    Lambda = np.diag([lambda1, lambda2])

    # C = R Λ R^T
    return R @ Lambda @ R.T


# ============ 等高线集合生成 ============

def generate_contour_levels(func: Callable[[float, float], float],
                           x_range: tuple = (-4, 4),
                           y_range: tuple = (-3, 3),
                           num_levels: int = 8,
                           z_min: float = 0.1,
                           z_max: float = 0.8) -> list[float]:
    """生成等高线的高度值

    Args:
        func: 标量函数 f(x, y)
        x_range, y_range: 计算范围
        num_levels: 等高线数量
        z_min, z_max: 高度范围

    Returns:
        等高线高度值列表
    """
    return np.linspace(z_min, z_max, num_levels).tolist()
