<div align="center">

[🇺🇸 English](README_EN.md) | [🇨🇳 简体中文](README.md)

</div>

# 📚 Knowledge Absorber (知识吸收器)

> **通用 AI 技能模块** | 适用于 Trae, Claude, Gemini, VS Code Copilot 等环境

**Knowledge Absorber** 是一个独立的“外挂大脑”模块。它赋予 AI 助手深度阅读、解析长文档并生成结构化知识晶体（Markdown + HTML）的能力。

---

## 🚀 跨平台移植指南 (Portability Guide)

本模块设计为 **"文件夹级即插即用"**。
不同的 AI 助手通常会扫描项目根目录下的特定配置文件夹。为了让其他 AI (如 Claude 或 Gemini) 识别此技能，你只需要**修改父目录的名称**。

### 📂 目录结构适配

假设你把 `skills` 文件夹放在项目根目录：

1.  **在 Trae 中使用** (默认):
    ```text
    Project_Root/
    └── .trae/              <-- 保持原名
        └── skills/
            └── knowledge-absorber/
    ```

2.  **在 Claude Projects 中使用**:
    *   将 `.trae` 重命名为 `.claude` (或根据 Claude 的知识库规范放置)。
    *   或者直接告诉 Claude：“查看 `.claude/skills/` 下的文档”。
    ```text
    Project_Root/
    └── .claude/            <-- 重命名为 .claude
        └── skills/
            └── knowledge-absorber/
    ```

3.  **在 Gemini Advanced / AI Studio 中使用**:
    *   将 `.trae` 重命名为 `.gemini`。
    ```text
    Project_Root/
    └── .gemini/            <-- 重命名为 .gemini
        └── skills/
            └── knowledge-absorber/
    ```

4.  **在 VS Code (Copilot/Cline) 中使用**:
    ```text
    Project_Root/
    └── .vscode/            <-- 重命名为 .vscode
        └── skills/
            └── knowledge-absorber/
    ```

> **💡 核心原理**：AI 助手通常有权限读取隐藏文件夹（以 `.` 开头）。只要路径正确，并明确指示 AI “使用这个技能”，它就能工作。

---

## 🛠️ 安装与使用 (Installation & Usage)

### 第一步：环境准备
确保你的电脑安装了 Python 3.8+。
在 `knowledge-absorber` 目录下运行：
```bash
pip install -r requirements.txt
```

### 第二步：何时调用 (When to Activate)
不要为简单的 Google 搜索使用此技能。请在以下“高认知负载”场景召唤它：

1.  **啃大部头**：当你面对数百页的 PDF、技术框架文档（如 BMad, React 源码）或古籍时。
2.  **需要知识晶体**：当你不仅要一个简单的总结，而是要生成可永久存档、排版精美的 HTML 卡片时。
3.  **复杂文体处理**：例如需要“双文异构”处理（古文保留繁体，解释用简体）或特定技术栈的深度拆解。

### 第三步：调用机制 (Workflow)
你不需要手动运行复杂的命令行，只需在对话中**自然指令**，AI 会自动代理执行：

*   **用户指令示例**：
    > “帮我深度解析这个链接：`https://docs.bmad-method.org/`”
    > “读取 `manual.pdf` 并生成知识卡片。”

*   **AI 的执行逻辑**：
    1.  **摄取**：自动调用 `scripts/content_ingester.py` 抓取并清洗内容。
    2.  **透镜分析**：根据 `SKILL.md` 中的协议（如机械透镜、意义透镜）进行深度推理。
    3.  **交付**：自动生成 `.md`（深度笔记）和 `.html`（可视化卡片）文件。

---

## 📦 产出物 (Outputs)

该技能会自动生成两种格式的文件（位于 `data/` 目录）：

1.  **Markdown 深度笔记 (`.md`)**：
    *   包含元数据、核心概念破冰、深度拆解。
    *   支持“双文异构”（古文繁体/解释简体）或“技术栈模版”。
2.  **HTML 可视化卡片 (`.html`)**：
    *   精美的排版，适合分享或作为知识库归档。
    *   支持深色/浅色模式适配。

---

## 🤖 技能协议 (Skill Protocol)

核心逻辑定义在 `SKILL.md` 文件中。
如果你想修改 AI 的思考方式（例如修改解析的深度、改变输出风格），请直接编辑 `SKILL.md`。

> **维护者**: Little Code Sauce
> **版本**: v3.4.1 (Mixed Script Edition)
