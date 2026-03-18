## § 7 · Standards & Reference

### 7.1 Structural Design Standards

| Standard | Application | Key Provisions |
|----------|-------------|----------------|
| **ASCE 7-22** | Load determination | Dead, live, snow, wind, seismic, rain, flood loads |
| **IBC 2021** | Building classification | Occupancy, construction type, seismic design category |
| **ACI 318-19** | Concrete design | Reinforced concrete beams, columns, walls, foundations |
| **AISC 360-22** | Steel design | Steel members, connections, composite design |
| **NDS 2021** | Wood design | Allowable stress design and LRFD for wood |
| **MSJC 2022** | Masonry design | Reinforced and unreinforced masonry |
| **ACI 530** | Masonry code | Masonry structural design |

### 7.2 Seismic Design Categories

| Seismic Design Category | Risk Level | Application |
|------------------------|------------|-------------|
| **A** | Low | Minimal seismic requirements |
| **B** | Moderate | Standard seismic design per ASCE 7 |
| **C** | High | Special inspection, detailed system requirements |
| **D, E, F** | Very High | Enhanced detailing, capacity design, redundancy |

### 7.3 Load Combination Templates

```
LRFD Combinations (ASCE 7-22):
1. 1.4D
2. 1.2D + 1.6L + 0.5(Lr or S or R)
3. 1.2D + 1.6(Lr or S or R) + (L or 0.5W)
4. 1.2D + 1.0W + L + 0.5(Lr or S or R)
5. 1.2D + 1.0E + L + 0.2S
6. 0.9D + 1.0W
7. 0.9D + 1.0E

ASD Combinations:
1. D
2. D + L
3. D + (Lr or S or R)
4. D + 0.75L + 0.75(Lr or S or R)
5. D + 0.6W
6. D + 0.7E
```

### 7.4 Deflection Limits (IBC Table 1604.3)

| Member | L/360 | L/240 | L/180 |
|--------|-------|-------|-------|
| Rafters, joists, beams | Live load | Total load | — |
| Floor joists | Live load | Total load | — |
| Roof members (plaster) | — | Live load | Total load |
| Roof members (no plaster) | — | — | Total load |
| Cantilevers | L/180 | — | — |

