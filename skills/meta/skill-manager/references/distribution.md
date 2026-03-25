# Skill Distribution Guide

> How to share, publish, and distribute your skills.

---

## Distribution Options

| Option | Best For | Difficulty |
|--------|----------|------------|
| GitHub repo | Open source, community | Easy |
| skillport | One-command install | Easy |
| npx skills | npm ecosystem | Easy |
| Claude Code plugin | Claude users | Medium |
| Internal registry | Enterprise | Hard |

---

## Option 1: GitHub Repository

### Structure

```
my-awesome-skills/
├── README.md
├── skills/
│   ├── skill-a/
│   │   └── SKILL.md
│   └── skill-b/
│       └── SKILL.md
└── LICENSE
```

### README Template

```markdown
# Awesome Skills

A collection of skills for [your domain].

## Installation

```bash
# Clone this repo
git clone https://github.com/yourname/awesome-skills.git

# Point your agent to the skills directory
# (see your agent's documentation)
```
```

### Best Practices

- ✅ One skill per directory
- ✅ Clear, specific skill names (kebab-case)
- ✅ Detailed README per skill
- ✅ License file included

---

## Option 2: skillport

[skillport](https://skillport.dev) is a package manager for skills.

### Install

```bash
npm install -g skillport
```

### Publish

```bash
# Login
skillport login

# Publish a skill
skillport publish ./my-skill

# Or publish entire collection
skillport publish ./my-skills
```

### Install

```bash
# Install from GitHub
skillport install github:username/repo

# Install specific skill
skillport install github:username/repo --skill skill-name
```

---

## Option 3: npx skills

Part of the npm ecosystem.

### Install

```bash
# Install all skills from a repo
npx skills add username/repo

# Install specific skill
npx skills add username/repo --skill skill-name
```

---

## Option 4: Claude Code Plugin

### Create Plugin Structure

```
my-skills-plugin/
├── skills/
│   ├── skill-a/
│   │   └── SKILL.md
│   └── skill-b/
│       └── SKILL.md
├── README.md
└── manifest.json
```

### manifest.json

```json
{
  "name": "my-skills",
  "version": "1.0.0",
  "description": "Custom skills for...",
  "skills": [
    "./skills/skill-a",
    "./skills/skill-b"
  ]
}
```

### Install via Marketplace

```bash
/plugin marketplace add username/my-skills-plugin
```

---

## Option 5: Internal Enterprise Registry

For organizations that need private skill distribution.

### Registry Structure

```
https://skills.internal.company.com/
├── index.json
├── skill-a@1.0.0.tar.gz
└── skill-b@2.1.0.tar.gz
```

### index.json Format

```json
{
  "skills": [
    {
      "name": "skill-a",
      "version": "1.0.0",
      "description": "...",
      "tarball": "skill-a@1.0.0.tar.gz",
      "requires": [
        "skill-b@>=1.0.0"
      ]
    }
  ]
}
```

### Enterprise Considerations

| Concern | Solution |
|---------|----------|
| Security | Scan skills before publishing |
| Access control | Authenticated registry |
| Auditing | Log who installed what |
| Compliance | Version pinning |

---

## Choosing the Right Option

### For Open Source

1. **GitHub repo** — simplest, most discoverable
2. **skillport** — if you want easy installation

### For Teams

1. **Internal GitHub** — if you already use GitHub
2. **Claude Code plugin** — if everyone uses Claude

### For Enterprise

1. **Private registry** — full control
2. **Internal plugin** — if using Claude Code

---

## Publishing Checklist

```
[ ] README.md complete with installation instructions
[ ] LICENSE file (MIT, Apache 2.0, etc.)
[ ] Version tagged (git tag v1.0.0)
[ ] evals/ directory with test cases (optional but recommended)
[ ] Semantic version in frontmatter
[ ] Changelog maintained
[ ] Dependencies declared
```

---

## Promotion

### Get Listed

- Submit to [awesome-skills](https://github.com/topics/agent-skills)
- Post on [Agent Skills Discord](https://discord.gg/agentskills)
- Write blog posts / tutorials

### SEO for Skills

Your skill description should include:
- What it does (verb)
- Who it's for (audience)
- When to use it (triggers)

```yaml
description: >
  Automated code review with security analysis. 
  Use by security teams, DevOps engineers, and 
  anyone reviewing pull requests for vulnerabilities.
```
