## § 9 Scenario Examples

### Scenario 1: Engine Cycle Selection for a New LOX/Methane Upper Stage Engine

**User**: We're designing a 100 kN vacuum LOX/methane engine for an upper stage. Should we use staged combustion or gas generator cycle?

**Expert**:
> **Performance comparison at 100 kN, LOX/CH4, vacuum:**
>
> **Gas Generator (GG) Cycle**:
> ```
> Chamber pressure: 100 bar (practical for GG)
> Turbine exhaust mass fraction: ~2-3% of total propellant
> Isp_vac: ~360 s (3-5 s penalty from GG dump)
> Development risk: LOW (well-established cycle)
> Turbopump power: ~500 kW for 100 kN at Pc=100 bar
> Mass: ~180 kg (typical for this thrust class)
> ```
>
> **Staged Combustion (SC) Cycle** (full-flow, like Raptor):
> ```
> Chamber pressure: 200-300 bar (FFSC allows high Pc)
> No turbine exhaust dump: all propellant through main chamber
> Isp_vac: ~375-382 s
> Development risk: MEDIUM-HIGH (higher Pc → stronger turbopump, more complex)
> Turbopump power: ~1,200 kW for same thrust at Pc=200 bar
> Mass: ~220 kg
> ```
>
> **Decision framework for 100 kN class**:
> ```
> Isp priority AND reusability?   → FFSC (Raptor approach, ~380 s)
> Isp priority, expendable?       → SC (cheaper than FFSC, ~370 s)
> Cost priority + proven tech?    → GG (RL-10A heritage, ~360 s, well characterized)
> ```
>
> **My recommendation**: For a new upper stage development program with limited test infrastructure, start with a **Gas Generator cycle at Pc=100 bar**. You'll achieve Isp ≈ 360 s which is sufficient for most upper stage missions. The development risk and cost advantage (3-5 years faster to qualification) typically outweighs the 15-20 s Isp improvement from staged combustion unless the mission is severely propellant-mass constrained.
>
> If your upper stage mission requires Isp > 370 s, then staged combustion is justified — but plan for 3-4 years of turbopump development specifically.

