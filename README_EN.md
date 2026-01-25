<div align="center">

# 📚 Knowledge Absorber

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version: 4.0.0](https://img.shields.io/badge/Version-4.0.0-green.svg)](CHANGELOG.md)

**Universal AI Skill Module | Compatible with Trae, Claude, Gemini, VS Code Copilot, etc.**

[🇺🇸 English](README_EN.md) | [🇨🇳 简体中文](README.md)

---

**Knowledge Absorber** is an independent "External Brain" module. It empowers AI agents with the ability to deeply read long documents, analyze complex content, and generate structured "Knowledge Crystals" (Markdown + HTML).

</div>

---

## 🚀 What's New

> **v4.0.0 "Mixed Script Edition"**

- **⚡ High-Speed Concurrent Engine**: Introduced `ThreadPoolExecutor` and `threading.Lock` for simultaneous scraping of multiple links/files, improving processing efficiency by 300%+.
- **🎨 Visual Progress System**: Integrated `Rich` library for high-contrast color tracking, providing a clear task board and real-time progress feedback in the terminal.
- **⚓ Truth Anchoring Protocol**: Added `【💡 Deep Linking】` analysis to automatically identify factual conflicts or complementarities across multiple sources.
- **🔍 Deep Protocol Alignment**: Mandatory integration of the "Seven Holographic Lenses" protocol, ensuring outputs include "Mind Maps" and "Pitfall Guides".
- **🛡️ Enhanced Robustness**: Optimized SSL verification for offline testing and added auto-fix for character encoding issues (Mojibake) on major platforms.
- **⚛️ Deep Fission Module**: Added atomic-level contradiction analysis and version archeology module to reveal counter-intuitive conclusions (Style: `.fission-section`).
- **🔍 Strict Search Filter**: Upgraded HTML interaction; search box now **strictly hides** non-matching content blocks instead of just highlighting, providing a focused reading experience.
- **🛡️ Mermaid Safety Protocol**: Built-in syntax auto-correction mechanism that forcibly escapes special characters to prevent diagram rendering crashes.

---

## 📂 Portability Guide

This module is designed for **"Folder-Level Plug & Play"**.
AI assistants typically scan specific configuration folders in the project root. To let other AIs (like Claude or Gemini) recognize this skill, you simply need to **rename the parent directory**.

### 📂 Directory Structure Adaptation

Assuming your `skills` folder is located at the project root:

1.  **For Trae** (Default):
    ```text
    Project_Root/
    └── .trae/              <-- Keep original name
        └── skills/
            └── knowledge-absorber/
    ```

2.  **For Claude Projects**:
    *   Rename `.trae` to `.claude`.
    ```text
    Project_Root/
    └── .claude/            <-- Rename to .claude
        └── skills/
            └── knowledge-absorber/
    ```

3.  **For Gemini Advanced / AI Studio**:
    *   Rename `.trae` to `.gemini`.
    ```text
    Project_Root/
    └── .gemini/            <-- Rename to .gemini
        └── skills/
            └── knowledge-absorber/
    ```

4.  **For VS Code (Copilot/Cline)**:
    *   Rename `.trae` to `.vscode`.
    ```text
    Project_Root/
    └── .vscode/            <-- Rename to .vscode
        └── skills/
            └── knowledge-absorber/
    ```

> **💡 Core Principle**: AI agents usually have permission to read hidden folders (starting with `.`). As long as the path is correct and you explicitly instruct the AI to "use this skill", it will work.

---

## 🛠️ Installation & Usage

### Step 1: Environment Preparation
Ensure Python 3.8+ is installed on your machine.
Run the following command in the `knowledge-absorber` directory:
```bash
pip install -r requirements.txt
```

### Step 2: When to Activate
Do not use this skill for simple Google searches. Summon it for **"High Cognitive Load"** scenarios:

1.  **Heavy Lifting**: When facing hundreds of pages of PDFs, technical framework docs (e.g., BMad, React Source), or ancient texts.
2.  **Knowledge Crystals Needed**: When you need more than a simple summary—you need a beautifully formatted, archivable HTML card.
3.  **Cross-Source Analysis**: When you need to scrape and compare multiple links (e.g., Zhihu + Blog + Official Docs) for deep Truth Anchoring.

### Step 3: Workflow
You don't need to manually run complex command-line instructions. Just use **Natural Language** in the chat, and the AI will proxy the execution:

*   **User Instruction Examples**:
    > "Help me deeply analyze this link: `https://docs.bmad-method.org/`"
    > "Read `manual.pdf` and apply the [Mechanistic Lens] to generate knowledge cards."

*   **AI Execution Logic**:
    1.  **Ingestion**: Automatically calls `scripts/content_ingester.py` to scrape and clean content concurrently.
    2.  **Lens Analysis**: Applies deep reasoning based on protocols defined in `SKILL.md` (e.g., Mechanistic Lens, Evolution Lens).
    3.  **Delivery**: Automatically generates `.md` (Deep Notes) and `.html` (Visual Cards).

---

## 📦 Outputs

This skill automatically generates files in two formats (located in the `data/` directory):

1.  **Markdown Deep Notes (`.md`)**:
    *   Includes metadata, concept icebreaking, deep deconstruction, mind maps, and pitfall guides.
    *   Supports "Mixed Script Protocol" (Traditional/Simplified) or "Tech Stack Templates".
2.  **HTML Visual Cards (`.html`)**:
    *   Beautiful formatting, perfect for sharing or archiving in a knowledge base.
    *   Supports Dark/Light mode adaptation, with perfected code highlighting and Mermaid diagram display.

---

## 🤖 Skill Protocol

The core logic is defined in the `SKILL.md` file.
If you want to modify the AI's way of thinking (e.g., changing the depth of analysis or output style), please edit `SKILL.md` directly.

---

> **Maintainer**: Little Code Sauce
> **Version**: v4.0.0 (Mixed Script Edition)
