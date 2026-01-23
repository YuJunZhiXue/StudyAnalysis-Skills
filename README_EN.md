<div align="center">

[🇺🇸 English](README_EN.md) | [🇨🇳 简体中文](README.md)

</div>

# 📚 Knowledge Absorber

> **Universal AI Deep Learning & Knowledge Extraction Module** | Compatible with Trae, Claude, Gemini, VS Code Copilot, etc.

**Knowledge Absorber** is an "External Brain" designed for AI assistants. It automates the transformation of messy web pages, documents, and images into structured, high-density "Knowledge Crystals," breaking the limitations of long-context understanding and multimodal parsing.

---

## 🆕 Latest Updates

### 1. ⚡ Self-Healing Dependencies
- **New**: Built-in `AUTO-DEPENDENCY INSTALLER`. The script automatically reads `requirements.txt` and silently installs missing libraries on its first run, eliminating manual setup.

### 2. 👁️ Multimodal Deep Parsing
- **OCR Enhanced**: Integrated `RapidOCR` for automated text extraction from web images, local photos, and embedded images within PDF/Docx files.
- **Full Format Support**: Native parsing for `.doc` (via Word conversion), `.docx`, `.pdf`, and `.jpg/png/bmp`.

### 3. 🛡️ Level-4 Smart Ingestion
- **Level 1 (Requests)**: Turbo fetching.
- **Level 2 (DrissionPage)**: Automated browser driver to bypass JS rendering and basic anti-scraping.
- **Level 3 (MCP Protocol)**: System-level tools as a fallback.
- **Level 4 (Manual)**: Intelligent user-guided import.

### 4. 🧠 7D Cognitive Lenses
- **Dimension Fission**: Analyzes knowledge through the "Seven-Sided Prism" (Hermeneutic, Evolutionary, Mechanistic, Systemic, Behavioral, Adversarial, Pragmatic) across four cognitive worlds.

---

## 🚀 Quick Start

### 📂 Directory Structure
```text
knowledge-absorber/
├── scripts/             # Core scripts (with self-healing logic)
├── references/          # 7D Cognitive Lens Protocol (system_prompt.md)
├── config/              # [Auto-generated] Cleaned raw text (raw_content.txt)
├── SKILL.md             # Skill activation protocol (Path decoupled)
└── requirements.txt     # Core dependencies
```

### 🛠️ Environment Preparation
1. Ensure Python 3.8+ is installed.
2. Chrome or Edge browser is recommended (for Level 2 Ingestion).
3. **Run**: Just execute the script; dependencies will auto-install:
   ```bash
   python scripts/content_ingester.py "https://example.com"
   ```

### 💡 Examples
- *"Deeply parse this webpage: https://example.com"*
- *"Read this PDF and generate knowledge notes"*
- *"Analyze the core logic in this architecture diagram (image)"*

---

## 🚀 Portability
This module supports **"Folder-Level Plug-and-Play."**
When porting between environments (e.g., Trae to Claude):
1. **Path Decoupling**: `SKILL.md` uses a `[SKILL_PATH]` placeholder. Ensure your AI knows this path or replace it with the actual absolute path.
2. **Locations**: 
   - **Trae**: `.trae/skills/`
   - **Claude**: `.claude/skills/`
   - **Gemini**: `.gemini/skills/`

---

## 📦 Outputs
Notes are saved in a `knowledge_{date}_{title}/` folder in your project root:
1.  **Markdown Deep Notes (`.md`)**: Includes ASCII art demos and 7D deep analysis.
2.  **HTML Visual Cards (`.html`)**: Features Mermaid diagrams and adaptive styling.
3.  **Raw Data (`config/raw_content.txt`)**: Cleaned raw data for backup.

---

## 🤝 Contribution & Feedback
If you find this useful, please give it a Star! ⭐ 
Feel free to submit an Issue if you encounter any problems.

---
<div align="center">
Made with ❤️ for Learners
</div>
