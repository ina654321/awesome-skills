## 7. Standards & Reference

### 7.1 Major Platform Specifications

| Platform | Format | Max Lines | Max Chars/Line | Max Duration | CPS Limit |
|----------|--------|-----------|----------------|---------------|------------|
| **Netflix** | SRT, VTT | 2 | 42 | 7 seconds | 17-20 CPS |
| **Amazon Prime** | SRT, VTT | 2 | 42 | 7 seconds | 17 CPS |
| **Disney+** | SRT, VTT | 2 | 38 | 6 seconds | 16 CPS |
| **YouTube** | SRT, VTT, SBV | 2 | 32 | Unknown | 21 CPS |
| **Broadcast (FCC)** | CEA-608/708 | 4 | 32 | Per spec | 15 CPS |

### 7.2 SRT Format Structure

```
1
00:00:01,000 --> 00:00:04,000
First subtitle line
Second subtitle line

2
00:00:05,500 --> 00:00:08,200
Second subtitle text
```

### 7.3 VTT Format Structure

```
WEBVTT

00:00:01.000 --> 00:00:04.000
First subtitle line
Second subtitle line

00:00:05.500 --> 00:00:08.200
Note: VTT uses periods, not commas
```

