<div align="center">

[🇺🇸 English](README_EN.md) | [🇨🇳 简体中文](README.md)

</div>

# 📚 Knowledge Absorber

> **Universal AI Skill Module** | Compatible with Trae, Claude, Gemini, VS Code Copilot, etc.

**Knowledge Absorber** is an independent "External Brain" module. It empowers AI assistants with the capability to deeply read, parse long documents, and generate structured knowledge crystals (Markdown + HTML).

---

## 🚀 Portability Guide

This module is designed to be **"Plug-and-Play at the Folder Level"**.
Different AI assistants usually scan specific configuration folders in the project root. To let other AIs (like Claude or Gemini) recognize this skill, you simply need to **rename the parent directory**.

### 📂 Directory Structure Adaptation

Assuming you place the `skills` folder in the project root:

1.  **For Trae** (Default):
    ```text
    Project_Root/
    └── .trae/              <-- Keep as is
        └── skills/
            └── knowledge-absorber/
    ```

2.  **For Claude Projects**:
    *   Rename `.trae` to `.claude` (or place according to Claude's knowledge base specs).
    *   Or directly tell Claude: "Check the docs under `.claude/skills/`".
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
    ```text
    Project_Root/
    └── .vscode/            <-- Rename to .vscode
        └── skills/
            └── knowledge-absorber/
    ```

> **💡 Core Principle**: AI assistants usually have permission to read hidden folders (starting with `.`). As long as the path is correct and you explicitly instruct the AI to "use this skill", it will work.

---

## � Core Features

### 1. Smart Ingestion
Adopts a **Four-Level Fallback Strategy** to ensure absolute stability in data acquisition:
- **Level 1 (Standard Requests)**: Millisecond-level fetching using Requests, minimal resource usage.
- **Level 2 (Browser Automation)**: Automatically invokes local Chrome/Edge (DrissionPage) to solve 403 errors, dynamic rendering, and simple captchas.
- **Level 3 (MCP Assist)**: Invokes system-level tools as a defense line.
- **Level 4 (Manual Fallback)**: Provides clear guidance to support user manual import of HTML/PDF.

### 2. Deep Purification
Automatically performs "noise reduction" before analysis, ensuring the AI focuses only on core content:
- **UI Cleaning**: Removes login modals, sidebars, footer navigation.
- **Commercial Cleaning**: Filters paywall prompts, ad banners, membership promotion info.

### 3. Multi-Dimensional Cognitive Lenses
Automatically switches analysis models based on content attributes (see `SKILL.md` for details):
- **Mechanistic Lens**: Deconstructs technical principles (How it works).
- **Hermeneutic Lens**: Analyzes humanistic context (Context & Origin).
- **Behavioral Lens**: Digs into social incentives (Incentives).
- **Pragmatic Lens**: Distills business manuals (Actionable Items).

---

## 🛠️ Installation & Configuration

### Environment Preparation
Ensure Python 3.8+ is installed, and run the following in the `knowledge-absorber` directory:
```bash
pip install -r requirements.txt
```
*(Note: To use DrissionPage automation, ensure Chrome or Edge browser is installed locally)*

---

## 💡 When to Activate

Please activate this skill in the following scenarios:

1.  **Explicit Learning Instructions**:
    - User explicitly asks: "Learn this", "Deep analysis", "Deep learning", "Parse", "Explain this concept", "Save to knowledge base".
    - User asks: "Explain this clearly", "Teach me how to use", "Summarize and generate notes".
    - Keyword trigger: Whenever the user mentions "learn" or "analyze" with an object.

2.  **Complex Multi-Modal Input**:
    - User provides one or more URL links (especially those with heavy info or images).
    - User uploads document files (PDF, Word, Markdown, TXT).
    - User uploads images (PNG, JPG) containing dense text or charts (e.g., architecture diagrams, mind maps).
    - Mixed input: Contains links, text descriptions, and images simultaneously.

3.  **Deep Code Analysis**:
    - User selects or uploads code files and asks: "How does this code run?", "What is the architecture?".

4.  **Implicit Teaching Needs**:
    - User expresses confusion: "I don't understand this concept", "It's too hard, I don't get it".
    - User needs simplification: "Explain in plain language", "Give a beginner-friendly example".

---

## 🔄 Workflow

You simply issue natural commands in the chat, and the AI will automatically proxy the execution:

*   **Command Examples**:
    > "Help me deeply parse this link: `https://...`"
    > "Read `manual.pdf` and generate knowledge cards."

*   **Execution Logic**:
    1.  **Ingestion**: Script automatically attempts Requests -> Drission -> MCP.
    2.  **Purification**: Removes all non-content elements (Login/Ads).
    3.  **Analysis**: Applies cognitive lenses for deep reasoning.
    4.  **Delivery**: Generates high-density notes.

---

## 📦 Outputs

The skill automatically generates files in two formats (located in the `data/` directory):

1.  **Markdown Deep Notes (`.md`)**: Contains metadata, core concept ice-breaking, and deep deconstruction.
    *   Supports "Dual-Script Architecture" (Traditional for classics / Simplified for explanation) or "Tech Stack Templates".
2.  **HTML Visual Cards (`.html`)**: Beautifully formatted files suitable for sharing or archiving.
    *   Supports Dark/Light mode adaptation.
3.  **Raw Data (`raw_content.txt`)**: Cleaned plain text backup.

---

## 🤖 Skill Protocol

The core logic is defined in the `SKILL.md` file. If you need to modify the AI's thinking depth or output style, please edit that file directly.
