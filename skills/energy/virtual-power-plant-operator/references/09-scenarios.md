# Scenario Examples

## 9.1 Unexpected Resource Outage During DR Event

**Situation:** "30% of enrolled residential HVAC load dropped offline during peak DR event due to customer override."

**Expert:**
> **Immediate Response:**
> 
> 1. **Assessment:**
    - Identify affected resources
    - Calculate capacity shortfall
    - Check remaining portfolio
    - Verify communication status
> 
> 2. **Compensation:**
    - Dispatch additional available resources
    - Activate commercial/industrial load
    - Use battery storage if available
    - Request emergency dispatch
> 
> 3. **Root Cause:**
    - Customer comfort override
    - Communication failure
    - Device malfunction
    - Incorrect enrollment
> 
> **Prevention:**
    - Customer incentive structure
    - Multiple resource types
    - Over-recruiting capacity
    - Real-time monitoring alerts
    - Device management technology

## 9.2 Grid Emergency Response

**Situation:** "Grid operator issues EEA Level 2 emergency. Requesting all VPP resources respond immediately."

**Expert:**
> **Emergency Response Protocol:**
> 
> 1. **Immediate Actions:**
    - Confirm emergency notification
    - Activate all available resources
    - Prioritize by capability
    - Maintain grid stability
> 
> 2. **Dispatch Priority:**
    | Resource Type | Priority | Response |
    |--------------|----------|----------|
    | Battery storage | 1 | Immediate dispatch |
    | Commercial DR | 1 | Fast response |
    | Industrial load | 2 | Slightly longer |
    | Residential | 3 | Customer notification |
> 
> 3. **Monitoring:**
    - Real-time grid frequency
    - Transmission constraints
    - Local capacity issues
    - Equipment limits
> 
> 4. **Coordination:**
    - Continuous grid operator contact
    - Status updates
    - Performance reporting
    - Event documentation

## 9.3 Communication System Failure

**Situation:** "SCADA communication lost with 40% of distributed battery storage resources. Resources still operating locally."

**Expert:**
> **Assessment:**
> 
> Communication failures require careful handling:
> 
> 1. **Immediate:**
    - Verify local operation status
    - Switch to backup communications
    - Alert field operations
    - Notify grid operator
> 
> 2. **Impact:**
    - Cannot dispatch affected resources
    - Portfolio capacity reduced
    - May need to bid less capacity
    - Settlement implications
> 
> 3. **Troubleshooting:**
    - Check network infrastructure
    - Verify cloud connectivity
    - Test backup channels
    - Review security events
> 
> **Recovery:**
    - Field dispatch if critical
    - Manual reading of meters
    - Restoration of communications
    - Performance reconciliation
> 
> **Mitigation:**
    - Backup communication paths
    - Local autonomous operation
    - Regular communication testing
    - Redundant systems

## 9.4 Resource Performance Underperformance

**Situation:** "Aggregated residential solar+storage showing 20% less performance than modeled during peak hours."

**Expert:**
> **Analysis:**
> 
> Performance issues can stem from multiple sources:
> 
> 1. **Data Review:**
    - Compare actual vs. modeled output
    - Check weather correlation
    - Review customer behavior
    - Verify meter accuracy
> 
> 2. **Possible Causes:**
    - Weather forecast error
    - Customer loads higher than expected
    - Inverter curtailments
    - DER configuration issues
    - Shade or degradation
> 
> 3. **Corrective:**
    - Recalibrate models
    - Re-forecast with actual data
    - Customer outreach
    - Site inspections if needed
> 
> **Future Prevention:**
    - Better forecasting models
    - Real-time performance monitoring
    - Customer education
    - Regular maintenance
    - Diverse resource mix

## 9.5 Market Price Volatility

**Situation:** "Day-ahead prices spiked 300% unexpectedly. VPP committed capacity at lower prices."

**Expert:**
> **Assessment:**
> 
> Price volatility creates both risk and opportunity:
> 
> 1. **Risk Management:**
    - Real-time optimization
    - Bid strategy adjustment
    - Portfolio balancing
    - Flexibility use
> 
> 2. **Opportunity Capture:**
    - Shift dispatch to high-price hours
    - Store energy for peak
    - Defer flexible loads
    - Bid ancillary services
> 
> 3. **Lessons Learned:**
    - Better price forecasting
    - Flexible resource positioning
    - Hedging strategies
    - Scenario planning
> 
> **Portfolio Optimization:**
    - Blend of long/short positions
    - Resource flexibility
    - Storage arbitrage
    - Ancillary services revenue

## 9.6 Cyber Incident Response

**Situation:** "Suspicious commands detected in DER management system. System potentially compromised."

**Expert:**
> **Emergency Protocol:**
> 
> 1. **Immediate:**
    - Isolate affected systems
    - Alert cybersecurity team
    - Switch to backup control
    - Notify leadership
> 
> 2. **Investigation:**
    - Identify attack vector
    - Assess scope of compromise
    - Review access logs
    - Determine impact
> 
> 3. **Containment:**
    - Disable compromised accounts
    - Change credentials
    - Update firewall rules
    - Monitor for spread
> 
> 4. **Recovery:**
    - Restore from clean backup
    - Verify system integrity
    - Test all connections
    - Gradual return to service
> 
> **Prevention:**
    - Regular security audits
    - Multi-factor authentication
    - Network segmentation
    - Employee training
    - Incident response plan
