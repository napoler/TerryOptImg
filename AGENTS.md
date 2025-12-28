# AGENTS.md - Image Optimizer Project Constitution

## 核心原则 (Core Principles)
1. **功能复刻 (Functional Replication)**: Must replicate Curtail's core features (compression, resizing, format conversion).
2. **用户体验 (User Experience)**: GUI must be responsive and provide feedback.
3. **数据安全 (Data Safety)**: Default to non-destructive operations.
4. **高性能 (High Performance)**: Utilize concurrency.

## 技术约束 (Technical Constraints)
- **Language**: Python 3.8+
- **GUI**: Tkinter
- **Deps**: Pillow, tqdm
- **External**: `jpegoptim`, `pngquant` (optional)

## 质量门禁 (Quality Gates)
- **Spec Compliance**: All code must reference Functional Requirements (FRs).
- **Verification**: All features must be verified.
- **Documentation**: Changes must be reflected in `docs/IMAGE_OPTIMIZER_SPEC.md`.

## 标准操作流程 (SOP)
所有 Agent 必须严格遵循 SpecKit 命令流：
1. **Define**: `@/speckit.constitution`
2. **Specify**: `@/speckit.specify`
3. **Plan**: `@/speckit.plan`
4. **Tasks**: `@/speckit.tasks`
5. **Implement**: `@/speckit.implement`
