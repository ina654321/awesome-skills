# Standards & Reference

## 7.1 Official Documentation

- [IEEE Electron Devices Society — WBG Standards](https://eds.ieee.org/technical-standards/wbg)
- [JEDEC JC-70 Committee — Wide Bandgap Power Electronics](https://www.jedec.org/committees/jc-70)
- [ANSI/ASHRAE 90.1 — Energy Standard for WBG in HVAC](https://www.ashrae.org/)
- [AIST — National Institute of Advanced Industrial Science and Technology](https://www.aist.go.jp/)
- [DoE PowerAmerica — WBG Deployment Reports](https://www.poweramerica.org/)

## 7.2 Key Device & Material Standards

| Standard | Scope | Key Requirements |
|----------|-------|------------------|
| **JEDEC JEP173** | Dynamic On-Resistance test method for GaN | Test conditions, measurement setup, reporting |
| **JEDEC JEP180** | GaN HEMT reliability qualification | Time-dependent dielectric breakdown, HTRB |
| **JEP192** | GaN Figure of Merit methodology | FOM calculation from RDS(on), Qgd, Coss |
| **AEC-Q101** | Automotive discrete semiconductor stress test | Automotive-grade qualification for SiC/GaN |
| **JEDEC JEP119** | Silicon Carbide Schottky diode qualification | Surge current, reverse recovery |
| **IEC 60747-9** | Discrete semiconductor — MOSFET parameters | SiC MOSFET datasheet parameters |
| **JEDEC JEP136** | SiC MOSFET specific test methods | Threshold voltage stability, body diode |

## 7.3 Critical Performance Parameters

| Parameter | SiC MOSFET (650V) | SiC MOSFET (1200V) | GaN HEMT (650V) | Si IGBT (1200V) |
|-----------|-------------------|-------------------|-----------------|-----------------|
| RDS(on) at 25°C | 15–80 mΩ | 25–160 mΩ | 10–50 mΩ | N/A (Vce(sat)) |
| Switching loss (Eon+Eoff) | 0.3–1.2 mJ | 0.8–3.0 mJ | 0.1–0.5 mJ | 5–15 mJ |
| Figure of Merit (FOM) | 50–200 mΩ·nC | 100–500 mΩ·nC | 20–100 mΩ·nC | N/A |
| Thermal resistance (Rth_jc) | 0.5–2.0 °C/W | 0.4–1.5 °C/W | 0.5–2.0 °C/W | 0.3–1.0 °C/W |
| Max junction temp | 175–200°C | 175–200°C | 150–175°C | 150–175°C |
| dv/dt capability | 50–100 V/ns | 20–50 V/ns | 100–200 V/ns | 5–20 V/ns |

## 7.4 Reliability Test Standards

| Test | Condition | Duration | Failure Criteria |
|------|-----------|----------|-----------------|
| **HTRB** (High Temp Reverse Bias) | 100% Vrated, 150°C | 1000–2000h | RDS(on) drift > 20%; IDSS > 10× initial |
| **HTGB** (Gate Bias) | Vgs_max, 150°C | 1000h | Vth shift > 0.5V; IGSS > 100 µA |
| **TC** (Temperature Cycling) | -55°C to 150°C | 500 cycles | Cracking, delamination, RDS(on) shift |
| **Power Cycling** | ΔT_j = 100°C | 10,000 cycles | Vce(on) or RDS(on) > 20% increase |
| **H3TRB** (Humidity) | 85°C/85% RH, 80% Vrated | 1000h | Corrosion, parameter shift |
