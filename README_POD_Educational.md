# POD Educational Animation - 使用说明

## 简介

这是一个使用Manim库创建的POD（Proper Orthogonal Decomposition）教学动画，采用3Blue1Brown风格设计，适合本科生学习。

## 动画内容

### 场景结构（总时长约5-7分钟）

1. **场景1: 物理实验引入**（30秒）
   - 从物理实验的两个传感器数据引入
   - 生成椭圆形点云
   - 说明传统坐标系的局限性

2. **场景2: 2D能量搜索**（1.5-2分钟）
   - 展示POD的核心思想：寻找能量最大方向
   - 旋转扫描向量，实时显示能量变化
   - 找到第一模态（Mode 1）

3. **场景3: 正交约束**（1分钟）
   - 展示Mode 2必须正交于Mode 1
   - 可视化正交关系
   - 锁定两个主要模态

4. **场景4: 数学公式讲解**（1分钟）
   - 数据矩阵构建
   - 协方差矩阵计算
   - 特征值分解原理

5. **场景5: 3D扩展**（1.5-2分钟）
   - 生成3D椭球点云
   - 详细演示三个模态的搜索过程
   - 展示三维空间的正交性

6. **场景6: 总结**（30秒）
   - POD核心要点回顾
   - 最终总结

## 安装依赖

```bash
# 安装Manim
pip install manim

# 或使用Manim Community Edition
pip install manim-ce

# 安装其他依赖
pip install numpy
```

## 使用方法

### 方法1: 使用渲染脚本（推荐）

```bash
# 进入目录
cd podstudy

# 标准质量渲染（720p30）
python render_pod_educational.py

# 低质量快速预览（480p15）
python render_pod_educational.py low

# 高质量渲染（1080p60）
python render_pod_educational.py high

# 只预览最后一帧（不生成完整视频）
python render_pod_educational.py preview
```

### 方法2: 直接使用Manim命令

```bash
# 低质量（480p15，快速预览）
manim pod_educational.py PODEducational -ql

# 中等质量（720p30，推荐）
manim pod_educational.py PODEducational -qm

# 高质量（1080p60，最终版本）
manim pod_educational.py PODEducational -qh

# 预览模式（只生成最后一帧）
manim pod_educational.py PODEducational -ps
```

## 渲染时间估算

- 低质量（480p15）: 约3-5分钟
- 中等质量（720p30）: 约8-12分钟
- 高质量（1080p60）: 约20-30分钟

*时间取决于计算机性能*

## 输出位置

渲染完成后，视频文件位于：
```
podstudy/media/videos/pod_educational/[质量等级]/PODEducational.mp4
```

## 自定义修改

### 修改点云数据

在 `scene1_introduction()` 方法中修改协方差矩阵：

```python
# 调整椭圆的形状和方向
cov_matrix = [[2.5, 2.0], [2.0, 2.5]]  # 修改这些数值
```

### 修改颜色方案

文件中使用的颜色：
- `YELLOW`: 标题和重点强调
- `BLUE_C`: 数据点
- `GREEN`: Mode 1（第一模态）
- `RED`: Mode 2（第二模态）
- `ORANGE`: Mode 3 / 能量相关元素

### 修改动画速度

调整各场景中的 `run_time` 参数：

```python
self.play(Create(obj), run_time=2)  # 2秒完成动画
```

### 修改字体

在 `setup_fonts()` 方法中修改：

```python
# Windows
self.CN_FONT = "Microsoft YaHei"  # 或 "SimHei", "KaiTi" 等

# macOS
self.CN_FONT = "PingFang SC"  # 或 "STHeiti", "Songti SC" 等
```

## 常见问题

### Q1: 提示找不到字体

A: 检查系统是否安装了中文字体，或在代码中修改为系统已有的字体名称。

### Q2: 渲染过程中卡住

A: 可能是内存不足，尝试：
1. 降低渲染质量（使用 `-ql`）
2. 减少点云数量（修改代码中的点数）
3. 分段渲染各个场景

### Q3: 颜色显示不正常

A: 确保使用的是Manim Community Edition，某些颜色定义可能不兼容旧版本。

### Q4: 3D场景相机角度不理想

A: 在 `scene5_3d_extension()` 中调整相机参数：

```python
self.set_camera_orientation(
    phi=70 * DEGREES,    # 俯仰角
    theta=30 * DEGREES   # 方位角
)
```

## 技术特点

1. **教学友好**：从应用场景切入，逐步深入数学原理
2. **可视化丰富**：能量变化、投影过程、正交关系均有可视化
3. **公式展示**：关键数学公式配合动画讲解
4. **3D演示**：完整展示三维空间的POD过程

## 参考资源

- Manim官方文档: https://docs.manim.community/
- 3Blue1Brown频道: https://www.youtube.com/c/3blue1brown
- POD理论介绍: 见项目中的其他教学材料

## 重要更新：分离版本 (推荐使用)

### 问题说明

原始 `pod_educational.py` 存在技术问题:
- 继承自 `ThreeDScene` 但前4个场景使用 2D `Axes`
- 3D相机与2D对象坐标转换导致 `IndexError: too many indices for array`
- `add_fixed_in_frame_mobjects` 与 3D 坐标系冲突

### 解决方案：分离版本

已创建两个独立文件,彻底解决上述问题:

#### 1. `pod_educational_2d.py`
- 继承: `Scene` (纯2D场景)
- 内容: Scene1-4 (引入、能量搜索、正交约束、数学公式)
- 特点: 无3D相机冲突,渲染稳定

#### 2. `pod_educational_3d.py`
- 继承: `ThreeDScene` (3D场景)
- 内容: Scene5-6 (3D扩展、总结)
- 特点: 正确使用3D功能

### 使用分离版本 (推荐)

```bash
# 使用统一渲染脚本
python render_pod_split.py          # 渲染全部(2D+3D)
python render_pod_split.py 2d low   # 只渲染2D部分
python render_pod_split.py 3d high  # 只渲染3D部分
python render_pod_split.py --help   # 查看帮助

# 或者分别渲染
"G:/Users/26689/anaconda3/envs/manim_env/Scripts/manim.exe" pod_educational_2d.py PODEducational2D -ql
"G:/Users/26689/anaconda3/envs/manim_env/Scripts/manim.exe" pod_educational_3d.py PODEducational3D -ql
```

### 输出位置
- 2D部分: `media/videos/pod_educational_2d/`
- 3D部分: `media/videos/pod_educational_3d/`

### 合并视频(可选)

使用 ffmpeg 合并两个视频:

```bash
# 创建文件列表
echo "file 'media/videos/pod_educational_2d/480p15/PODEducational2D.mp4'" > filelist.txt
echo "file 'media/videos/pod_educational_3d/480p15/PODEducational3D.mp4'" >> filelist.txt

# 合并
ffmpeg -f concat -safe 0 -i filelist.txt -c copy POD_Complete.mp4
```

### 为什么分离?

| 问题 | 原因 | 分离后解决方案 |
|------|------|---------------|
| IndexError | ThreeDScene + 2D Axes 维度不匹配 | 2D场景用Scene基类 |
| 坐标转换错误 | c2p()在3D环境返回3D坐标 | 2D/3D坐标系各自独立 |
| fixed_in_frame冲突 | 2D对象与3D相机冲突 | 仅3D场景使用该功能 |

## 贡献与反馈

如有问题或改进建议，欢迎提出！
