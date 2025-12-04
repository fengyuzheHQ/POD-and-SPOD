"""拉格朗日乘子法动画 - 工具函数

包含梯度计算、路径插值、数值计算等辅助函数
"""

from typing import Callable
import numpy as np


# ============ 梯度计算 ============

def gaussian_gradient(x: float, y: float, center: tuple[float, float] = (0, 0),
                     sigma_x: float = 3.0, sigma_y: float = 2.0,
                     amplitude: float = 0.8) -> np.ndarray:
    """计算高斯函数的梯度

    函数形式: f(x,y) = A * exp(-(x-cx)²/(2σx²) - (y-cy)²/(2σy²))
    梯度: ∇f = [∂f/∂x, ∂f/∂y]

    Args:
        x, y: 计算点坐标
        center: 高斯中心 (cx, cy)
        sigma_x, sigma_y: 标准差
        amplitude: 振幅

    Returns:
        梯度向量 [grad_x, grad_y]
    """
    cx, cy = center
    dx = x - cx
    dy = y - cy

    # 高斯函数值
    exp_term = np.exp(-(dx**2 / (2 * sigma_x**2) + dy**2 / (2 * sigma_y**2)))
    f_val = amplitude * exp_term

    # 梯度
    grad_x = -f_val * dx / (sigma_x**2)
    grad_y = -f_val * dy / (sigma_y**2)

    return np.array([grad_x, grad_y, 0.0])  # 添加 z=0 以兼容 3D


def composite_gradient(x: float, y: float) -> np.ndarray:
    """复合地形的梯度 (用于 Scene 2/3)

    组合多个高斯函数和正弦波
    """
    # 主高斯峰
    grad1 = gaussian_gradient(x, y, center=(0, 0), sigma_x=3.0, sigma_y=2.0, amplitude=0.8)

    # 次要起伏 (正弦波的梯度)
    sin_term = 0.4 * np.sin(0.8 * x) * np.cos(0.6 * y)
    grad_sin_x = 0.4 * 0.8 * np.cos(0.8 * x) * np.cos(0.6 * y)
    grad_sin_y = -0.4 * 0.6 * np.sin(0.8 * x) * np.sin(0.6 * y)

    return grad1 + np.array([grad_sin_x, grad_sin_y, 0.0])


def normalize_vector(v: np.ndarray, epsilon: float = 1e-8) -> np.ndarray:
    """归一化向量 (避免除零)

    Args:
        v: 输入向量
        epsilon: 避免除零的小量

    Returns:
        归一化后的向量
    """
    norm = np.linalg.norm(v)
    if norm < epsilon:
        return v
    return v / norm


def path_normal_2d(tangent: np.ndarray) -> np.ndarray:
    """计算 2D 路径的法向量

    Args:
        tangent: 切向量 [tx, ty, 0]

    Returns:
        法向量 (逆时针旋转 90°)
    """
    tx, ty = tangent[0], tangent[1]
    return np.array([-ty, tx, 0.0])


# ============ 路径插值 ============

def lerp_path(path_a: Callable[[float], np.ndarray],
              path_b: Callable[[float], np.ndarray],
              alpha: float) -> Callable[[float], np.ndarray]:
    """线性插值两条参数化路径

    Args:
        path_a: 起始路径函数 t -> [x, y, z]
        path_b: 目标路径函数 t -> [x, y, z]
        alpha: 插值参数 [0, 1]

    Returns:
        插值后的路径函数
    """
    def interpolated_path(t: float) -> np.ndarray:
        point_a = path_a(t)
        point_b = path_b(t)
        return (1 - alpha) * point_a + alpha * point_b

    return interpolated_path


def smooth_step(t: float, edge0: float = 0.0, edge1: float = 1.0) -> float:
    """平滑阶跃函数 (Hermite 插值)

    Args:
        t: 输入值
        edge0, edge1: 边界值

    Returns:
        平滑插值结果 [0, 1]
    """
    t = np.clip((t - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ============ 矩阵插值 (用于 Scene 5 等高线变形) ============

def lerp_matrix(mat_a: np.ndarray, mat_b: np.ndarray, alpha: float) -> np.ndarray:
    """线性插值两个矩阵

    用于等高线变形: Q(α) = (1-α)Q_start + αQ_end

    Args:
        mat_a: 起始矩阵
        mat_b: 目标矩阵
        alpha: 插值参数

    Returns:
        插值后的矩阵
    """
    return (1 - alpha) * mat_a + alpha * mat_b


# ============ 数值微分 (用于向量场) ============

def numerical_gradient_2d(func: Callable[[float, float], float],
                         x: float, y: float,
                         h: float = 0.01) -> np.ndarray:
    """数值梯度计算 (中心差分)

    Args:
        func: 标量函数 f(x, y)
        x, y: 计算点
        h: 步长

    Returns:
        梯度向量 [∂f/∂x, ∂f/∂y, 0]
    """
    grad_x = (func(x + h, y) - func(x - h, y)) / (2 * h)
    grad_y = (func(x, y + h) - func(x, y - h)) / (2 * h)
    return np.array([grad_x, grad_y, 0.0])
