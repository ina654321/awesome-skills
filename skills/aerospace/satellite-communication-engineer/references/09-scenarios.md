## § 9 Scenario Examples

### Scenario 1: Ka-Band LEO User Terminal Sizing

**User**: We're deploying a Ka-band LEO broadband service. Our satellite EIRP per beam is 45 dBW and we're at 550km altitude. We need 100 Mbps to a small flat-panel terminal. How big does the terminal need to be?

**Expert**:
> Let me work through the link budget. **Downlink (satellite → terminal) at 550 km, Ka-band ~20 GHz**:
>
> ```
> Satellite EIRP (per beam):          +45.0 dBW
> Free Space Path Loss (550km, 20GHz): -173.0 dB  [FSPL = 20log(4πd/λ)]
> Atmospheric absorption (Ka, 40° el): -0.5 dB
> Polarization loss:                   -0.3 dB
> Net power at terminal antenna input: -128.8 dBW
>
> Required Eb/N0 for 100 Mbps:
>   DVB-S2X 16APSK 3/4 (spectral eff: 3.0 bits/s/Hz):
>     Bandwidth needed: 100 Mbps
>     Required C/N0 = Eb/N0 + 10log(bitrate) = 8.3 + 80 = 88.3 dBHz
>     Required C/N (33.3 MHz bandwidth) = 88.3 - 75.2 = 13.1 dB
>
> Required terminal G/T:
>   G/T = Required C/N0 - EIRP + FSPL + losses - k
>   G/T = 88.3 - 45.0 + 173.0 + 0.8 - 228.6 = -11.5 dB/K
> ```
>
> **Terminal sizing**:
> - Required G/T = -11.5 dB/K
> - Assume LNB noise temp: 80K (T_sys ≈ 100K with antenna noise → 10log(100) = 20 dBK)
> - Required antenna gain: G = G/T + 10log(T) = -11.5 + 20 = 8.5 dBi
> - Flat panel antenna gain at 20 GHz: G = 10log(η × (πD/λ)²) where η=0.6
> - For 8.5 dBi: D ≈ 17 cm → **flat panel ~20cm × 20cm** (including margin)
>
> **Rain fade margin check** (Ka-band, US CONUS, 99.9% availability, 40° elevation): +6.5 dB needed
> - Clear-sky margin with 20cm panel: ~5 dB → **need 25cm × 25cm panel for 99.9% availability**
>
> **Bottom line**: A ~25cm flat-panel phased array can support 100 Mbps downlink at 99.9% availability in CONUS. This aligns with the Starlink Gen3 terminal form factor.

