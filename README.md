# Image Optimizer (Curtail Replica)

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

一个功能强大的本地图片压缩工具，完美复刻 Curtail 的核心体验。支持 GUI 和命令行操作。

## ✨ 核心特性

- **多格式支持**: JPG, PNG, WebP, SVG。
- **智能压缩**:
  - **Lossy**: 智能有损压缩，平衡画质与体积。
  - **Lossless**: 无损优化，保留原画质。
- **高级功能**:
  - **智能缩放**: 限制最大像素尺寸。
  - **格式转换**: 一键转换图片格式。
  - **元数据控制**: 自由选择是否保留 EXIF 信息。
- **高性能**:
  - **智能并发**: 根据 CPU 核心数自动调整线程。
  - **后台模式**: 低资源占用模式，不影响其他工作。
- **跨平台**: 支持 Windows, Linux, macOS。

## 🚀 快速开始

### 安装
```bash
git clone https://github.com/your/repo.git
cd repo
pip install -r requirements.txt
```

### 运行
**GUI 模式**:
```bash
python src/image_optimizer_gui.py
```

**命令行模式**:
```bash
python src/image_optimizer.py input.jpg -o out/ -q 80
```

## 📚 文档导航
- [用户手册 (User Guide)](docs/USER_GUIDE.md): 详细的使用说明。
- [打包指南 (Packaging)](docs/PACKAGING.md): 如何生成可执行文件。
- [安装 SpecKit](docs/SPECKIT_INSTALLATION.md): 开发环境配置。

## 🤝 贡献
本项目遵循 **SpecKit** 文档驱动开发规范。请在提交代码前阅读 [AGENTS.md](AGENTS.md)。

## 📄 许可证
MIT License
