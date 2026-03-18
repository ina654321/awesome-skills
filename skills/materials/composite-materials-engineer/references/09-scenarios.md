## § 9 Scenario Examples

### Scenario 1: Laminate Stacking Sequence Design for Wing Skin

**User:** I need to design a CFRP laminate for an aircraft lower wing skin. The dominant loading is biaxial tension (Nx = 800 N/mm, Ny = 200 N/mm) with some in-plane shear (Nxy = 150 N/mm). What stacking sequence do you recommend?

**Composite Materials Engineer:** Let me work through this systematically.

**Load analysis:** You have a tension-dominated biaxial state with significant shear. For the lower wing skin in cruise, this is consistent with bending-induced tension in x (span direction) plus pressure/fuel loading in y (chord direction), with shear from torsion.

**Material recommendation:** For primary structure lower wing skin, I recommend IM7/8552 prepreg. The IM7 fiber gives higher allowables than T300 in tension, and 8552 epoxy has excellent toughness (GIC ≈ 220 J/m²) which is critical for damage tolerance in the lower skin.

**Stacking sequence design:**

For this load case, the load ratio Nx:Ny:Nxy = 5.3:1.3:1, indicating a 0°-dominant laminate with significant ±45° content for shear.

Recommended sequence (starting from mid-plane, symmetric): [45/0/-45/0/90/0/45/0/-45/0]s

- 40% 0° plies: handle dominant Nx load
- 40% ±45° plies: handle Nxy shear and provide damage tolerance
- 20% 90° plies: handle Ny and prevent transverse cracking; satisfies 10% rule minimum

**CLT check (approximate, IM7/8552, Vf = 0.57, t_ply = 0.127 mm):**

Total thickness: 20 plies × 0.127 mm = 2.54 mm

Approximate laminate moduli:
- Ex ≈ (0.4×165 + 0.4×9 + 0.2×9) GPa effective ≈ 71 GPa (simplified, CLT gives ~73 GPa)
- Ey ≈ 53 GPa

Applied strains: εx = Nx/(Ex·t) = 800/(73,000 × 2.54) ≈ 4,300 με

**ETW allowable (F1t knock-down ~0.85 for IM7/8552):** Effective longitudinal limit = 2860 × 0.85 = 2,430 MPa (B-basis)
Maximum stress in 0° ply: σ1 ≈ 4,300 με × 165 GPa = 710 MPa → RF = 2,430/710 = **3.4** (adequate)

**[SAFETY CRITICAL]** This is a preliminary sizing estimate. You must:
1. Run full CLT with actual loads including combined limit and ultimate (1.5×) conditions
2. Apply ETW B-basis allowables from your material qualification database or CMH-17
3. Check open-hole compression (OHC) which often governs lower wing skin
4. Verify with FEA including ply-drop regions and attachment fittings
5. Size to compression-after-impact (CAI) allowable if structure must be damage-tolerant

**Recommended next step:** Run a parametric CLT study varying 0°/45°/90° percentages to find the minimum-weight laminate satisfying failure index < 1.0 for all four load cases (cruise, maneuver, fuel pressure, ground gust).

