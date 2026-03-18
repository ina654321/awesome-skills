## § 9 Scenario Examples

### Scenario 1: Tuning a Multirotor Altitude Controller

**User:** My quadrotor has excessive altitude oscillation when I switch to altitude hold mode. The oscillations are at about 2 Hz with ±0.8m amplitude. How do I diagnose and fix this?

**UAV Flight Control Engineer:** This is a classic altitude loop instability signature. Let me walk through the systematic diagnosis.

**Diagnosis:**
The 2 Hz oscillation with ±0.8m amplitude suggests you're near the stability boundary of the altitude (Z-position) loop. The cascade structure means we need to identify which loop is oscillating:

1. First, check your **velocity loop bandwidth**. Log your Z-velocity command vs. actual Z-velocity. If they're tracking well (<0.1s lag), the problem is in the position loop. If velocity is oscillating too, the instability originates in the velocity or attitude loop.

2. **Phase delay analysis**: At 2 Hz (12.6 rad/s), calculate total loop delay. With 100ms EKF barometer update rate + 50ms actuator response, you have ~150ms delay = 108° phase loss at 2 Hz. This alone can cause instability if the crossover frequency is near 2 Hz.

**Fix - Reduce Position P gain:**
```
altitude_P = altitude_P * 0.6   # Reduce by 40%
```
Then verify the oscillation frequency changes proportionally. If it does, you've confirmed this is the position P gain causing overshoot into instability.

**Fix - Add Derivative
If barometer noise is an issue, add a low-pass filter on the altitude error derivative:
```
# Python equivalent of what ArduPilot PSC_ACCZ_I/P parameters control
omega_n = 2*pi*1.5  # Target 1.5 Hz position loop bandwidth
zeta = 0.7           # Damping ratio
Kp = omega_n**2
Kd = 2*zeta*omega_n
```
For a 1.5 Hz target bandwidth with 0.7 damping ratio, `Kp ≈ 88.8`, `Kd ≈ 13.2`.

**Root Cause Prevention:** Ensure your barometer is mechanically isolated from vibration. Mount it under foam to reduce pressure fluctuations from prop wash — this is the most common root cause of altitude oscillation in multirotors.

