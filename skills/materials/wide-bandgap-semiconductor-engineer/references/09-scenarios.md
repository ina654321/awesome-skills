# Scenario Examples

## 9.1 Common Scenario: GaN HEMT Gate Oscillation

**User:** Our GaN HEMT half-bridge shows 30V gate oscillation at turn-on in simulation, but oscillates 50V in lab. What is causing this and how do we fix it?

**Expert:**
> **Analysis:**
> Gate oscillation in GaN is caused by the interaction of high dv/dt with parasitic inductance in the gate loop. GaN's very high switching speed (dv/dt > 100 V/ns) amplifies even small inductances.
>
> **Root cause identification:**
> 1. Gate loop inductance: Lg_loop = Lg_source + Lg_pcb; should be < 5 nH
> 2. Common source inductance: if source pin is shared with power loop, it creates feedback
> 3. Gate resistor too small: Rg < 5 Ω can cause underdamped response
> 4. Missing gate clamp: body diode commutation induces gate overshoot
>
> **Fix (in order of priority):**
> 1. Kelvin source connection: separate power source and gate source pins
> 2. Add gate-to-source clamp: 5.1V Zener or Schottky clamp
> 3. Increase Rg_off to 2–5 Ω (Rg_on can stay low)
> 4. Add RC snubber at gate: 10 Ω + 100 pF across device
> 5. Shorten gate trace: use 0402 components directly at device pins
>
> **Target:** Gate overshoot < 1V above Vgs(on); oscillation damped in < 2 periods.

## 9.2 Complex Scenario: SiC MOSFET Body Diode Degradation in PV Inverter

**User:** Our 1200V SiC MOSFETs in a PV inverter show increased reverse recovery (Qrr increased 3× after 2000h of field operation). The VDS leakage current also doubled. What is the failure mechanism?

**Expert:**
> **Comprehensive Solution:**
> This is a classic SiC MOSFET body diode degradation pattern, indicating either:
> 1. **Body diode forward current stress** — if used as freewheeling diode in hard-switched topology
> 2. **SiC/SiCPN junction temperature exceedance** — body diode has higher VF drift than Si
> 3. **Hot carrier injection** — carriers trapped in gate oxide, affecting threshold
>
> **Diagnostic protocol:**
> 1. Measure Vf at rated If (25°C and 150°C): compare to baseline
> 2. Measure Qrr at VDS = 600V, di/dt = 500 A/µs: Qrr should be < datasheet max
> 3. Gate leakage scan: IGSS vs Vgs at operating temperature
> 4. Cross-section failure analysis: TEM of gate oxide if device is available
>
> **Immediate mitigation:**
> - Add Schottky diode (SiC SBD) in parallel with SiC MOSFET to reduce body diode stress
> - Reduce switching frequency to lower di/dt
> - Improve thermal management: lower Tj from 150°C to 125°C
>
> **Long-term design change:**
> - Use SiC MOSFET in synchronous rectification mode only (never body diode as main FW)
> - Select SiC MOSFET with low Qrr specification (< 300 nC at 760V)
> - Implement diode monitoring: measure Vf in periodic self-test

## 9.3 Edge Case: GaN inTotem-Pole PFC Exceeds EMI Limits

**User:** Our 3kW totem-pole PFC using GaN fails CISPR 32 Class B at 150 kHz–30 MHz. What can we do?

**Expert:**
> **Special Handling:**
>
> Totem-pole PFC with GaN is notoriously challenging for EMI because of:
> - Hard commutation with 100+ V/ns dv/dt
> - High-frequency switching (100–300 kHz)
> - CM noise from fast dv/dt without soft-switching
>
> **Fix sequence (least invasive first):**
> 1. **CM filter:** Add common-mode choke on AC input + Y capacitors; typical CM inductance 10–50 mH
> 2. **DM inductor optimization:** Increase DM inductance or add differential RC snubber
> 3. **Soft-switching:** Implement TCM (triangular current mode) or bridgeless totem-pole with ZVS
> 4. **Layout:** Shield switching nodes; use EMI absorber material (ferrite sheet) on PCB
> 5. **Spread spectrum:** Implement frequency dithering ±5% at 250 Hz modulation (if GaN gate driver supports)
>
> **Expected result:** CISPR 32 Class B margin of 6 dB achievable with CM filter + dithering
