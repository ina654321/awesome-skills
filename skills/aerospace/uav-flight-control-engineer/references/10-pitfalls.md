## § 10 Common Pitfalls

### Pitfall 1: Ignoring Anti-Windup

❌ **BAD:**
```python
integral += error * dt   # Unbounded integration
output = Kp*error + Ki*integral + Kd*derivative
```

✅ **GOOD:**
```python
# Clamping anti-windup
integral += error * dt
output_unlimited = Kp*error + Ki*integral + Kd*derivative
output = clip(output_unlimited, -MAX_OUTPUT, MAX_OUTPUT)
# Back-calculate to prevent windup
if output != output_unlimited:
    integral -= (output_unlimited - output)
```

