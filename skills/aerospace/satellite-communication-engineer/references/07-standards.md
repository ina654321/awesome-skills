## § 7 Standards & Reference

### Link Budget Template (Ka-band LEO example)
```
FORWARD LINK (Gateway → Satellite → User Terminal):

Uplink (Gateway → Satellite):
  Gateway EIRP:                    +65 dBW  (10m dish at Ka)
  Free Space Path Loss (550km):   -177.3 dB (at 30 GHz)
  Atmospheric loss (el=40°):       -0.8 dB
  Satellite G/T:                   +5.0 dB/K
  C/N0 (uplink):                  +116.9 dBHz

Downlink (Satellite → User Terminal):
  Satellite EIRP per beam:         +45 dBW
  Free Space Path Loss (550km):   -173.0 dB (at 20 GHz)
  Rain fade margin needed (Ka):    -4.5 dB  (99.9% availability)
  Terminal G/T (30cm flat panel):  +6.0 dB/K
  C/N0 (downlink):                +93.5 dBHz

Combined C/N0 (carrier to noise):  +92.5 dBHz (total, dominated by downlink)
Required Eb/N0 for QPSK 3/4:      +4.6 dB
Occupied bandwidth:                500 MHz
Available C/N:                     +12.5 dB
Required C/N (QPSK 3/4):          +7.5 dB
Link Margin:                       +5.0 dB  ✓ (≥3 dB required)
```

### Key Performance Metrics
| Metric | Target | Warning | Critical |
|--------|--------|---------|---------|
| Link margin (clear sky) | ≥ 6 dB | 3–6 dB | < 3 dB |
| Link margin (rain fade, 99.9% avail.) | ≥ 1 dB | 0–1 dB | < 0 dB (outage) |
| EIRP spectral density (ITU limit) | Per ITU Art. 22 mask | Within 2 dB of limit | Exceeds limit |
| Pointing accuracy (GEO) | ≤ 0.1° for large terminal | 0.1–0.3° | > 0.3° |
| Terminal rain margin (Ka) | ≥ 6 dB (90° elevation) | 3–6 dB | < 3 dB |
| Spectral efficiency | > 4 bits/s/Hz (DVB-S2X) | 2–4 bits/s/Hz | < 2 bits/s/Hz |

