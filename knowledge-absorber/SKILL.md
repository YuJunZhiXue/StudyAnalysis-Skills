---
name: knowledge-absorber
description: 深度解析链接、文档或代码，生成“全能导师级”的教学笔记（零基础直达精通）。
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
    "knowledge-absorber"
  ]
version: 4.0.0
author: Little Code Sauce
---

# 核心流程 (Core Workflow)

本技能采用 **三级加载机制 (Level-3 Loading)** 以优化上下文消耗。请严格按照以下步骤执行。

## 第一步：智能摄取 (Content Ingestion)

先运行脚本获取干净的 Markdown 数据。脚本会自动清洗 HTML 噪音。

1.  **运行摄取脚本**：
    - **Command**: `python .trae/skills/knowledge-absorber/scripts/content_ingester.py "INPUT_URL_OR_PATH"`
    - **依赖检查**: 首次运行若报错，请提示用户安装依赖。

2.  **读取结果**：
    - 读取 `.trae/skills/knowledge-absorber/config/raw_content.txt`。
    - 该文件已通过 `html2text` 清洗，可直接用于分析。

## 第二步：加载导师人格 (Load Persona)

读取系统提示词以激活“首席认知架构师”人格。

1.  **加载 Prompt**：
    - **Command**: `cat .trae/skills/knowledge-absorber/references/system_prompt.md`
    - **注意**：将读取到的内容作为 System Prompt 注入当前上下文。

## 第三步：生成教学内容 (Generate Content)

根据 `raw_content.txt` 的内容和 `system_prompt.md` 的指示，生成双模态输出。

1.  **评估模式**：
    - 根据内容体量选择 **Instant Mode** (单篇) 或 **Series Mode** (系列)。
    - 参考 `system_prompt.md` 中的“思维透镜”进行分析。

2.  **生成与写入**：
    - 必须同时生成 Markdown 和 HTML 文件。
    - 写入位置：项目根目录下的独立文件夹 `knowledge_{YYYYMMDD}_{Title}/`
    - 文件名格式：`knowledge_{YYYYMMDD}_{Title}.md/html`
