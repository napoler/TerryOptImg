#!/usr/bin/env python3
"""
TerryOptImg Qt Launcher
启动Qt版本的图像优化器
"""
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from qt_image_optimizer import main
    main()
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保已安装PyQt5: pip install PyQt5")
    sys.exit(1)
except Exception as e:
    print(f"❌ 启动错误: {e}")
    sys.exit(1)