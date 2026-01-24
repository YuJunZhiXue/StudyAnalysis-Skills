---
name: knowledge-absorber
description: 深度解析链接、文档或代码，生成“全能导师级”的教学笔记（零基础直达精通）。具备“真理锚定”校验能力，自动识别幻觉与过时信息。
tags: ["learning","学习","analysis","分析","documentation","文档","knowledge-base","知识库","architecture","知识吸收","knowledge-absorber","verification",]
version: 4.1.0
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

## 第二步：真理锚定 (Truth Anchoring)

**“不要轻信任何文本，哪怕它看起来很专业。”**
在加载导师人格之前，必须先对摄取的内容进行**准确性校验**。

1.  **提取核心主张 (Claim Extraction)**：
    - 快速扫描 `raw_content.txt`。
    - 提取 3-5 个**关键事实性主张**（Key Factual Claims）。
      - _重点关注_：具体数据、代码API用法、历史事件、绝对化论断（"总是"、"从未"）。

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

根据 `raw_content.txt` 的内容、`system_prompt.md` 的指示以及**第二步的校准报告**，生成多模态输出。

1.  **结构化输出 (必填项)**：
    - **【⚠️ 认知校准】**：对比“原文主张”与“2026最新事实”。
    - **【🧠 认知地图】**：**强制生成 Mermaid 流程图/思维导图代码**。
    - **【🚀 避坑指南】**：总结 3 个最容易犯的错误与“避雷针”方案。
    - **【💡 深度链接】**：分析多源输入之间的冲突或互补。
    - **【透镜解析】**：**必须严格按照 `system_prompt.md` 中的“七维全息透镜”进行裂变式解析。**
    - **【通用架构】**：**必须包含 `TL;DR`、`认知挂钩`、`概念破冰`、`核心解构`、`实操指南`、`巩固答疑` 等模块。**

2.  **生成与写入**：
    - 必须同时生成 Markdown 和 HTML 文件。
    - 写入位置：项目根目录下的独立文件夹 `knowledge_{YYYYMMDD}_{Title}/`
    - 文件名格式：`knowledge_{YYYYMMDD}_{Title}.md/html`
    
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