## 8. Standard Workflow

### 8.1 Translation Workflow

```
Phase 1: Preparation (Before translation)
├── Receive: Video file, source subtitles (if available), style guide, glossary
├── Review: Watch video entirely; note speakers, names, terminology
├── Create: Project glossary (names, terms, recurring phrases)
├── Configure: Subtitle software with target format and timing settings
└── Set: QC parameters (max duration, CPS, min gap)

Phase 2: Translation (Core work)
├── Segment by segment: Translate one subtitle at a time
├── Check: Timing fits source audio (sync to spoken words)
├── Apply: CPS calculation; split or merge lines if needed
├── Maintain: Glossary consistency throughout
├── Add: Speaker IDs for SDH/CC (if required)
└── Flag: Problem areas for later review (inaudible, ambiguous)

Phase 3: Quality Assurance (After translation)
├── Automated QC: Run software checks for timing, CPS, formatting
├── Manual review: Watch entire video with subtitles playing
├── Consistency check: Verify glossary terms used correctly
├── Style check: Verify formatting matches style guide
└── Spot check: Verify sync points match audio exactly

Phase 4: Delivery
├── Export: Correct format (SRT, VTT, etc.)
├── Validate: File plays correctly in player
├── Package: Deliver per client requirements
└── Archive: Save project files for future reference
```

### 8.2 SDH/Accessibility Workflow

```
For Closed Captions (SDH), add to translation:
1. Speaker Identification
   ├── [JOHN] at start of each new speaker's lines
   ├── [UNKNOWN] when speaker cannot be identified
   └── [OFFSCREEN] for voices not shown

2. Sound Descriptions
   ├── [MUSIC: tense, building] at start of significant music
   ├── [PHONE RINGING] when audible but not shown
   ├── [DOOR CREAKS] for important sound effects
   └── [LAUGHTER] for audience/group reactions

3. Formatting
   ├── All caps for sounds: [DOORBELL]
   ├── Italics for song lyrics or foreign language
   └── Include non-speech sounds that affect understanding
```

