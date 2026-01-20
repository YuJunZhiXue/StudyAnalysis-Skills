<div align="center">

[🇺🇸 English](README_EN.md) | [🇨🇳 简体中文](README.md)

</div>

# 📚 Knowledge Absorber

> **Universal AI Skill Module** | Compatible with Trae, Claude, Gemini, VS Code Copilot, etc.

**Knowledge Absorber** is an independent "External Brain" module. It empowers AI agents with the ability to deeply read long documents, analyze complex content, and generate structured "Knowledge Crystals" (Markdown + HTML).

---

## 🚀 Portability Guide

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
    *   Rename `.trae` to `.claude` (or place it according to Claude's knowledge base norms).
    *   Or simply instruct Claude: "Check the documents under `.claude/skills/`".
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
3.  **Complex Text Processing**: E.g., "Mixed Script Protocol" (Traditional Chinese for original text, Simplified for analysis) or deep deconstruction of specific tech stacks.

### Step 3: Workflow
You don't need to manually run complex command-line instructions. Just use **Natural Language** in the chat, and the AI will proxy the execution:

*   **User Instruction Examples**:
    > "Help me deeply analyze this link: `https://docs.bmad-method.org/`"
    > "Read `manual.pdf` and generate knowledge cards."

*   **AI Execution Logic**:
    1.  **Ingestion**: Automatically calls `scripts/content_ingester.py` to scrape and clean content.
    2.  **Lens Analysis**: Applies deep reasoning based on protocols defined in `SKILL.md` (e.g., Mechanistic Lens, Meaning Lens).
    3.  **Delivery**: Automatically generates `.md` (Deep Notes) and `.html` (Visual Cards).

---

## 📦 Outputs

This skill automatically generates files in two formats (located in the `data/` directory):

1.  **Markdown Deep Notes (`.md`)**:
    *   Includes metadata, concept icebreaking, and deep deconstruction.
    *   Supports "Mixed Script Protocol" or "Tech Stack Templates".
2.  **HTML Visual Cards (`.html`)**:
    *   Beautifully typeset, suitable for sharing or knowledge base archiving.
    *   Supports Dark/Light mode adaptation.

---

## 🤖 Skill Protocol

The core logic is defined in the `SKILL.md` file.
If you want to modify the AI's thinking process (e.g., change the depth of analysis or output style), please edit `SKILL.md` directly.

> **Maintainer**: Little Code Sauce
> **Version**: v3.4.1 (Mixed Script Edition)
