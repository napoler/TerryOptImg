# Image Optimizer 用户手册

## 📖 简介
**Image Optimizer** 是一个开源的图像压缩工具，复刻了 Curtail 的核心功能。它支持 JPG、PNG、WebP、SVG 格式的无损和有损压缩，提供直观的 GUI 界面和强大的 CLI 命令行模式。

## ⚙️ 安装指南

### 前置要求
- Python 3.8 或更高版本
- 推荐安装外部工具以获得最佳压缩效果：
  - `jpegoptim` (用于 JPG)
  - `pngquant` (用于 PNG)
  - `svgo` 或 `scour` (用于 SVG)

### 源码安装
```bash
# 1. 克隆仓库
git clone https://github.com/your/repo.git
cd repo

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行 GUI
python src/image_optimizer_gui.py

# 4. 运行 CLI
python src/image_optimizer.py --help
```

## 🖥️ GUI 使用指南

### 界面概览
1. **输入选择**: 点击 "Add Files" 或 "Add Folder" 选择要处理的图片。
2. **模式选择**:
   - **Lossy (有损)**: 默认模式，平衡体积与画质。Quality 默认为 85。
   - **Lossless (无损)**: 仅优化数据结构，不损失画质。Quality 锁定为 100。
3. **设置**:
   - **Keep Metadata**: 是否保留 EXIF 等元数据。
   - **Quality**: 压缩质量 (1-100)。
   - **Workers**: 并发线程数。程序会根据 CPU 核心数自动设定智能默认值。
   - **Low Resource Mode**: 勾选后限制为单线程，适合后台运行。
4. **输出控制**:
   - **Max Width/Height**: 输入像素值，图片长边若超过此值将被缩小。
   - **Format**: 转换目标格式 (如 PNG 转 WebP)。
   - **Overwrite**: 勾选则覆盖原文件；不勾选需选择输出目录（默认在原目录创建 `optimized` 文件夹）。
5. **控制**:
   - **Start Optimization**: 开始处理。
   - **Stop**: 随时取消任务。

## 💻 CLI 使用指南

```bash
python src/image_optimizer.py [INPUT] [OPTIONS]
```

### 常用参数
- `input`: 输入文件或目录路径。
- `-o, --output`: 输出目录。
- `-s, --max-size`: 最大像素尺寸 (resize)。
- `-f, --format`: 目标格式 (jpg, png, webp)。
- `-w, --workers`: 并发线程数。
- `-q, --quality`: 压缩质量 (默认 85)。
- `--overwrite`: 覆盖原文件。

### 示例
```bash
# 将 images 目录下的所有图片转换为 WebP，限制宽/高 1920，保存到 dist 目录
python src/image_optimizer.py ./images -o ./dist -f webp -s 1920
```

### 图标与快捷方式
- **Windows**: 使用 `scripts/build.py` 生成的 exe 包含内嵌图标。
- **Linux**: 使用 `scripts/build_deb.py` 生成的 deb 包会自动安装图标到 `/usr/share/icons`，并在应用程序菜单中显示。如果图标未显示，请尝试运行 `sudo gtk-update-icon-cache -f /usr/share/icons/hicolor`。

## ❓ 故障排除

**Q: 压缩效果不明显？**
A: 请确保已安装 `jpegoptim` 或 `pngquant`。如果未安装，程序会回退到 Python Pillow 库进行压缩，效果可能不如专用工具。

**Q: 程序卡死？**
A: 请检查是否开启了过多的 Workers。尝试勾选 "Low Resource Mode"。

**Q: SVG 文件未被处理？**
A: SVG 优化需要系统安装 `svgo` 或 `scour` 命令。
