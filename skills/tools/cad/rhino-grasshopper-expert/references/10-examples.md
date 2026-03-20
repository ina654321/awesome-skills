# Examples

## 10.1 Doubly-Curved Roof Surface

### Rhino Commands

```text
Phase 1: Create Guide Curves
1. CPlane → Top (set construction plane)
2. InterpCrv → Draw 6 curves across X-axis
   - Use Osnap: Near, Interp
   - Space curves evenly across 20m span
   
3. InterpCrv → Draw 3 rail curves across Y-axis
   - These define the curvature profile

Phase 2: Build Surface
1. NetworkSrf
   - Select all 9 curves (6 + 3)
   - Adjust Continuity: G2 (curvature)
   - OK
   
2. Analyze → Frame (check surface curvature)

Phase 3: Refine
1. F10 (show control points)
2. Select and move CVs to adjust form
3. F11 (hide control points)
4. MatchSrf → Adjust edges if needed
```

### Grasshopper Alternative

```text
1. Params → Geometry → Curve
   - Right-click → Set Multiple Curves
   - Select all guide curves
   
2. Curve → Division → Divide Curve
   - Count: 50
   - Output: Points

3. List → Tree → Stream Filter
   - Connect points from all divisions
   
4. Surface → Freeform → Network Surface
   - Curves input: grafted guide curves
   
5. Surface → Util → Divide Domain²
   - U: 50, V: 50
   
6. Surface → Analysis → Evaluate Surface
   - Input surface + UV points
   - Output: normals for analysis
   
7. Params → Input → Number Slider
   - Connect to divide counts for adjustability
```

## 10.2 Parametric Facade Panel System

```text
Grasshopper Definition:

1. Input Parameters:
   - Panel Width: Number Slider (200-500mm)
   - Panel Height: Number Slider (100-400mm)
   - Depth: Number Slider (50-200mm)
   - Rows: Integer Slider (3-20)
   - Columns: Integer Slider (3-20)
   
2. Generate Grid:
   - Math → Sequence → Series
     - Start: 0
     - Step: Width + Gap
     - Count: Columns
   - Duplicate for Y direction
   
3. Create Base Surface:
   - Curve → Primitive → Rectangle
   - Width: Panel Width
   - Height: Panel Height
   
4. Extrude Panels:
   - Surface → Util → Offset Surface
   - Distance: Depth
   - Cap: Yes (solid)
   
5. Add Radius Edges:
   - Solid → Util → Fillet Edge
   - Radius: 5mm
   
6. Bake to Rhino:
   - Right-click → Bake
   - Set Layer: Facade_Panels
   
7. Create Mullions (optional):
   - Surface → Division → Isotrim
   - Offset inner curves
   - Extrude with smaller depth
```

## 10.3 Structural Analysis with Karamba3D

```text
Grasshopper Workflow:

1. Import Geometry:
   - Mesh → Mesh Edit → Explode (to get faces)
   - Surface → Mesh → Mesh Shadow
   
2. Define Shell Element:
   - Karamba → Cross Section → Shell Section
   - Thickness: 150mm (concrete slab)
   - Material: Karamba → Materials → Concrete C30/37
   
3. Model Mesh as Shell:
   - Karamba → Elements → Model Mesh
   - Input mesh + shell section
   - Element type: Shell (Kirchhoff-Love)
   
4. Define Supports:
   - Karamba → Supports → Support
   - Click mesh vertices at column locations
   - Type: Fixed (all rotations constrained)
   
5. Apply Loads:
   - Karamba → Loads → Load
   - Type: Gravity (-Z, 9.81 m/s²)
   - Mesh Load: Dead load + Live load (2.0 kN/m²)
   
6. Analyze:
   - Karamba → Algorithms → Analyze
   - Iterations: 1000
   - Tolerance: 0.001
   
7. Results Visualization:
   - Karamba → Visualization → Beam View
   - Deformations: Scale 100x
   - Utilization: Color gradient (blue=low, red=high)
   - Max utilization should be < 1.0
```

## 10.4 Kangaroo Physics Form-Finding

```text
Form-Finding Tensile Structure:

1. Define Anchor Points:
   - Params → Geometry → Point
   - Place 4 points at corners (Z = 0)
   - Place 2 elevated points (Z = 5000mm)
   
2. Create Initial Mesh:
   - Surface → Freeform → Quad Panel
   - Connect all points in grid
   - Mesh → Mesh Edit → Mesh From Grid
   
3. Kangaroo Setup:
   - Kangaroo2 → Engine → Kangaroo Goals → Spring
   - Connect mesh edges
   - Strength: 1.0
   
4. Anchor Constraints:
   - Kangaroo → Goals → Anchor
   - Connect anchor points
   - Fixed: True
   
5. Add受力 (Load) Goal:
   - Kangaroo → Goals → Load
   - Apply uniform downward load
   
6. Solve:
   - Kangaroo → Engine → Grabber
   - Click Reset to solve
   - Set iterations: 500
   
7. Output:
   - Kangaroo → Object → Deconstruct Mesh
   - Surface → Mesh → Mesh From Points
   - Bake final form
```

## 10.5 Weaverbird Subdivision

```text
Mesh Smoothing and Subdivision:

1. Create Base Geometry:
   - Surface → Primitive → Box
   - Dimensions: 100x100x100mm
   
2. Convert to Mesh:
   - Mesh → From Surface
   
3. Apply Catmull-Clark Subdivision:
   - Weaverbird → Subdivision → Wb Catmull-Clark
   - Subdivisions: 2
   - Quad topology: On
   
4. Add Creases:
   - Select edge curves
   - Weaverbird → Weaverbird Components → Wb Move Vertices
   - Crease strength: 1.0
   
5. Offset and Hollow:
   - Mesh → Mesh Tools → Offset Mesh
   - Distance: -10mm (inward)
   - Both sides: Off
   
6. Final Output:
   - Join meshes
   - Fill hole if needed
   - Export for 3D printing
```

## 10.6 Environmental Analysis with Ladybug

```text
Solar Radiation Analysis:

1. Import Location:
   - Ladybug → Ladybug Components → Import EPW
   - Select .epw weather file
   - Location: New York JFK
   
2. Sun Path:
   - Ladybug → Solar Access → Sun Path
   - Connect location output
   - Display: 3D sun path spheres
   
3. Radiation Mesh:
   - Ladybug → Solar Access → Radiation Analysis
   - Input geometry: building roof mesh
   - Orientation: North
   - Mesh: 0.5m resolution
   
4. Results:
   - Legend: kWh/m²/year
   - High radiation: South-facing slopes
   - Low radiation: North-facing, shaded areas
   
5. Optimization:
   - Use Galapagos to rotate building
   - Fitness: Maximize solar gain in winter
   - Constraints: Shading from neighbors
```

## 10.7 Architectural Detailing

```text
Curtain Wall with Structural Silicone:

1. Create Grid:
   - Grasshopper → Rectangle → Grid
   - Rows: 20, Columns: 10
   - Cell size: 1500mm x 1500mm
   
2. Panel Geometry:
   - Surface → Util → Divide Domain²
   - Surface → Analysis → Isotrim
   - Surface → From Points → 4-Point Surface
   
3. Add Thickness:
   - Surface → Util → Offset
   - Distance: 12mm (triple-glazed unit)
   
4. Create Mullions:
   - Curve → Primitive → Rectangle
   - Width: 60mm
   - Extrude along grid lines
   - Filleting: 3mm radius
   
5. Structural Silicone Joint:
   - Curve → Division → Divide
   - Offset curves by 6mm
   - Create tapered geometry

Export to Revit:
1. Rhino.Inside Revit → Import 3DM
2. Match layers to Revit categories
3. Assign materials
4. Generate schedule
```
