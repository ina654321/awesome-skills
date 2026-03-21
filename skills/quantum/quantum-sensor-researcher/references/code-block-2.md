# python Example

```
# Systematic error budget for Rb atom gravimeter
systematics = {
    "Zeeman_2nd_order": {
        "shift_g": 3e-10,   # m/s², bias
        "uncertainty_g": 5e-11,  # m/s², uncertainty
        "mitigation": "Bias field > 1 Gauss; measure at ±B field; cancel by averaging"
    },
    "AC_Stark_laser": {
        "shift_g": 2e-10,
        "uncertainty_g": 3e-11,
        "mitigation": "Intensity servo to 0.1%; alternating Raman beam direction"
    },
    "Coriolis_Earth_rotation": {
        "shift_g": 0,  # zero with symmetric geometry
        "uncertainty_g": 1e-10,
        "mitigation": "k-vector alternation (up/down launch averaging)"
    },
    "Wavefront_aberration": {
        "shift_g": 1e-10,
        "uncertainty_g": 5e-11,
        "mitigation": "High-quality beam expander; atom cloud temperature < 1 nK"
    },
}

total_systematic_unc = np.sqrt(sum(s["uncertainty_g"]**2
                                   for s in systematics.values()))
statistical_precision = 1e-10  # g after 1000s averaging

print(f"Statistical precision (1000s): {statistical_precision:.0e} g")
print(f"Total systematic uncertainty:  {total_systematic_unc:.0e} g")
if total_systematic_unc > statistical_precision:
    print("WARNING: Systematics dominate! Report systematic-limited accuracy.")
```
