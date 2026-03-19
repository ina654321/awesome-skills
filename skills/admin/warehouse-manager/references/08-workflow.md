# Workflow Reference

## 8.1 Receiving Workflow

### Step-by-Step Process
1. **Pre-Arrival**: Review advance shipping notice (ASN), allocate dock door
2. **Truck Arrival**: Verify driver credentials, check seal integrity
3. **Unloading**: Inspect packaging damage, count pieces, stage pallet
4. **Inspection**: Quality check against PO, note discrepancies
5. **Put-Away**: Scan items into WMS, move to designated location
6. **Documentation**: File BOL, update inventory records

### Checkpoint
```
Shipment Received → Count Verification → Quality Check → WMS Update → Put-Away Complete
```

## 8.2 Inventory Management Workflow

### Cycle Count Process
1. Generate count schedule (ABC classification)
2. Print count sheets from WMS
3. Physical count with scanner
4. Input variances in system
5. Investigate discrepancies > 1%
6. Adjust inventory records

### Replenishment Logic
- Min/Max: Set reorder points based on historical usage
- Kanban: Visual signals for pull-based replenishment
- Cross-docking: Direct transfer from receiving to shipping

## 8.3 Order Fulfillment Workflow

### Pick, Pack, Ship Process
1. **Order Release**: WMS generates pick wave based on priority
2. **Picking**: Batch pick or discrete pick based on order profile
3. **Packing**: Verify items, select appropriate carton, apply labels
4. **Weighing**: Verify weight against carrier expectations
5. **Labeling**: Apply shipping labels, tracking numbers
6. **Staging**: Arrange in outbound dock by carrier/route

### Performance Metrics
- Orders per hour: Target 25-40 (depends on order complexity)
- Items per pick: Batch of 8-15 orders typical
- Packs per hour: Target 40-60 packages