# iflow.md - Workflow & Specification

## 规范 (Specification)
See `docs/IMAGE_OPTIMIZER_SPEC.md` for full details.

### Functional Requirements
- **FR-001**: 智能图像压缩 (Smart Compression)
- **FR-002**: 智能图像缩放 (Smart Resizing)
- **FR-003**: 多格式转换 (Format Conversion)
- **FR-004**: 图形用户界面 (GUI)
- **FR-005**: 高并发处理 (Concurrency)

## 流程 (Workflow)
1. **Design**: Update `docs/IMAGE_OPTIMIZER_SPEC.md`.
2. **Plan**: Define tasks.
3. **Implement**: Write code in `src/`.
4. **Verify**: Test and Update Reports.

## 任务清单 (Tasks)
### Phase 1: MVP (Completed)
- [x] T-001: 核心逻辑实现
- [x] T-002: CLI 实现
- [x] T-003: GUI 实现
- [x] T-004: 多线程机制
- [x] T-005: 文档同步

### Phase 2: GUI Optimization & High Availability (Completed)
- [x] T-006: 配置持久化 (ConfigManager)
- [x] T-007: 任务控制 (Cancel Button)
- [x] T-008: 错误隔离与日志优化 (Error Handling)

### Phase 3: Smart Concurrency (Completed)
- [x] T-010: 智能默认线程数 (CPU Count)
- [x] T-011: 限制 UI 最大线程数
- [x] T-012: 低负载模式 (Low Resource Mode)

## SpecKit 核心功能命令 (Core Commands)

### 🎯 四阶段核心工作流
| 阶段 | 命令 | 用途 |
|------|------|------|
| 1️⃣ | `@/speckit.specify` | 将功能需求转化为清晰的规范文档 |
| 2️⃣ | `@/speckit.plan` | 制定功能的技术实现方案 |
| 3️⃣ | `@/speckit.tasks` | 将技术方案分解为可执行的任务清单 |
| 4️⃣ | `@/speckit.implement` | 按任务清单逐步实现功能代码 |

### 🔧 辅助命令
| 命令 | 用途 | 使用时机 |
|------|------|----------|
| `@/speckit.constitution` | 定义项目的核心原则和开发规范 | 项目开始时（可选） |
| `@/speckit.clarify` | 解决规范中的模糊和歧义问题 | 规范化后（可选） |
| `@/speckit.analyze` | 检查规范、计划、任务的一致性 | 实现前（可选） |
| `@/speckit.checklist` | 生成需求质量验证清单 | 任何阶段 |
