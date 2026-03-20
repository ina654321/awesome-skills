# Examples

## 10.1 Parametric Bracket Design

### Workflow

```text
Phase 1: Base Sketch
Command: S (Sketch) → Select Top Plane
Draw: Rectangle 60x40mm
Constrain: Center at origin (Origin → Coincident)
Dimension: Click edges → Type 60 and 40
Constraint: Add Horizontal/Vertical constraints

Phase 2: Base Extrusion
Command: E (Extrude)
Profile: Select rectangle
Operation: New Body
Distance: 5mm
OK

Phase 3: Corner Relief Pockets
Command: S → Select top face of extrusion
Draw: 4 circles (radius 8mm) at each corner
Constrain: Coincident to corner vertices
Dimension: Set diameter to 16mm
Command: E (Extrude)
Profile: Select 4 circles
Operation: Cut
Distance: Through All
OK

Phase 4: Mounting Holes
Command: H (Hole)
Placement: Click top face → click each pocket center
Type: Clearance Hole
Size: M4
Depth: Through All
OK

Phase 5: Edge Fillet
Command: F (Fillet)
Radius: 2mm
Selection: Select all top edges
OK

Phase 6: Bottom Pocket
Command: S → Select bottom face
Draw: Rectangle 50x30mm, centered
Command: E (Extrude)
Profile: Select rectangle
Operation: Cut
Distance: 3mm
OK
```

### Resulting Model

```
Top View:
  +-------------------+
  |  o             o  |
  |                   |
  |                   |
  |  o             o  |
  +-------------------+
```

## 10.2 CNC Programming Workflow

### 2.5D Pocket Operation

```text
Setup:
1. Select Setup → New Setup
2. Work Coordinate: Select top face of stock
3. Stock Box: Define stock dimensions (90x70x20mm)
4. OK

Operation: 2D Pocket
1. Select geometry: Click top face of pocket
2. Tool: 6mm flat endmill ( carbide )
3. Passes:
   - Roughing: Adaptive, 35% stepover, 0.5mm depth
   - Finishing: Parallel, 10% stepover, 0.2mm stepdown
4. Leads/Ramps: Ramp helical, 3mm radius
5. Stock to Leave: 0.3mm (for finishing pass)
6. OK

Post Process:
1. Select Post Process
2. Choose controller: Generic FANUC
3. Output: Save .nc file to USB
```

### 3D Adaptive Roughing

```text
Operation: 3D Adaptive
1. Geometry: Select entire model
2. Tool: 10mm 4-flute carbide
3. Settings:
   - Maximum Roughing Depth: 15mm
   - Adaptive Strategy: Offset (trochoidal)
   - Stepover: 30%
   - Minimum Thickness: 0.5mm
4. Collision Avoidance: Enable tool holder check
5. Feeds & Speeds:
   - Spindle: 3000 RPM
   - Feed Rate: 800 mm/min
   - Plunge Rate: 400 mm/min
6. OK
```

## 10.3 Sheet Metal Enclosure

```text
Phase 1: Base Flange
1. Create new sketch on Top Plane
2. Draw L-bracket profile with tabs
3. Exit sketch
4. Create Sheet Metal:
   - Base Flange: Select profile
   - Material: Aluminum 6061
   - Thickness: 1.5mm
   - Bend Radius: 1.5mm (K-factor: 0.44)

Phase 2: Additional Flanges
1. Select edge → M (Move Face)
2. Extend to length 25mm
3. Add relief cuts at corners

Phase 3: Punches and Holes
1. Create holes on face (H command)
2. Add louvers for ventilation
3. Create edge bends for lips

Phase 4: Flat Pattern
1. Click Flat Pattern
2. Export DXF for laser cutting
3. Export PDF with bend notes
```

## 10.4 Assembly with Joints

```text
Phase 1: Create Components
1. Component 1: Base plate (already modeled)
2. Component 2: Bracket (Create in Place)
3. Component 3: Shaft (Create in Place)

Phase 2: Add Joints
1. Joint 1: Base ↔ Bracket
   - Type: Revolute (hinge)
   - Origin: Select edge on both parts
   
2. Joint 2: Bracket ↔ Shaft
   - Type: Ball (3-axis rotation)
   - Origin: Select contact point

Phase 3: Motion Link
1. Select Revolute joint
2. Define Motion: -45° to +45°
3. Enable animation

Phase 4: Ground Component
1. Right-click Base
2. Ground
```

## 10.5 Simulation Study

```text
Static Stress Analysis:

1. Create Study:
   - Type: Static
   - Mesh: Standard, 2mm element size

2. Apply Material:
   - Select all → Aluminum 6061-T6
   - Yield Strength: 276 MPa
   - Tensile Strength: 310 MPa

3. Apply Constraints:
   - Fixed Support: Select bottom face of base
   
4. Apply Loads:
   - Remote Force: 500N downward on top edge
   - Direction: Perpendicular to face

5. Run Simulation:
   - Click Solve
   - Review Von Mises stress (max < 276 MPa = PASS)

6. Results:
   - Safety Factor: 2.5 minimum
   - Max Displacement: 0.3mm
```

## 10.6 STL for 3D Printing

```text
Workflow:

1. Prepare Model:
   - Use Replace Face to close any gaps
   - Check for non-manifold edges:
     Analyze → Shape Analysis → Check for Issues
   
2. Check Wall Thickness:
   - Analyze → Thicken/Offset
   - Minimum wall: 0.8mm for FDM
   
3. Orient for Print:
   - Click Orient for 3D Print
   - Choose optimal angle (45° for overhangs)
   
4. Generate Supports:
   - Enable auto-support
   - Set support density: 15%
   
5. Export:
   - File → Export
   - Format: STL
   - Resolution: Fine (0.01mm)
   - Units: mm
   - Save to SD card

6. Slice in PrusaSlicer:
   - Layer height: 0.2mm
   - Infill: 15% gyroid
   - Supports: Tree
   - Material: PLA
```

## 10.7 Drawing Creation

```text
Create 2D Drawing:

1. New Drawing:
   - File → New from Document → Drawing
   - Select Template: A3 Landscape
   
2. Insert Views:
   - Base View: Select top face
   - Scale: 1:1
   - Position: Top left
   
3. Add Projected Views:
   - Front View (below top)
   - Right Side View (to right)
   
4. Add Dimensions:
   - Click dimension tool
   - Select edges → place dimension
   - Add GD&T symbols as needed
   
5. Add Annotations:
   - Surface Texture: Ra 3.2 on critical faces
   - Thread callouts: M4x0.7-6H
   - Notes: Material: Aluminum 6061
   
6. Export:
   - Save as DWG or PDF
```
