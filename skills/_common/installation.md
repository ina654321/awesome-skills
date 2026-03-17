---
title: Common Installation Guide
description: >
  Common installation guide for all Awesome Skills. This document provides platform-specific
  installation instructions referenced by individual skill files to avoid duplication.
---

# 通用安装指南 / Common Installation Guide

OpenCode 原生支持技能安装：

```
/skill install [skill-name]
```

或使用 Read 命令：
```
Read [SKILL_URL] and install [skill-name] skill
```

---

## OpenClaw（推荐 / Recommended）

```
Read [SKILL_URL] and install [skill-name] skill
```

技能存储位置：`~/.openclaw/workspace/skills/[skill-name]/SKILL.md`

---

## Claude Code

**方法 1：项目级配置（推荐）**
```bash
cat >> CLAUDE.md << 'EOF'
Read [SKILL_URL] and apply the skill guidelines to this project.
EOF
```

**方法 2：单次会话**
```
Read [SKILL_URL] and install [skill-name] skill
```

---

## Cursor

```bash
curl -s [RAW_SKILL_URL] >> .cursorrules
```

将 `[RAW_SKILL_URL]` 替换为技能的 raw GitHub 地址（`raw.githubusercontent.com/...`）

---

## OpenAI Codex / Cline / Kimi Code

将技能文件的 System Prompt 部分复制到对应平台的系统提示词配置中。

---

## 完整平台指南 / Full Platform Guide

详见项目根目录的 [INSTALL-GUIDE.md](../../INSTALL-GUIDE.md)

---

## 技能包安装 / Package Installation

```
Read https://github.com/theneoai/awesome-skills/blob/main/packages/[package-name].md and install [package-name] package
```

可用技能包 (Available packages)：`executive`, `tech`, `ai-ml`, `professional`, `creative`
