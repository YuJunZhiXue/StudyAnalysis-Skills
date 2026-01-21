<div align="center">

[🇺🇸 English](README_EN.md) | [🇨🇳 简体中文](README.md)

</div>

# 📚 Knowledge Absorber (知识吸收器)

> **通用 AI 技能模块** | 适用于 Trae, Claude, Gemini, VS Code Copilot 等环境

**Knowledge Absorber** 是一个独立的“外挂大脑”模块。它赋予 AI 助手深度阅读、解析长文档并生成结构化知识晶体（Markdown + HTML）的能力。
只是用来分析总结你分享的内容，如果只有一个网页那只会分析这一个网页的内容

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
    - 将 `.trae` 重命名为 `.claude` (或根据 Claude 的知识库规范放置)。
    - 或者直接告诉 Claude：“查看 `.claude/skills/` 下的文档”。

    ```text
    Project_Root/
    └── .claude/            <-- 重命名为 .claude
        └── skills/
            └── knowledge-absorber/
    ```

3.  **在 Gemini Advanced / AI Studio 中使用**:
    - 将 `.trae` 重命名为 `.gemini`。

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

## 🚀 核心功能 (Core Features)

### 1. 智能数据摄取 (Smart Ingestion)

采用 **四级降级策略**，确保数据获取的绝对稳定性：

- **Level 1 (标准请求)**: 使用 Requests 进行毫秒级抓取，资源占用极低。
- **Level 2 (浏览器自动化)**: 自动调用本地 Chrome/Edge (DrissionPage)，解决 403、动态渲染及简单验证码。
- **Level 3 (MCP 辅助)**: 调用系统级工具作为防线。
- **Level 4 (手动兜底)**: 提供明确指引，支持用户手动导入 HTML/PDF。

### 2. 深度降噪与清洗 (Deep Purification)

在分析前自动执行“去噪”处理，确保 AI 仅聚焦于核心内容：

- **UI 清洗**: 剔除登录弹窗、侧边栏、页脚导航。
- **商业清洗**: 过滤付费提示、广告横幅、会员推广信息。

### 3. 多维思维透镜 (Cognitive Lenses)

根据内容属性自动切换分析模型 (详见 `SKILL.md`)：

- **机制透镜**: 拆解技术原理 (How it works)。
- **意义透镜**: 解析人文脉络 (Context)。
- **行为透镜**: 挖掘社科动机 (Incentives)。
- **行动透镜**: 提炼商业手册 (Actionable Items)。

## 🛠️ 安装与配置 (Installation)

### 环境准备

确保安装 Python 3.8+，并在 `knowledge-absorber` 目录下运行：

```bash
pip install -r requirements.txt
```

_(注意：如需使用 DrissionPage 自动化，请确保本地已安装 Chrome 或 Edge 浏览器)_

---

## 💡 何时调用 (When to Activate)

# 何时调用 (When to use)

当出现以下任一场景时，请立即激活本技能：

1.  **显式学习指令**：
    - 用户明确要求：“学习这个”、“深度分析”、“深度学习”、“解析”、“解释这个概念”、“存入知识库”。
    - 用户要求：“把这个讲清楚”、“教我怎么用”、“总结并生成笔记”。
    - 关键词触发：只要用户提到“学习”或“分析”配合某个对象，必须激活。

2.  **复杂多模态输入**：
    - 用户提供了一个或多个 URL 链接（尤其是包含大量信息或图片的链接）。
    - 用户上传了文档文件（PDF, Word, Markdown, TXT）。
    - 用户上传了图片（PNG, JPG），且图片内容包含大量文字或图表（如架构图、思维导图）。
    - 混合输入：同时包含链接、文字描述和图片。

3.  **代码深度解析**：
    - 用户选中或上传了代码文件，并询问：“这段代码是怎么跑的？”、“架构是怎样的？”。

4.  **隐式教学需求**：
    - 用户表示困惑：“我不理解这个概念”、“太难了，看不懂”。
    - 用户需要降维打击：“用大白话解释一下”、“给个小白能懂的例子”。

## 🔄 工作流 (Workflow)

你只需在对话中下达自然指令，AI 将自动代理执行：

- **指令示例**：

  > “帮我深度解析这个链接：`https://...`”
  > “读取 `manual.pdf` 并生成知识卡片。”

- **执行逻辑**：
  1.  **摄取**: 脚本自动尝试 Requests -> Drission -> MCP。
  2.  **清洗**: 移除所有非内容元素 (登录/广告)。
  3.  **分析**: 运用思维透镜进行深度推理。
  4.  **交付**: 生成高密度笔记。


---

## 📦 产出物 (Outputs)


如果出现调用浏览器的情况，那是因为反爬机制才会这样，无需操作等待结束即可！！！

该技能会自动生成两种格式的文件（位于 `data/` 目录）：

1.  **Markdown 深度笔记 (`.md`)**：
    *   包含元数据、核心概念破冰、深度拆解。
    *   支持“双文异构”（古文繁体/解释简体）或“技术栈模版”。
2.  **HTML 可视化卡片 (`.html`)**：
    *   精美的排版，适合分享或作为知识库归档。
    *   支持深色/浅色模式适配。
3.  **原始数据 (`raw_content.txt`)**: 经过清洗的纯净文本备份。

---

## 🤖 技能协议 (Skill Protocol)

核心逻辑定义在 `SKILL.md` 文件中。如需修改 AI 的思考深度或输出风格，请直接编辑该文件。
