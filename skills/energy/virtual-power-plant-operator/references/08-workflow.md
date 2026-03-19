# Standard Workflow

## 8.1 VPP Operations Workflow

```
VPP Control Process
├── Resource Aggregation
│   ├── DER registration
│   ├── Resource characterization
│   ├── Capacity assessment
│   └── Communication verification
├── Market Operations
│   ├── Day-ahead bidding
│   ├── Real-time dispatch
│   ├── Performance monitoring
│   └── Settlement
├── Grid Services
│   ├── Frequency regulation
│   ├── Demand response
│   ├── Voltage support
│   └── Capacity resources
└── Customer Management
    ├── Device enrollment
    ├── Performance tracking
    └── Customer support
```

## 8.2 Demand Response Event Workflow

1. **Pre-Event Preparation**
   - Review event parameters
   - Verify resource availability
   - Confirm communications
   - Alert participants

2. **Event Execution**
   - Dispatch signals to resources
   - Monitor load response
   - Adjust dispatch as needed
   - Track performance metrics

3. **Post-Event**
   - Calculate performance
   - Generate event report
   - Reconcile with grid operator
   - Pay participant incentives

## 8.3 Resource Integration Workflow

| Phase | Activities | Deliverables |
|-------|-----------|--------------|
| Screening | Site assessment, utility approval | Screening study |
| Interconnection | Technical review, agreements | IA, CSAg |
| Enrollment | Market registration, testing | Market participation |
| Operations | Monitoring, dispatch, settlement | Performance reports |

## 8.4 Capacity Market Operations

1. **Auction Preparation**
   - Resource portfolio review
   - Availability assessment
   - Cost estimation
   - Strategy development

2. **Capacity Performance**
   - Real-time monitoring
   - Performance scoring
   - Penalty avoidance
   - Revenue optimization

3. **Settlement**
   - Capacity payment calculation
   - Performance adjustments
   - Invoice reconciliation
   - Dispute resolution

## 8.5 Ancillary Services Workflow

| Service | Response Time | Duration | Requirements |
|---------|--------------|----------|-------------|
| Reg up/down | Seconds | Continuous | AGC capable |
| Spin reserve | Minutes | 15-30 min | Must dispatch |
| Non-spin | Minutes | 15-60 min | Can dispatch |
| Demand response | Minutes | Event-based | Load shed |

## 8.6 Quality Checklist

- [ ] All resources communicating
- [ ] Capacity verified for event
- [ ] Market positions confirmed
- [ ] Emergency contacts verified
- [ ] Performance tracking active
- [ ] Settlement data accurate
- [ ] Cybersecurity measures in place
- [ ] Backup communication ready
- [ ] DR program compliance current
- [ ] Customer notifications tested
