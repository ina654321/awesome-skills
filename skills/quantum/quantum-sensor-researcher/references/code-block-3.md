# python Example

```
import numpy as np

# Transfer function: vibration noise into gravity measurement
# For atom gravimeter, vibration rejection comes from:
# 1. Differential gradiometer (two clouds): rejects common-mode
# 2. Seismometer feedforward: measure and subtract vibration

def vibration_sensitivity(S_vib_mHz, k_eff, T, rejection_factor=1.0):
    """
    Convert platform vibration PSD to effective gravity noise.
    S_vib: vibration PSD in (m/s²)²/Hz at measurement frequency
    rejection_factor: gradiometer or feedforward rejection (e.g., 0.01 = 40 dB)
    """
    # Gravity phase noise from vibration: Phi_noise = k_eff * T² * a_vib
    # S_phi = k_eff² * T^4 * S_vib
    S_phi_vib = k_eff**2 * T**4 * S_vib_mHz
    delta_g_vib = np.sqrt(S_phi_vib)
    return delta_g_vib * rejection_factor

k_eff = 2 * 2 * np.pi
T = 0.1  # s (reduced for mobile platform)

scenarios = {
    "Lab (passive isolation)": (1e-12, 1.0),      # quiet lab
    "Vehicle (no isolation)": (1e-8, 1.0),         # van
    "Vehicle + seismometer feedforward": (1e-8, 0.01),  # 40 dB rejection
    "Vehicle + gradiometer (1m baseline)": (1e-8, 0.001),  # 60 dB rejection
}

print("Effective gravity noise from platform vibration:")
for scenario, (S_vib, rejection) in scenarios.items():
    delta_g = vibration_sensitivity(S_vib, k_eff, T, rejection)
    print(f"  {scenario}: {delta_g/1e-9:.2f} × 10^-9 g/√Hz")
```
