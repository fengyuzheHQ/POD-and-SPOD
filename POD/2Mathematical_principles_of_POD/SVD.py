import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 定义我们的矩阵 A
A = np.array([
    [1, 2],
    [3, 4],
    [5, 6]
])

# 使用 numpy 的 linalg.svd 函数进行分解
# U: 3x3 正交矩阵
# s: 包含奇异值的 1D 数组 (注意，不是完整的 Sigma 矩阵)
# Vt: 2x2 正交矩阵的转置
U, s, Vt = np.linalg.svd(A)

# 为了进行矩阵乘法，我们需要将 1D 数组 s 构造成完整的 Sigma 矩阵
# Sigma 矩阵的形状应该和 A 矩阵一样，是 3x2
Sigma = np.zeros(A.shape)
Sigma[:2, :2] = np.diag(s) # s 有 2 个元素，所以填充到 2x2 的对角线上

print("矩阵 U (输出空间的旋转):\n", U)
print("\n矩阵 Sigma (拉伸):\n", Sigma)
print("\n矩阵 V^T (输入空间的旋转):\n", Vt)

# 验证一下：U @ Sigma @ Vt 是否等于 A
A_reconstructed = U @ Sigma @ Vt
print("\n重构的矩阵 A:\n", A_reconstructed)
print("\n重构是否成功:", np.allclose(A, A_reconstructed))
# --- 可视化设置 ---
fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(1, 4, 1, aspect='equal')
ax2 = fig.add_subplot(1, 4, 2, aspect='equal')
ax3 = fig.add_subplot(1, 4, 3, projection='3d')
ax4 = fig.add_subplot(1, 4, 4, projection='3d')

# 1. 原始输入空间：一个单位圆
theta = np.linspace(0, 2*np.pi, 100)
points_original = np.vstack([np.cos(theta), np.sin(theta)])
ax1.plot(points_original[0, :], points_original[1, :], label='Original Circle')
ax1.set_title('1. Input Space (2D)')
ax1.grid()

# 2. 第一步变换：V^T (输入空间的旋转)
# Vt 是 2x2, points_original 是 2x100
points_rotated = Vt @ points_original
ax2.plot(points_rotated[0, :], points_rotated[1, :], label='After $V^T$ Rotation')
ax2.set_title('2. After $V^T$ (Rotation)')
ax2.grid()

# 3. 第二步变换：Sigma (拉伸并提升维度)
# Sigma 是 3x2, points_rotated 是 2x100 -> 结果是 3x100
points_scaled = Sigma @ points_rotated
ax3.plot(points_scaled[0, :], points_scaled[1, :], points_scaled[2, :], label='After $\Sigma$ Scaling')
ax3.set_title('3. After $\Sigma$ (Scaling to 3D)')
ax3.set_xlabel('X'); ax3.set_ylabel('Y'); ax3.set_zlabel('Z')
ax3.view_init(elev=20, azim=30) # 调整视角

# 4. 第三步变换：U (输出空间的最终旋转)
# U 是 3x3, points_scaled 是 3x100 -> 结果是 3x100
points_final_svd = U @ points_scaled

# 作为对比，直接用 A 进行变换
points_final_A = A @ points_original

# 绘制 SVD 三步法的结果
ax4.plot(points_final_svd[0, :], points_final_svd[1, :], points_final_svd[2, :], 'r-', label='Final Shape (from SVD)')
# 绘制直接用 A 变换的结果
ax4.plot(points_final_A[0, :], points_final_A[1, :], points_final_A[2, :], 'g--', label='Final Shape (from A direct)')
ax4.set_title('4. Final Result')
ax4.set_xlabel('X'); ax4.set_ylabel('Y'); ax4.set_zlabel('Z')
ax4.view_init(elev=20, azim=30)
ax4.legend()

plt.tight_layout()
plt.show()
