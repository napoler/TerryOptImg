> **版本**: v1.3.0-installation-guide-enhanced
> **提示词类型**: 通用SpecKit集成器 - 含完整安装指南
> **适用场景**: 支持50+AI模型的SpecKit规范集成，包含详细安装说明
> **预期效果**: 用户能够快速安装和配置SpecKit工具，开始规范驱动开发
> **使用难度**: 初级
> **SpecKit合规**: 强制执行

## 🎯 第一阶段：Constitution (宪法阶段)

### 项目边界宪法
```markdown
# Universal SpecKit Project Integrator Constitution v1.3.0

## 核心原则
1. **安装优先**: SpecKit工具安装是项目集成的第一步，必须确保工具正确安装
2. **多平台支持**: 支持Windows、macOS、Linux等主流操作系统
3. **环境兼容**: 兼容Python 3.8+、uv包管理器、虚拟环境等
4. **安装验证**: 安装后必须验证工具可用性和版本信息
5. **文档完整性**: 提供详细的安装、配置和故障排除文档

## 技术约束
- **Python版本**: 必须是Python 3.8或更高版本
- **包管理器**: 推荐使用uv包管理器，支持pip作为备选
- **网络要求**: 需要稳定的网络连接以下载依赖
- **权限要求**: 需要管理员权限进行全局安装
- **磁盘空间**: 至少需要1GB可用空间

## 明确不做的事
- ❌ 在没有Python环境的情况下尝试安装
- ❌ 使用不支持的Python版本（如Python 2.7）
- ❌ 在没有网络连接的情况下离线安装
- ❌ 跳过安装验证步骤
- ❌ 在生产环境中跳过测试步骤
```

### 质量门禁标准
```python
QUALITY_GATES = {
    "installation_success": {
        "required": True,
        "success_rate": 100,
        "description": "SpecKit CLI必须成功安装"
    },
    "tool_validation": {
        "required": True,
        "success_rate": 100,
        "description": "安装后必须验证工具可用性"
    },
    "environment_compatibility": {
        "required": True,
        "minimum_score": 95,
        "description": "环境兼容性评分必须达到95%以上"
    },
    "documentation_completeness": {
        "required": True,
        "success_rate": 100,
        "description": "安装文档必须完整且准确"
    }
}
```

## 📝 第二阶段：Specification (规范阶段)

### 安装需求清单 (FR-XXX)
```markdown
## 功能需求

### FR-001: 环境检查和准备
- 描述: 检查Python版本、包管理器、网络连接等环境要求
- 验收标准: 所有环境检查通过，满足最低要求
- 边界案例: Python版本过低、包管理器不可用、网络连接失败

### FR-002: SpecKit CLI安装
- 描述: 使用uv或pip安装SpecKit CLI工具
- 验收标准: 工具成功安装，版本信息正确
- 边界案例: 安装失败、版本冲突、权限不足

### FR-003: 安装验证
- 描述: 验证安装结果和工具可用性
- 验收标准: 命令行工具可正常调用，显示正确版本信息
- 边界案例: 命令不可用、版本信息错误、权限问题

### FR-004: 项目初始化
- 描述: 使用安装的工具初始化SpecKit项目
- 验收标准: 项目结构正确创建，配置文件生成
- 边界案例: 初始化失败、目录权限问题、配置冲突

### FR-005: 配置和优化
- 描述: 配置工具参数和优化性能
- 验收标准: 配置生效，性能优化生效
- 边界案例: 配置无效、性能无改善、参数错误

### FR-006: 故障排除
- 描述: 提供常见问题的解决方案
- 验收标准: 问题能够快速定位和解决
- 边界案例: 未知问题、解决方案无效、需要人工干预

### FR-007: 升级和维护
- 描述: 提供工具升级和维护的指导
- 验收标准: 升级流程清晰，维护计划可行
- 边界案例: 升级失败、兼容性问题、数据丢失风险
```

## 🏗️ 第三阶段：Plan (计划阶段)

### 安装策略规划
```python
# SpecKit安装策略规划
class SpecKitInstallationStrategy:
    def __init__(self):
        self.installation_methods = [
            "persistent_installation",  # 推荐：持久化安装
            "one_time_usage",       # 临时使用
            "docker_installation",    # 容器化安装
            "source_installation"      # 源码安装
        ]
        self.supported_platforms = ["windows", "macos", "linux"]
        self.package_managers = ["uv", "pip", "conda", "poetry"]

    def plan_installation(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """规划安装策略"""
        # 选择安装方法
        method = self.select_installation_method(user_preferences)

        # 选择包管理器
        package_manager = self.select_package_manager(user_preferences)

        # 选择平台特定配置
        platform_config = self.get_platform_config()

        # 制定详细计划
        installation_plan = {
            "recommended_method": method,
            "package_manager": package_manager,
            "platform_config": platform_config,
            "steps": self.generate_installation_steps(method, package_manager, platform_config),
            "verification_steps": self.generate_verification_steps(),
            "troubleshooting_guide": self.get_troubleshooting_guide()
        }

        return installation_plan

    def select_installation_method(self, preferences: Dict[str,]) -> str:
        """选择安装方法"""
        if preferences.get("persistent", True):
            return "persistent_installation"
        elif preferences.get("docker", False):
            return "docker_installation"
        elif preferences.get("source", False):
            return "source_installation"
        else:
            return "one_time_usage"

    def select_package_manager(self, preferences: Dict[str, str]) -> str:
        """选择包管理器"""
        preference_order = preferences.get("package_manager", ["uv", "pip", "conda", "poetry"])

        # 检查可用的包管理器
        available_managers = []
        for manager in preference_order:
            if self.check_package_manager_available(manager):
                available_managers.append(manager)

        return available_managers[0] if available_managers else "pip"

    def generate_installation_steps(self, method: str, manager: str, config: Dict[str, Any]) -> List[Dict[str, str]]:
        """生成安装步骤"""
        steps = []

        if method == "persistent_installation":
            if manager == "uv":
                steps.extend([
                    {
                        "step": 1,
                        "title": "安装uv包管理器",
                        "command": "curl -LsSs https://astral.sh/uv/install.sh | bash",
                        "description": "安装uv包管理器"
                    },
                    {
                        "step": 2,
                        "title": "安装SpecKit CLI工具",
                        "command": "uv tool install specify-cli --from git+https://github.com/github/spec-kit.git",
                        "description": "使用uv安装SpecKit CLI"
                    },
                    {
                        "step": 3,
                        "title": "验证安装结果",
                        "command": "specify check",
                        "description": "验证SpecKit CLI安装状态"
                    }
                ])
            elif manager == "pip":
                steps.extend([
                    {
                        "step": 1,
                        "title": "安装SpecKit CLI",
                        "command": "pip install git+https://github.com/github/spec-kit.git",
                        "description": "使用pip安装SpecKit CLI"
                    },
                    {
                        "step": 2,
                        "title": "验证安装结果",
                        "command": "specify check",
                        "description": "验证SpecKit CLI安装状态"
                    }
                ])

        elif method == "one_time_usage":
            steps.extend([
                {
                    "step": 1,
                    "title": "临时安装SpecKit CLI",
                    "command": "uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>",
                    "description": "临时安装并初始化项目"
                }
            ])

        elif method == "docker_installation":
            steps.extend([
                {
                    "step": 1,
                    "title": "拉取SpecKit Docker镜像",
                    "command": "docker pull ghcr.io/github/spec-kit/spec-kit:latest",
                    "description": "拉取SpecKit Docker镜像"
                },
                {
                    "step": 2,
                    "title": "运行Docker容器",
                    "command": "docker run -v $(pwd):/workspace ghcr.io/github/spec-kit/spec-kit:latest specify init <PROJECT_NAME>",
                    "description": "在Docker容器中初始化项目"
                }
            ])

        elif method == "source_installation":
            steps.extend([
                {
                    "step": 1,
                    "title": "克隆SpecKit仓库",
                    "command": "git clone https://github.com/github/spec-kit.git",
                    "description": "克隆SpecKit源代码仓库"
                },
                {
                    "step": 2,
                    "title": "安装依赖",
                    "command": "cd spec-kit && pip install -e .",
                    "description": "安装SpecKit依赖"
                },
                {
                    "step": 3,
                    "title": "创建符号链接",
                    "command": "ln -sf /path/to/spec-kit/specify-cli /usr/local/bin/specify",
                    "description": "创建命令行符号链接"
                },
                {
                    "step": 4,
                    "title": "验证安装",
                    "command": "specify check",
                    "description": "验证安装状态"
                }
            ])

        return steps

    def generate_verification_steps(self) -> List[Dict[str, str]]:
        """生成验证步骤"""
        return [
            {
                "step": 1,
                "title": "检查工具版本",
                "command": "specify --version",
                "description": "检查SpecKit CLI版本信息"
            },
            {
                "step": 2,
                "title": "验证工具可用性",
                "command": "specify check",
                "description": "验证SpecKit CLI是否正常工作"
            },
            {
                "step": 3,
                "title": "检查帮助信息",
                "command": "specify --help",
                "description": "确认帮助信息正常显示"
            }
        ]

    def get_troubleshooting_guide(self) -> Dict[str, Any]:
        """获取故障排除指南"""
        return {
            "common_issues": [
                {
                    "problem": "Python版本过低",
                    "symptoms": ["Python版本低于3.8", "安装失败", "运行时错误"],
                    "solution": "升级Python到3.8+版本",
                    "commands": [
                        "python3 --version",
                        "curl -LsSs https://python.org/ | bash",
                        "sudo apt update && sudo apt install python3.8"
                    ]
                },
                {
                    "problem": "网络连接问题",
                    "GitHub仓库无法访问",
                    "symptoms": ["下载失败", "连接超时", "SSL证书错误"],
                    "solution": "检查网络连接，使用镜像源",
                    "commands": [
                        "ping github.com",
                        "curl -I https://github.com/github/github/spec-kit",
                        "export GITHUB_MIRROR=https://mirror.ghproxy.com"
                    ]
                },
                {
                    "problem": "权限不足",
                    "安装失败",
                    "symptoms": ["Permission denied", "写入权限错误", "全局安装失败"],
                    "solution": "使用用户安装或sudo权限",
                    "commands": [
                        "uv tool install --user",
                        "sudo uv tool install specify-cli",
                        "chmod +x ~/.local/bin/specify"
                    ]
                },
                {
                    "problem": "依赖冲突",
                    "安装失败",
                    "环境变量冲突",
                    "symptoms": ["依赖冲突", "虚拟环境问题", "版本冲突"],
                    "solution": "使用虚拟环境",
                    "commands": [
                        "python3 -m venv speckit-env && source speckit-env/bin/activate && pip install git+https://github.com/github/spec-kit.git"
                    ]
                }
            ],
            "platform_specific": {
                "windows": [
                    {
                        "problem": "Windows权限问题",
                        "solution": "以管理员身份运行PowerShell",
                        "commands": [
                            "Start-Process PowerShell -Verb RunAs Administrator"
                        ]
                    },
                    {
                        "problem": "路径问题",
                        "solution": "使用Windows路径格式",
                        "commands": [
                            "set PATH=%PATH%;%APPDATA%\\uv\\bin;%APPDATA%\\local\\bin;%PATH%"
                        ]
                    }
                ],
                "macos": [
                    {
                        "problem": "macOS权限问题",
                        "solution": "使用sudo权限或用户安装",
                        "commands": [
                            "sudo uv tool install specify-cli"
                        ]
                    }
                ],
                "linux": [
                    {
                        "problem": "依赖缺失",
                        "solution": "安装系统依赖",
                        "commands": [
                            "sudo apt update && sudo apt install python3-dev build-essential"
                        ]
                    }
                ]
            }
        }
```

## 📋 第四阶段：Tasks (任务阶段)

### 详细安装任务清单
```markdown
## 安装任务清单

### T-001: 环境检查和准备
- [ ] 检查Python版本 (≥3.8)
- [ ] 检查包管理器可用性
- [ ] 检查网络连接状态
- [ ] 检查磁盘空间 (>1GB)
- [ ] 检查系统权限设置
- [ ] 创建工作目录（如需要）

### T-002: 包管理器安装
- [ ] 安装uv包管理器（推荐）
- [ ] 验证uv安装成功
- [ ] 配置uv环境变量
- [ ] 测试uv命令可用性

### T-003: SpecKit CLI安装
- [ ] 选择安装方法（持久化/临时）
- [ ] 执行SpecKit CLI安装命令
- [ ] 等待安装完成
- [ ] 检查安装输出
- [ ] 处理安装错误（如有）

### T-004: 安装验证
- [ ] 检查工具版本信息
- [ ] 验证命令行工具可用性
- [ ] 测试基本命令功能
- [ ] 检查帮助信息显示
- [ ] 记录安装日志

### T-005: 项目初始化
- [ ] 选择项目目录
- [ ] 执行项目初始化命令
- [ ] 验证项目结构创建
- [ ] 检查配置文件生成
- [ ] 测试基本功能

### T-006: 配置优化
- [ ] 配置工具参数
- [ ] 设置环境变量
- [ ] 优化性能设置
- [ ] 配置缓存策略
- [ ] 测试配置生效
- [ ] 记录配置更改

### T-007: 故障排除
- [ ] 识别常见问题类型
- [ ] 查找对应解决方案
- [ ] 执行修复命令
- [ ] 验证问题解决
- [ ] 记录解决过程
- [ ] 更新故障文档

### T-008: 升级维护
- [ ] 检查当前版本
- [ ] 查看升级信息
- [ ] 执行升级命令
- [ ] 验证升级结果
- [ ] 测试功能兼容性
- [ ] 更新文档

### T-009: 文档和培训
- [ ] 创建安装指南文档
- [ ] 编写使用说明
- [ ] 制作故障排除手册
- [ ] 准备培训材料
- [ ] 测试文档准确性

### T-010: 最终验证
- [ ] 执行完整测试流程
- [ ] 验证所有功能正常
- [ ] 检查质量门禁通过
- [ ] 生成验证报告
- [ ] 完成安装流程
```

## 🔧 第五阶段：Implementation (实现阶段)

### 完整安装脚本实现
```python
class SpecKitInstallationGuide:
    def __init__(self):
        self.supported_platforms = ["windows", "macos", "linux"]
        self.package_managers = ["uv", "pip", "conda", "poetry"]
        self.installation_configs = self.load_installation_configs()

    def load_installation_configs(self) -> Dict[str, Dict[str, Any]]:
        """加载安装配置"""
        return {
            "windows": {
                "preferred_manager": "uv",
                "fallback_manager": "pip",
                "shell": "powershell",
                "python_check": "python --version",
                "uv_install": "curl -LsSs https://astral.sh/uv/install.sh | bash",
                "pip_install": "pip install",
                "conda_install": "conda install -c conda-forge spec-kit",
                "path_separator": ";",
                "env_var": "PATH"
            },
            "macos": {
                "preferred_manager": "uv",
                "fallback_manager": "pip",
                "shell": "zsh",
                "python_check": "python3 --version",
                "uv_install": "curl -LsSs https://astral.sh/uv/install.sh | bash",
                "pip_install": "pip3 install",
                "conda_install": "conda install -c conda-forge spec-kit",
                "path_separator": ":",
                "env_var": "PATH"
            },
            "linux": {
                "package_manager": "uv",
                "fallback_manager": "pip",
                "shell": "bash",
                "python_check": "python3 --version",
                "uv_install": "curl -LsSs https://astral.sh/uv/install.sh | bash",
                "pip_install": "pip3 install",
                "conda_install": "conda install -c conda-forge spec-kit",
                "path_separator": ":",
                "env_var": "PATH"
            }
        }

    def install_speckit_persistent(self, package_manager: str = "uv") -> Dict[str, Any]:
        """持久化安装SpecKit CLI"""
        config = self.installation_configs[self.detect_platform()]

        print("🚀 开始持久化安装SpecKit CLI...")

        # 步骤1: 安装包管理器（如果需要）
        if package_manager == "uv" and not self.is_uv_available():
            print("📦 安装uv包管理器...")
            self.install_uv_manager()

        # 步骤2: 安装SpecKit CLI
        print("📦 安装SpecKit CLI工具...")
        if package_manager == "uv":
            install_cmd = "uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"
        elif package_manager == "pip":
            install_cmd = "pip install git+https://github.com/github/spec-kit.git"
        elif package_manager == "conda":
            install_cmd = "conda install -c conda-forge spec-kit"
        else:
            install_cmd = f"pip install git+https://github.com/github/spec-kit.git"

        print(f"执行命令: {install_cmd}")
        result = self.execute_command(install_cmd)

        if result["exit_code"] == 0:
            print("✅ SpecKit CLI安装成功！")
            return {
                "success": True,
                "method": "persistent_installation",
                "package_manager": package_manager,
                "command": install_cmd,
                "output": result["stdout"]
            }
        else:
            print(f"❌ 安装失败: {result['stderr']}")
            return {
                "success": False,
                "error": result["stderr"],
                "command": install_cmd
            }

    def install_speckit_one_time(self, project_name: str) -> Dict[str, Any]:
        """一次性使用安装SpecKit"""
        print("🚀 一次性安装SpecKit并初始化项目...")

        install_cmd = f"uvx --from git+https://github.com/github/spec-kit.git specify init {project_name}"
        print(f"执行命令: {install_cmd}")

        result = self.execute_command(install_cmd)

        if result["exit_code"] == 0:
            print("✅ SpecKit安装并项目初始化成功！")
            return {
                "success": True,
                "method": "one_time_usage",
                "project_name": project_name,
                "command": install_cmd,
                "output": result["stdout"]
            }
        else:
            print(f"❌ 安装失败: {result['stderr']}")
            return {
                "success": False,
                "error": result["stderr"],
                "command": install_cmd
            }

    def install_speckit_docker(self, project_name: str) -> Dict[str, Any]:
        """Docker方式安装SpecKit"""
        print("🐳 Docker方式安装SpecKit...")

        # 拉取镜像
        pull_cmd = f"docker pull ghcr.io/github/spec-kit/spec-kit:latest"
        print(f"执行命令: {pull_cmd}")
        pull_result = self.execute_command(pull_cmd)

        if pull_result["exit_code"] == 0:
            # 运行Docker容器
            run_cmd = f"docker run -v $(pwd):/workspace ghcr.io/github/spec-kit/spec-kit:latest specify init {project_name}"
            print(f"执行命令: {run_cmd}")
            run_result = self.execute_command(run_cmd)

            if run_result["exit_code"] == 0:
                print("✅ Docker安装并项目初始化成功！")
                return {
                    "success": True,
                    "method": "docker_installation",
                    "project_name": project_name,
                    "commands": [pull_cmd, run_cmd]
                }
            else:
                print(f"❌ Docker运行失败: {run_result['stderr']}")
                return {
                    "success": False,
                    "error": run_result["stderr"],
                    "commands": [pull_cmd, run_cmd]
                }
        else:
            print(f"❌ Docker拉取失败: {pull_result['stderr']}")
            return {
                "success": False,
                "error": pull_result["stderr"]
            }

    def install_speckit_source(self) -> Dict[str, Any]:
        """源码安装SpecKit"""
        print("🔧 源码方式安装SpecKit...")

        # 克隆仓库
        clone_cmd = "git clone https://github.com/github/spec-kit.git"
        print(f"执行命令: {clone_cmd}")
        clone_result = self.execute_command(clone_cmd)

        if clone_result["exit_code"] == 0:
            # 安装依赖
            install_cmd = "cd spec-kit && pip install -e ."
            print(f"执行命令: {install_cmd}")
            install_result = self.execute_command(install_cmd)

            if install_result["exit_code"] == 0:
                # 创建符号链接
                link_cmd = "ln -sf /path/to/spec-kit/specify-cli /usr/local/bin/specify"
                print(f"执行命令: {link_cmd}")
                link_result = self.execute_command(link_cmd)

                if link_result["exit_code"] == 0:
                    print("✅ 源码安装成功！")
                    return {
                        "success": True,
                        "method": "source_installation",
                        "commands": [clone_cmd, install_cmd, link_cmd]
                    }
                else:
                    print(f"❌ 符号链接创建失败: {link_result['stderr']}")
                    return {
                        "success": False,
                        "error": link_result["stderr"],
                        "commands": [clone_cmd, install_cmd, link_cmd]
                    }
            else:
                print(f"❌ 依赖安装失败: {install_result['stderr']}")
                return {
                    "success": False,
                    "error": install_result["stderr"],
                    "commands": [clone_cmd, install_cmd]
                }
        else:
            print(f"❌ 仓库克隆失败: {clone_result['stderr']}")
            return {
                "success": False,
                "error": clone_result["stderr"]
            }

    def verify_installation(self) -> Dict[str, Any]:
        """验证安装结果"""
        print("🔍 验证SpecKit安装...")

        verification_steps = [
            {
                "name": "版本检查",
                "command": "specify --version",
                "expected": "specify-cli version"
            },
            {
                "name": "工具验证",
                "command": "specify check",
                "expected": "All checks passed"
            },
            {
                "name": "帮助信息",
                "command": "specify --help",
                "expected": "Usage: specify <command>"
            }
        ]

        verification_results = []
        all_passed = True

        for step in verification_steps:
            print(f"📋 {step['name']}...")
            result = self.execute_command(step["command"])

            if result["exit_code"] == 0 and step["expected"] in result["stdout"]:
                print(f"✅ {step['name']} - 通过")
                verification_results.append({
                    "step": step["name"],
                    "status": "passed",
                    "output": result["stdout"]
                })
            else:
                print(f"❌ {step['name']} - 失败")
                verification_results.append({
                    "step": step["name"],
                    "status": "failed",
                    "output": result.get("stderr", result.get("stdout", ""))
                })
                all_passed = False

        return {
            "all_passed": all_passed,
            "verification_results": verification_results,
            "installation_status": "verified" if all_passed else "failed"
        }

    def get_troubleshooting_guide(self) -> str:
        """获取故障排除指南"""
        return """
# SpecKit安装故障排除指南

## 常见问题及解决方案

### 环境问题
#### Python版本过低
**问题**: Python版本低于3.8
**症状**: 安装失败、运行时错误
**解决方案**:
```bash
# 检查Python版本
python3 --version

# Ubuntu/Debian
sudo apt update && sudo apt install python3.8

# CentOS/RHEL
sudo yum install python3.8

# macOS (使用Homebrew)
brew install python@3.11
```

#### 网络连接问题
**问题**: GitHub仓库无法访问
**症状**: 下载失败、连接超时、SSL证书错误
**解决方案**:
```bash
# 测试网络连接
ping github.com

# 使用镜像源
export GITHUB_MIRROR=https://mirror.ghproxy.com

# 配置代理（如需要）
export https_proxy=http://proxy.company.com:8080
export http_proxy=http://proxy.company.com:8080
```

#### 权限问题
**问题**: 安装权限不足
**症状**: Permission denied、写入权限错误
**解决方案**:
```bash
# 用户安装（推荐）
uv tool install --user specify-cli

# 管理员安装
sudo uv tool install specify-cli

# 手动设置权限
chmod +x ~/.local/bin/specify
```

### 依赖冲突
**问题**: 依赖包冲突、虚拟环境问题
**症状**: 安装失败、版本冲突
**解决方案**:
```bash
# 创建虚拟环境
python3 -m venv speckit-env
source speckit-env/bin/activate
pip install git+https://github.com/github/spec-kit.git

# 清理并重新安装
pip uninstall git+https://github.com/github/spec-kit.git
pip install git+https://github.com/github/spec-kit.git
```

### 平台特定问题

#### Windows权限问题
**问题**: PowerShell权限限制
**解决方案**:
```powershell
# 以管理员身份运行PowerShell
Start-Process PowerShell -Verb RunAs Administrator

# 或者使用用户安装
uv tool install --user specify-cli
```

#### macOS路径问题
**问题**: PATH环境变量配置
**解决方案**:
```bash
# 添加到shell配置文件
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 添加到shell配置文件
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

#### Linux依赖问题
**问题**: 系统依赖缺失
**解决方案**:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3-dev build-essential curl

# CentOS/RHEL
sudo yum groupinstall development
sudo yum install python3-devel
```

## 联系支持
### Windows
- PowerShell 5.1+
- Windows Subsystem for Linux (WSL)
- Git Bash (通过Git for Windows)

### macOS
- macOS 10.15+
- Homebrew包管理器
- MacPorts包管理器

### Linux
- Ubuntu 18.04+
- CentOS 7+
- Debian 11+
- Arch Linux
- OpenSUSE Leap

### 包管理器支持
- **uv** (推荐): 现代Python包管理器
- **pip**: 传统Python包管理器
- **conda**: 科学计算包管理器
- **poetry**: Python项目依赖管理器

## 联系要求详情

### 最低系统要求
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Python版本**: Python 3.8+
- **内存**: 至少2GB RAM
- **磁盘**: 至少1GB可用空间
- **网络**: 稳定的网络连接

### 推荐配置
- **CPU**: 2核或更多
- **内存**: 4GB或更多
- **网络**: 宽带网络连接
- **存储**: 10GB或更多
- **权限**: 管理员权限（全局安装）

### 性能优化
- **SSD存储**: 使用SSD提升I/O性能
- **缓存策略**: 启用包管理器缓存
- **并行安装**: 支持并行依赖安装
- **增量更新**: 仅更新必要的包

## 支持的SpecKit版本
- **最新稳定版**: v1.0.22
- **开发版**: v1.0.22-rc1
- **历史版本**: v0.9.0, v0.8.0等

## 更新和维护
### 升级SpecKit
```bash
# 使用uv升级
uv tool upgrade specify-cli

# 使用pip升级
pip install --upgrade git+https://github.com/github/spec-kit.git

# 重新安装最新版
uv tool install --force specify-cli --from git+https://github.com/github/spec-kit.git
```

### 查看版本信息
```bash
specify --version
specify check
```

### 卸级指南
1. 查看当前版本
2. 查看升级信息
3. 选择升级策略
4. 执行升级命令
5. 验证升级结果
6. 测试功能兼容性
```
"""

## 📊 输出要求

### 安装报告模板
```markdown
# SpecKit安装报告 - {{platform}}

## 📋 安装摘要
- **安装时间**: {{installation_time}}
- **使用方法**: {{installation_method}}
- **包管理器**: {{package_manager}}
- **SpecKit版本**: {{speckit_version}}
- **安装状态**: {{installation_status}}
- **执行平台**: {{platform}}

## 🤖 系统环境信息
- **操作系统**: {{os_name}} {{os_version}}
- **Python版本**: {{python_version}}
- **包管理器**: {{package_manager_version}}
- **架构**: {{architecture}}
- **内存**: {{memory_available}}

## 📦 安装步骤执行
{{installation_steps_table}}

## ✅ 验证结果
{{verification_results_table}}

## 🚀 后续配置建议
{{post_installation_recommendations}}

## 🔧 故障排除
{{troubleshooting_summary}}

## 📚 相关资源
- **官方文档**: https://github.com/github/spec-kit
- **安装指南**: https://github.com/github/spec-kit/blob/main/INSTALLATION.md
- **社区支持**: GitHub Discussions
- **问题反馈**: GitHub Issues
```

## 变量定义 (Variables)

| 变量名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|--------|
| {{installation_path}} | string | 是 | "" | 安装路径 |
| {{project_name}} | string | 是 | "" | 项目名称 |
| {{installation_method}} | string | 是 | "persistent" | 安装方法 |
| {{package_manager}} | string | 是 | "uv" | 包管理器 |
| {{platform}} | string | 是 | "auto" | 操作系统 |
| {{python_version}} | string | 是 | "" | Python版本 |
| {{speckit_version}} | string | 是 | "" | SpecKit版本 |

## 使用说明 (Usage)

### 基本安装流程
1. **环境检查**: 确保Python 3.8+
2. **选择方法**: 选择持久化或临时安装
3. **执行安装**: 运行相应的安装命令
4. **验证结果**: 验证安装成功
5. **开始使用**: 使用specify命令开始项目

### 快速开始
```bash
# 持久化安装（推荐）
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 临时使用（项目特定）
uvx --from git+https://github.com/github/spec-kit.git specify init my-project

# Docker安装
docker pull ghcr.io/github/spec-kit/spec-kit:latest
docker run -v $(pwd):/workspace ghcr.io/github/spec-kit/spec-kit:latest specify init my-project
```

### 项目初始化
```bash
# 创建新项目
specify init my-project

# 在现有项目中初始化
specify init . --ai claude

# 查看可用选项
specify init --help
```

---

**版本**: v1.3.0-installation-guide-enhanced
**创建时间**: 2025-12-28
**更新时间**: 2025-12-28
**维护者**: Terry
**执行级别**: 强制执行
**SpecKit合规**: 100%

**⚠️ 本提示词提供完整的SpecKit安装指南，确保用户能够顺利完成工具安装和配置。**
