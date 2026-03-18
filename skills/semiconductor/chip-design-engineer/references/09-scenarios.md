## § 9 Scenario Examples

### Scenario 1 — Fixing a Setup Timing Violation

**User:** My PrimeTime report shows WNS = −320 ps on a path from a multiplier output to a register in the ALU. The clock is 1 GHz. What do I do?

**Expert:** A −320 ps violation at 1 GHz (1000 ps period) means your path arrival is 320 ps over budget. First, extract the path:

```tcl
# In PrimeTime — get full path details
report_timing -from [get_pins mult/out_reg/Q] \
              -to   [get_pins alu/result_reg/D] \
              -max_paths 1 -path_type full_clock_expanded
```

Look for: logic depth (gate count), net delays (RC parasitics), and cell sizes. If logic depth > 15 gates, insert a pipeline stage:

```systemverilog
// Before: single-cycle multiply + add (too long at 1 GHz)
always_ff @(posedge clk) begin
  result <= a * b + c;
end

// After: two-stage pipeline breaks the critical path
always_ff @(posedge clk) begin
  mult_result <= a * b;        // Stage 1: multiply
end
always_ff @(posedge clk) begin
  result <= mult_result + c;   // Stage 2: add
end
```

If violation < 100 ps, try incremental synthesis upsizing:
```tcl
# DC-Ultra incremental compile targeting critical path
set_dont_touch_network [get_nets {mult_out}] false
compile_ultra -incremental -timing
```

[RISK] Do not use set_false_path to hide this — the path is functionally real and silicon will fail.

