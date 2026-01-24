---
name: knowledge-absorber
description: 深度解析链接、文档或代码，生成“全能导师级”的教学笔记（零基础直达精通）。具备“真理锚定”校验能力，自动识别幻觉与过时信息。
tags:
  [
    "learning",
    "学习",
    "analysis",
    "分析",
    "documentation",
    "文档",
    "knowledge-base",
    "知识库",
    "architecture",
    "知识吸收",
    "knowledge-absorber",
    "verification"
  ]
version: 4.1.0
author: 叫我小杨同学的小码酱
---

# 核心流程 (Core Workflow)

本技能采用 **三级加载机制 (Level-3 Loading)** 配合 **真理锚定协议 (Truth Anchoring Protocol)**。请严格按照以下步骤执行。

## 第一步：智能摄取 (Content Ingestion)

先运行脚本获取干净的 Markdown 数据。脚本会自动清洗 HTML 噪音并处理多模态内容（PDF/OCR）。

1.  **运行摄取脚本**：
    - **Command**: `python [SKILL_PATH]/scripts/content_ingester.py "INPUT_URL_OR_PATH"`
    - **注意**: `[SKILL_PATH]` 是本技能所在的实际路径（如 `.trae/skills/knowledge-absorber/`）。
    - **依赖检查**: 首次运行若报错，请提示用户安装依赖。

2.  **读取结果**：
    - 读取 `[SKILL_PATH]/config/raw_content.txt`。
    - 该文件已通过 `html2text` 清洗，可直接用于分析。

## 第二步：真理锚定 (Truth Anchoring) [✨核心升级]

**“不要轻信任何文本，哪怕它看起来很专业。”**
在加载导师人格之前，必须先对摄取的内容进行**准确性校验**。

1.  **提取核心主张 (Claim Extraction)**：
    - 快速扫描 `raw_content.txt`。
    - 提取 3-5 个**关键事实性主张**（Key Factual Claims）。
      - *重点关注*：具体数据、代码API用法、历史事件、绝对化论断（"总是"、"从未"）。

2.  **联网审计 (Web Audit)**：
    - **Tool**: 调用 `WebSearch`。
    - **Query**: 针对每个主张构造验证性搜索（例如："React 19 useEffect changes 2026", "Python 3.14 features verification"）。
    - **Constraint**: 必须包含当前年份（2026）以确保时效性。

3.  **生成校准报告 (Calibration Report)**：
    - 在心中构建一个“红队报告”。
    - 如果发现原文有误、过时或存在争议，**必须**在后续生成的教学笔记中显式标注。

## 第三步：加载导师人格 (Load Persona)

读取系统提示词以激活“首席认知架构师”人格。

1.  **加载 Prompt**：
    - **Command**: `cat [SKILL_PATH]/references/system_prompt.md`
    - **注意**：将读取到的内容作为 System Prompt 注入当前上下文。

## 第四步：生成教学内容 (Generate Content)

根据 `raw_content.txt` 的内容、`system_prompt.md` 的指示以及**第二步的校准报告**，生成双模态输出。

1.  **结构化输出**：
    - **【⚠️ 认知校准】模块**（如果存在事实错误，必须放在文章最开头）。
    - **正文解析**（按照导师风格）。

2.  **生成与写入**：
    - 必须同时生成 Markdown 和 HTML 文件。
    - 写入位置：项目根目录下的独立文件夹 `knowledge_{YYYYMMDD}_{Title}/`
    - 文件名格式：`knowledge_{YYYYMMDD}_{Title}.md/html`
