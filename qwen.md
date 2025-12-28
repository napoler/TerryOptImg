# qwen.md - Agent Instructions

## Interaction Rules
1. **Language**: Always use **Chinese (中文)** for interaction unless specified otherwise.
2. **Methodology**: Follow **SpecKit** methodology (Document-Driven Development).
3. **References**: Always check `docs/IMAGE_OPTIMIZER_SPEC.md` before coding.
4. **Workflow**: Use standard SpecKit commands (`@/speckit.specify`, etc.) to guide the user through the development process.

## Coding Style
- Add `@spec: FR-XXX` annotations to classes and major functions.
- Use Type Hints.
- Write docstrings in English or Chinese (consistent with project).
