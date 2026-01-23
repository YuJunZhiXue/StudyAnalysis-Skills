<div align="center">

[🇺🇸 English](README_EN.md) | [🇨🇳 简体中文](README.md)

</div>

# 📚 Knowledge Absorber (知识吸收器)

> **通用 AI 深度学习与知识萃取模块** | 适配 Trae, Claude, Gemini, VS Code Copilot 等主流环境

**Knowledge Absorber** 是一个为 AI 助手打造的“深度阅读外挂”。它通过自动化工具链将杂乱的网页、文档、图片瞬间转化为结构化、高密度的“知识晶体”，帮助 AI 突破长文本理解与多模态解析的局限。

---

## 版本更新 (Latest Updates)

### 1. ⚡ 自动化依赖自愈 (Self-Healing)
- **新增**: 脚本内置 `AUTO-DEPENDENCY INSTALLER`。首次运行或缺少库时，脚本会自动读取 `requirements.txt` 并静默安装，无需手动干预。

### 2. �️ 多模态深度解析 (Multimodal Deep Parsing)
- **OCR 强化**: 集成 `RapidOCR`，支持对网页图片、本地图片、PDF/Docx 内嵌图片的自动化识别与提取。
- **全格式支持**: 新增对 `.doc` (自动调用 Word 转换)、`.docx`、`.pdf`、`.jpg/png/bmp` 的原生解析能力。

### 3. 🛡️ 四级智能降级摄取 (Level-4 Ingestion)
- **Level 1 (Requests)**: 极速抓取。
- **Level 2 (DrissionPage)**: 自动化浏览器驱动，绕过 JS 动态加载与基础反爬。
- **Level 3 (MCP Protocol)**: 调用系统级工具作为后备。
- **Level 4 (Manual)**: 智能引导用户导入。

### 4. � 七维全息思维透镜 (7D Cognitive Lenses)
- **维度裂变**: 从“意念、物质、关系、行动”四个世界出发，提供诠释、演化、机械、系统、行为、对抗、实用七大维度分析逻辑，确保知识解析无死角。

---

## 🚀 快速上手 (Quick Start)

### 📂 目录结构
```text
knowledge-absorber/
├── scripts/             # 核心脚本 (内置自愈安装逻辑)
├── references/          # 7D 思维透镜协议 (system_prompt.md)
├── config/              # [自动生成] 存放抓取后的原始文本 (raw_content.txt)
├── SKILL.md             # 技能激活协议 (跨平台路径已解耦)
└── requirements.txt     # 核心依赖清单
```

### 🛠️ 环境准备
1. 安装 Python 3.8+。
2. 建议安装 Chrome/Edge 浏览器（用于 Level 2 抓取）。
3. **运行**: 直接运行脚本即可，依赖将自动补全：
   ```bash
   python scripts/content_ingester.py "https://example.com"
   ```

### 💡 指令示例
- *"深度解析这个网页：https://example.com"*
- *"读取这个 PDF 并帮我生成知识笔记"*
- *"分析这张架构图里的核心逻辑"*

---

## 🚀 跨平台移植 (Portability)
本模块支持 **"文件夹级即插即用"**。
移植到不同环境（如从 Trae 到 Claude）时，请注意：
1. **路径解耦**: `SKILL.md` 中已使用 `[SKILL_PATH]` 占位符。请在使用时确保 AI 知道该路径，或将其替换为实际的绝对路径。
2. **位置**: 
   - **Trae**: `.trae/skills/`
   - **Claude**: `.claude/skills/`
   - **Gemini**: `.gemini/skills/`

---

## 📦 产出成果 (Outputs)
生成的笔记将存放在项目根目录下的 `knowledge_{date}_{title}/` 文件夹中：
1.  **Markdown 深度笔记 (`.md`)**: 含 ASCII 字符画演示与 7D 深度解析。
2.  **HTML 可视化卡片 (`.html`)**: 内置 Mermaid 流程图与自适应样式。
3.  **原始文本 (`config/raw_content.txt`)**: 经降噪后的纯净数据。

---

## 🤝 贡献与反馈
如果你觉得好用，请给个 Star！⭐ 
如有问题，欢迎提交 Issue。

---
<div align="center">
Made with ❤️ for Learners
</div>
