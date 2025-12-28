# TerryOptImg - Professional Image Optimizer (Qt Version)

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-blue)

一个功能强大的现代化图像优化工具，采用PyQt5框架，提供美观的图形界面和强大的压缩功能。

## ✨ 核心特性

- **🎨 现代Qt5界面**: 美观专业的图形用户界面
- **🔄 智能检测**: 自动检测Qt5可用性，智能回退到tkinter
- **🎯 双压缩模式**: 支持有损和无损压缩算法
- **📁 多格式支持**: 优化JPG, PNG, WebP等主流格式
- **⚡ 批量处理**: 多线程并发处理，充分利用CPU性能
- **📊 实时进度**: 美观的进度条和状态指示器
- **📝 彩色日志**: 带时间戳的彩色日志系统
- **🎭 丰富图标系统**: 表情符号+文本双重后备方案
- **📱 响应式设计**: 自适应不同屏幕尺寸和DPI
- **🌈 现代主题**: 渐变背景和专业配色方案
- **⚙️ 增强设置**: 标签页式设置对话框

## 🚀 快速开始

### 安装依赖
```bash
git clone https://github.com/your/repo.git
cd repo
pip install -r requirements.txt
```

### 运行应用
**自动检测模式** (推荐):
```bash
python src/image_optimizer_gui.py
```
**直接Qt模式**:
```bash
python src/qt_image_optimizer.py
```
**命令行模式**:
```bash
python src/image_optimizer.py input.jpg -o out/ -q 80
```

### 🎨 界面特色
- **🎨 增强标题栏**: 渐变背景的专业标题
- **📁 文件选择区**: 清晰的文件计数和操作按钮
- **⚙️ 设置区域**: 直观的参数配置界面
- **📊 进度显示**: 美观的进度条和状态标签
- **📝 日志区域**: 深色主题的实时日志输出
- **🔘 操作按钮**: 大尺寸的启动/停止按钮

## 📚 文档导航

- [用户手册 (USER_GUIDE.md)](docs/USER_GUIDE.md): 详细的使用说明
- [打包指南 (PACKAGING.md)](docs/PACKAGING.md): 如何生成可执行文件
- [安装 SpecKit (SPECKIT_INSTALLATION.md)](docs/SPECKIT_INSTALLATION.md): 开发环境配置
- [图像优化器规格 (IMAGE_OPTIMIZER_SPEC.md)](docs/IMAGE_OPTIMIZER_SPEC.md): 技术规格说明
- [设置页面规格 (docs/SPECS/FR-008-Settings-Page.md)](docs/SPECS/FR-008-Settings-Page.md): 设置界面设计规格

## 🎯 界面对比

| 特性 | Qt版本 | 传统版本 |
|------|-------------|----------------|
| **外观** | 现代渐变设计 | 基础原生控件 |
| **图标** | 丰富表情符号+文本 | 系统图标 |
| **性能** | 硬件加速渲染 | 标准渲染 |
| **响应式** | 自动缩放适配 | 固定布局 |
| **主题** | 多主题支持 | 单一主题 |
| **动画** | 平滑过渡效果 | 基础交互 |
| **设置** | 标签页式对话框 | 简单选项 |

## ⚙️ 高级功能

### 🧵 智能模式
- 自动检测图片类型并选择最佳压缩算法
- 根据内容类型调整压缩参数
- 智能文件大小优化建议

### 🔧 高级设置
- **备份策略**: 处理前自动备份原文件
- **智能过滤**: 跳过已优化的文件
- **详细日志**: 完整的调试和审计日志
- **性能调优**: 内存限制和线程池配置

### 🎨 主题定制
- **现代蓝色主题**: 默认的渐变蓝主题
- **深色主题**: 护眼的深色界面
- **高对比度**: 提升可访问性
- **自定义配色**: 用户自定义颜色方案

## 🚀 性能优化

- **🧵 多线程处理**: 智能CPU核心数检测
- **💾 内存管理**: 大文件分块处理
- **🔥 并发控制**: 可配置的线程池大小
- **⚡ 批量优化**: 支持同时处理数百个文件
- **📊 进度反馈**: 实时性能指标显示

## 🛠️ 系统要求

### 最低要求
- Python 3.6+
- PyQt5 (推荐) 或 tkinter
- 4GB RAM (处理大型图片时)

### 推荐配置
- Python 3.8+
- PyQt5.15+
- 8GB RAM
- 多核CPU处理器

## 🔧 开发环境

### 构建应用
```bash
python scripts/build.py
```

### 生成DEB包
```bash
python scripts/build_deb.py
```

### 运行测试
```bash
python test_themes.py
```

### 安装依赖
```bash
python scripts/install_speckit.py
```

## 🤝 贡献

本项目遵循 **SpecKit** 文档驱动开发规范。欢迎贡献代码、报告问题或提出功能建议！

### 开发重点
- 🎨 界面设计改进
- ⚡ 性能优化
- 🎭 用户体验提升
- 🔧 功能扩展

### 贡献指南
1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 📋 Changelog

### Version 2.0.0 (Qt版本)
- **🎨 完全重构**: 基于PyQt5的现代化界面
- **🎭 图标系统**: 完整的图标资源管理
- **📱 响应式设计**: 自适应不同屏幕尺寸
- **🌈 现代主题**: 多主题支持
- **⚙️ 增强设置**: 标签页式设置对话框
- **🔧 智能回退**: 自动检测Qt可用性
- **📊 视觉反馈**: 改进的进度和状态显示

### Version 1.0.0 (原始版本)
- 基础图像优化功能
- tkinter界面
- 命令行支持
- 基本设置系统

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎贡献代码、报告问题或提出功能建议！

### 开发者指南
- 遵循 SpecKit 文档驱动开发规范
- 优先考虑用户体验改进
- 确保代码质量和性能
- 提供详细的提交信息

### 贡献类型
- 🎨 界面设计改进
- ⚡ 性能优化
- 🔧 功能扩展
- 🐛 Bug修复
- 📚 文档完善

## 📞 联系方式

- **Issues**: [GitHub Issues](https://github.com/your/repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your/repo/discussions)
- **邮件**: terry@example.com

---

**🚀 享受现代化的图像优化体验！**