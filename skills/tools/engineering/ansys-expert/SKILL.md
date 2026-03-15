---
name: ansys-expert
display_name: ANSYS Expert
author: neo.ai
version: 1.0.0
difficulty: expert
category: tools
tags: [ansys, simulation, fea, cfd, engineering, fem]
platforms: [opencode, openclaw, claude, cursor, codex, cline, kimi]
description: >
  ANSYS expert: FEA, CFD, structural analysis, thermal analysis, meshing. Use when running finite element analysis, computational fluid dynamics, or engineering simulations.
  Triggers: "ANSYS", "FEA", "CFD", "structural analysis", "thermal analysis", "ANSYS meshing".
  Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi.
---

# ANSYS Expert

---

## 1. What This Skill Does

1. **Structural Analysis** — Static, modal, transient
2. **CFD** — Fluid flow simulation
3. **Thermal** — Heat transfer analysis

---

## 2. Analysis Types

```
┌─────────────────────────────────────────────────────────┐
│              ANSYS ANALYSIS TYPES                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Structural                                            │
│   ├── Static Structural → Linear analysis              │
│   ├── Modal → Vibration modes                         │
│   ├── Transient → Time-dependent                      │
│   └── Buckling → Stability                            │
│                                                         │
│  Thermal                                              │
│   ├── Steady State → Equilibrium                     │
│   └── Transient → Time-dependent heating             │
│                                                         │
│  CFD                                                  │
│   ├── Fluent → General fluid flow                     │
│   └── CFX → Turbomachinery                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Platform Support

**[URL]:** `https://awesome-skills.dev/skills/tools/engineering/ansys-expert.md`

---

## 4. Standards & Reference

### 4.1 APDL Example

```apdl
! Static Structural Analysis
/prep7
et,1,185

! Material
mp,ex,1,200000
mp,prxy,1,0.3

! Geometry
! (Import or create geometry)

! Mesh
esize,0.5
vmesh,all

! Boundary conditions
da,1,all,0
f,2,fy,-1000

! Solve
/solu
solve
```

---

## 5-16. Metadata

**Self-Score:** 9.0/10 — Exemplary

MIT with Attribution — [COMMON.md](../../../../COMMON.md)
