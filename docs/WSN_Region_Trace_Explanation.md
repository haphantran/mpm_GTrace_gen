# WSN Region Trace Example: Explanation and Change Impact Analysis

## Overview

This document explains the **WSN_region_trace.xml** example, which demonstrates end-to-end traceability in a **multi-platform Wireless Sensor Network (WSN)** system. The example shows:
- **High-level traces** for all three platforms (Arduino, RIOT, Contiki)
- **Detailed element/attribute-level traces** focusing on the Contiki path
- How the **Region.diameter** attribute propagates from high-level specification to executable C code

This represents a realistic scenario where complete system-wide traceability exists at the model level, with selective deep tracing for critical paths.

## WSN Networking Concepts

Before diving into the trace structure, let's clarify the key WSN (Wireless Sensor Network) concepts used in this example:

### Model Classes and Transformation Logic

**Region** (Class in GlobalView):

- **Location**: `GlobalView::Topology::Region`
- **Meaning**: Represents the geographic deployment area for the sensor network
- **Purpose**: High-level specification of network coverage requirements

**RegionDiameter** (Class in Region):

- **Location**: `GlobalView::Topology::Region::RegionDiameter`
- **Unit**: Meters (m)
- **Value**: 100 meters
- **Meaning**: The physical distance across the sensor network deployment area
- **Use**: IoT engineers specify the physical coverage requirement
- **Real-world**: "We need sensors to cover a 100-meter diameter field"

**NetworkDiameter** (Class in ContikiNetworkConfig - PSM):

- **Location**: `Contiki_PSM::NetworkConfig::ContikiNetworkConfig::NetworkDiameter`
- **Unit**: Meters (m)
- **Value**: 100 meters (copied from RegionDiameter)
- **Use**: Preserved in PSM to be used by code generation transformation

**MAX_HOP_COUNT** (C code constant - derived using transformation rule):

- **Location**: `Contiki_C_Code::contiki_network.c::MAX_HOP_COUNT` (line 12)
- **Unit**: Hops (number of relay transmissions)
- **Value**: 10 hops
- **Transformation Rule**: "10m per hop" (Contiki mesh routing standard)
- **Calculation**: `ceil(NetworkDiameter / 10) = ceil(100 / 10) = 10`
- **Use**: Prevents infinite routing loops and ensures messages can reach network edges
- **Real-world**: "Allow up to 10 hops to cover 100m diameter with standard 10m/hop routing"

### Transformation Logic

The traceability chain shows how **coverage requirement classes** are transformed into **routing parameter classes** using platform-specific transformation rules:

```
Class Hierarchy                 Transformation              Generated Code
RegionDiameter (100m)    +    "10m per hop" rule    →    MAX_HOP_COUNT (line 12)
       ↓                           ↓                            ↓
NetworkDiameter (PSM)      Documented in Intent        Constant (10 hops)
```

**Design Rationale:**

1. **Coverage requirement** (RegionDiameter class, 100m) comes from application needs (GlobalView)
2. **Class-level tracing** tracks how RegionDiameter maps to NetworkDiameter in PSM
3. **Transformation rule** (10m per hop) is a Contiki mesh routing standard
4. **Code generation** creates MAX_HOP_COUNT constant with line number information
5. The rule is **documented in the Intent** parameters, making it traceable and reproducible

## System Architecture

### Transformation Chain

The example implements a **2-level transformation chain** across **3 IoT platforms**:

```
                    ┌─> Arduino_PSM ─> Arduino_C_Code
                    │
GlobalView (L0) ────┼─> RIOT_PSM ──────> RIOT_C_Code
                    │
                    └─> Contiki_PSM ──> Contiki_C_Code
                           ↑                  ↑
                      (detailed trace with Region.diameter)
```

**Level 0 (L0)**: GlobalView → 3 PSMs (Arduino, RIOT, Contiki)
**Level 2 (L2)**: Each PSM → Platform-specific C Code

### Models and Their Roles

#### L0 Input Model

1. **GlobalView** (Platform-Independent Model)
   - Contains `Region` element with `diameter` attribute (represents network coverage)
   - Owned by: IoT Engineer
   - Purpose: High-level system specification independent of target platform
   - Feeds into: 3 transformation chains (one per platform)

#### L0 Output / L2 Input Models (PSMs)

2. **Arduino_PSM** (Arduino Platform-Specific Model)
   - Platform-specific configuration for Arduino devices
   - Owned by: Embedded System Engineer
   - Purpose: Arduino-optimized network configuration

3. **RIOT_PSM** (RIOT Platform-Specific Model)
   - Platform-specific configuration for RIOT OS
   - Owned by: Embedded System Engineer
   - Purpose: RIOT-optimized network configuration

4. **Contiki_PSM** (Contiki Platform-Specific Model)
   - Contains `ContikiNetworkConfig` with `diameter` attribute (in meters)
   - Owned by: Embedded System Engineer
   - Purpose: Contiki-specific network configuration
   - **Special**: Has detailed element/attribute traces from GlobalView

#### L2 Output Models (Code)

5. **Arduino_C_Code** - Executable C code for Arduino platform
6. **RIOT_C_Code** - Executable C code for RIOT platform
7. **Contiki_C_Code** - Executable C code for Contiki platform
   - Contains `MAX_HOP_COUNT` constant (routing limit)
   - **Special**: Has detailed trace back to GlobalView.Region.diameter with documented calculation

## Trace Structure

### Two Levels of Traceability

The example demonstrates **selective tracing granularity** for pedagogical purposes:

1. **High-Level Traces** (Arduino, RIOT): Model-level traceability only
   - Sufficient for understanding transformation flow
   - Lower overhead
   - Kept simple to avoid overwhelming the example

2. **Detailed Traces** (Contiki): Model + Element + Attribute level traceability
   - Complete lineage showing element and attribute mappings
   - Enables precise change impact analysis
   - **Selected for demonstration** because it provides a meaningful example of the Region.diameter transformation
   - **Note**: This is a pedagogical choice to keep the example manageable, not a statement about platform importance

### L0 High-Level Traces (Arduino & RIOT)

#### Arduino Path

**Transformation:** `GenArduino` (ATL M2M transformation)

**Trace Model:** `Trace_GenArduino_v1`

- **Minimal trace container** (no traced rules or links)
- Sufficient to indicate transformation occurred
- Enables visualization of transformation flow
- Low overhead for non-critical paths

#### RIOT Path

**Transformation:** `GenRIOT` (ATL M2M transformation)

**Trace Model:** `Trace_GenRIOT_v1`

- **Minimal trace container** (no traced rules or links)
- Sufficient to indicate transformation occurred
- Enables visualization of transformation flow
- Low overhead for non-critical paths

### L0 Detailed Trace (Contiki Path)

**Transformation:** `GenContiki` (ATL M2M transformation)

**Traced Rule:** `MapRegionToContiki`

**Intent:** PlatformMapping

- Parameters:
  - `targetPlatform = Contiki`
  - `networkTopology = mesh`

**Trace Links:**

1. **Element-Level Trace:**
   ```
   Source: GlobalView::Topology::Region
   Target: Contiki_PSM::NetworkConfig::ContikiNetworkConfig
   Type: transforms
   ```
   Captures how the abstract Region concept maps to Contiki's network configuration structure.

2. **Attribute-Level Trace:**
   ```
   Source: GlobalView::Topology::Region.diameter
   Target: Contiki_PSM::NetworkConfig::ContikiNetworkConfig.diameter
   Type: copies
   ```
   Documents that the coverage requirement (`diameter` = 100 meters) is copied directly to the PSM to be used later for routing calculations.

### L2 High-Level Traces (Arduino & RIOT)

#### Arduino Code Generation

**Transformation:** `Arduino2Code` (Acceleo M2T transformation)

**Trace Model:** `Trace_Arduino2C_v1`

- **Minimal trace container** (no traced rules or links)
- Sufficient to indicate code generation occurred
- Enables visualization of transformation flow
- Low overhead for non-critical paths

#### RIOT Code Generation

**Transformation:** `RIOT2Code` (Acceleo M2T transformation)

**Trace Model:** `Trace_RIOT2C_v1`

- **Minimal trace container** (no traced rules or links)
- Sufficient to indicate code generation occurred
- Enables visualization of transformation flow
- Low overhead for non-critical paths

### L2 Detailed Trace (Contiki Path)

**Transformation:** `Contiki2Code` (Acceleo M2T transformation)

**Traced Rule:** `GenerateContikiNetworkCode`

**Intent:** DeriveRoutingLimit

- Parameters:
  - `language = C`
  - `template = contiki_network.c`
  - `transformationRule = 10m per hop (Contiki mesh routing standard)`
  - `calculation = MAX_HOP_COUNT = ceil(diameter / 10)`

**Trace Links:**

1. **Element-Level Trace:**
   ```
   Source: Contiki_PSM::NetworkConfig::ContikiNetworkConfig
   Target: Contiki_C_Code::Structs::network_config
   Type: generates
   ```
   Shows how the PSM network configuration generates a C struct for network routing.

2. **Attribute-Level Trace (Calculated):**
   ```
   Source: Contiki_PSM::NetworkConfig::ContikiNetworkConfig.diameter
   Target: Contiki_C_Code::Constants::MAX_HOP_COUNT
   Type: derives
   ```
   Documents calculated code generation: `diameter` (100m) is transformed using the "10m per hop" rule to produce `MAX_HOP_COUNT` (10 hops). Calculation: ceil(100 / 10) = 10.

## Complete Traceability Chain (Contiki Focus)

The **Global Trace Map** shows the complete Region.diameter lineage through the Contiki path:

```
GlobalView::Region.diameter (100 meters - coverage requirement)
    ↓ [Element Trace: Region → ContikiNetworkConfig]
    ↓ [Attribute Trace: diameter → diameter] (copies via GenContiki)
Contiki_PSM::ContikiNetworkConfig.diameter (100 meters)
    ↓ [Element Trace: ContikiNetworkConfig → network_config]
    ↓ [Attribute Trace: diameter → MAX_HOP_COUNT] (derives with rule: 10m/hop)
Contiki_C_Code::MAX_HOP_COUNT constant (10 hops, calculated: ceil(100/10))
```

**Calculation Logic:**

```c
// In generated C code:
#define MAX_HOP_COUNT 10  // Calculated using transformation rule:
                          // ceil(diameter / 10) = ceil(100 / 10) = 10
                          // Rule: "10m per hop" (Contiki mesh routing standard)
                          // Allows messages to traverse 100m diameter network
```

**Parallel High-Level Traces** (visible in visualization):

```
GlobalView → Arduino_PSM → Arduino_C_Code
GlobalView → RIOT_PSM → RIOT_C_Code
```

This demonstrates:
- **Model-level traceability:** All 3 platforms have complete transformation flow
- **Element-level traceability:** Contiki path shows class/component mappings
- **Attribute-level traceability:** Contiki path shows precise property lineage AND transformation rules

## Change Impact Analysis

### Scenario: Increasing Network Diameter for Larger Deployment

**Context:** The IoT engineer needs to expand the sensor network deployment from 100 meters to 150 meters diameter to cover a larger geographic area (e.g., expanding from a small field to a larger farm). The routing parameters must be recalculated based on the "10m per hop" transformation rule. We need to understand which artifacts are affected and which calculations need to be updated.

### Step 1: Identify the Change

**Changed Element:**
- Model: `GlobalView`
- Element: `Region`
- Attribute: `diameter`
- Old Value: `100` meters
- New Value: `150` meters
- Rationale: Physical deployment area expanded to cover larger field (from 100m to 150m diameter circle)

### Step 2: Query the Global Trace Map

Open the visualization at `output_g_trace/WSN_region_trace.html` and:

1. **Locate GlobalView node** (ellipse at L0)
2. **Observe branching**: 3 solid arrows to Arduino_PSM, RIOT_PSM, Contiki_PSM
3. **Identify element trace diamonds**: Only visible on Contiki path
4. **Follow the detailed Contiki chain** through transformation levels

### Step 3: Trace Forward Dependencies

**Query:** "What artifacts are impacted by changing `GlobalView::Region.diameter`?"

#### High-Level Impact (All Platforms)

**Trace Path:**
```
L0 Model Trace: "GlobalView -> Arduino_PSM"
  └─> Affected Model: Arduino_PSM
  └─> Impact: UNKNOWN (no element-level trace)
  └─> Action: Must review Arduino PSM manually OR regenerate

L0 Model Trace: "GlobalView -> RIOT_PSM"
  └─> Affected Model: RIOT_PSM
  └─> Impact: UNKNOWN (no element-level trace)
  └─> Action: Must review RIOT PSM manually OR regenerate

L0 Model Trace: "GlobalView -> Contiki_PSM"
  └─> Affected Model: Contiki_PSM (DETAILED TRACE AVAILABLE)
  └─> See detailed analysis below ↓
```

**Interpretation:** All three PSMs receive inputs from GlobalView, but only Contiki has traceable Region dependencies.

#### Detailed Impact (Contiki Path Only)

**Trace Path Analysis:**

```
L0 Element Trace: "Region -> ContikiNetworkConfig"
  ├─> Links: GlobalView::Region → Contiki_PSM::ContikiNetworkConfig
  └─> Confirms: ContikiNetworkConfig depends on Region element

L0 Attribute Trace: "diameter -> diameter"
  ├─> Affected Attribute: Contiki_PSM::ContikiNetworkConfig.diameter
  ├─> Current Value: 100 meters → New Value: 150 meters
  ├─> Transformation Intent: PlatformMapping (copy coverage requirement)
  └─> Impact: Must regenerate Contiki_PSM

L2 Element Trace: "ContikiNetworkConfig -> network_config"
  ├─> Links: Contiki_PSM::ContikiNetworkConfig → Contiki_C_Code::network_config
  └─> Confirms: C code struct depends on PSM config

L2 Attribute Trace: "diameter -> MAX_HOP_COUNT"
  ├─> Affected Constant: Contiki_C_Code::Constants::MAX_HOP_COUNT
  ├─> Current Calculation: ceil(100 / 10) = 10 hops
  ├─> New Calculation: ceil(150 / 10) = 15 hops
  ├─> Transformation Rule: "10m per hop" (Contiki mesh routing standard)
  ├─> Transformation Intent: DeriveRoutingLimit
  └─> Impact: Must regenerate Contiki_C_Code with new MAX_HOP_COUNT
```

### Step 4: Impact Summary

#### Directly Impacted Artifacts (Provable via Trace)

**Contiki Platform** (Complete Impact Analysis):

1. **Contiki_PSM** (L0 Output)
   - Element: `ContikiNetworkConfig`
   - Attribute: `diameter` will change from `100` meters to `150` meters
   - Reason: **Traced copy** from `diameter` via GenContiki transformation
   - Confidence: **HIGH** (explicit attribute-level trace)

2. **Contiki_C_Code** (L2 Output)
   - Element: `Constants::MAX_HOP_COUNT`
   - Value: Will change from `10` to `15` hops
   - Calculation: ceil(150 / 10) = 15 (was ceil(100 / 10) = 10)
   - Transformation Rule: "10m per hop" (Contiki mesh routing standard)
   - Reason: **Traced derivation** from `diameter` via Contiki2Code transformation
   - Confidence: **HIGH** (explicit attribute-level trace with documented transformation rule)

#### Potentially Impacted Artifacts (Model-Level Trace Only)

**Arduino Platform** (Uncertain Impact):
- **Arduino_PSM** - May or may not use Region/diameter
- **Arduino_C_Code** - Depends on Arduino_PSM changes
- Confidence: **LOW** (no element-level trace available)
- Recommendation: **Manual review** or **conservative regeneration**

**RIOT Platform** (Uncertain Impact):
- **RIOT_PSM** - May or may not use Region/diameter
- **RIOT_C_Code** - Depends on RIOT_PSM changes
- Confidence: **LOW** (no element-level trace available)
- Recommendation: **Manual review** or **conservative regeneration**

### Step 5: Required Actions

#### Certain Actions (Based on Detailed Traces)

1. **Re-execute Contiki L0 transformation:**
   - Run: `GenContiki` transformation
   - Input: Updated GlobalView with `diameter = 150` meters
   - Output: New Contiki_PSM with `diameter = 150` meters
   - Generate: New trace `Trace_GenContiki_v2` (version evolution)
   - Priority: **REQUIRED** (proven dependency)

2. **Re-execute Contiki L2 transformation:**
   - Run: `Contiki2Code` transformation
   - Input: Updated Contiki_PSM with `diameter = 150` meters
   - Transformation Rule: "10m per hop" (documented in Intent)
   - Output: New Contiki_C_Code with `MAX_HOP_COUNT = 15` (calculated: ceil(150/10) = 15)
   - Generate: New trace `Trace_Contiki2C_v2`
   - Priority: **REQUIRED** (proven dependency)

3. **Re-test Contiki network behavior:**
   - Test routing with new 15-hop limit (increased from 10 hops)
   - Validate network coverage across expanded 150-meter deployment area
   - Verify reliable connectivity between sensor nodes at network edges
   - Confirm messages can traverse the full diameter with the new hop count
   - Test edge cases: messages near the 15-hop limit
   - Monitor routing table updates and convergence time

#### Uncertain Actions (Conservative Approach)

4. **Review or regenerate Arduino artifacts:**
   - Option A: Manual code review to check Region/diameter usage
   - Option B: Conservative regeneration of Arduino_PSM and Arduino_C_Code
   - Decision: Depends on project risk tolerance

5. **Review or regenerate RIOT artifacts:**
   - Option A: Manual code review to check Region/diameter usage
   - Option B: Conservative regeneration of RIOT_PSM and RIOT_C_Code
   - Decision: Depends on project risk tolerance

**Trade-off:** High-level traces provide coverage, but lack precision for surgical updates.

### Step 6: Trace Backward Dependencies (Design Rationale)

**Query:** "Why does Contiki's `MAX_HOP_COUNT` have value 10?"

**Backward Trace:**

```
Contiki_C_Code::MAX_HOP_COUNT (value = 10 hops)
  ↑ [derives from - calculated with transformation rule] Trace_Contiki2C_v1
  ↑ Intent: DeriveRoutingLimit
  ↑ Transformation Rule: "10m per hop (Contiki mesh routing standard)"
  ↑ Calculation: ceil(diameter / 10) = ceil(100 / 10) = 10
Contiki_PSM::ContikiNetworkConfig.diameter (value = 100 meters)
  ↑ [copies from] Trace_GenContiki_v1
GlobalView::Region.diameter (value = 100 meters)
  ↑ ORIGIN: Design decision by IoT Engineer
  ↑ Rationale: Network must cover 100-meter diameter deployment area
```

This explains:

- **What:** The constant's current value (10 hops)
- **Why:** Application requirement (100m coverage) + Platform transformation rule ("10m per hop")
- **How:** Documented transformation rule in Intent parameters ensures reproducibility

## Benefits of Selective Tracing

### 1. Precision for Critical Paths

**Contiki (Detailed Trace):**
- Element trace diamonds in visualization show exact dependencies
- Attribute traces document specific property mappings
- **Surgical change impact analysis** possible
- Example: "diameter change affects MAX_HOP_COUNT calculation" (provable with formula)

**Arduino & RIOT (Minimal Trace):**
- Rectangle trace nodes show transformation exists
- **No traced rules or links** (minimal trace container only)
- Solid arrows show model-to-model flow
- **Conservative change impact analysis** required
- Example: "diameter change MAY affect Arduino_C_Code" (uncertain)
- Significantly lower storage and processing overhead

### 2. Scalability vs. Precision Trade-off

| Aspect | Minimal Trace | Detailed Trace |
|--------|---------------|----------------|
| **Storage** | TraceModel container only (~100 bytes) | Full rules + links (~10KB+) |
| **Overhead** | Minimal | Significant |
| **Content** | No rules or links | Element + Attribute traces |
| **Precision** | None (container only) | High (provable dependencies) |
| **Impact Confidence** | Uncertain (requires review) | High (traceable) |
| **Use Case** | Full system coverage | Critical paths |
| **Visualization** | Rectangle nodes only | Rectangle + Diamond nodes |

### 3. Realistic Engineering Workflow

This example mirrors real-world practice:
- **Not everything needs fine-grained tracing** (cost/benefit)
- **Critical design decisions** (like Region.diameter) get detailed tracking
- **Less critical paths** use lightweight tracing
- Engineers can **upgrade trace granularity** on-demand for specific paths

### 4. Visual Clarity

In the visualization (`output_g_trace/WSN_region_trace.html`):
- **7 model nodes** (ellipses): Complete architecture visible
- **6 trace model nodes** (rectangles): All transformations tracked
- **4 element trace nodes** (diamonds): Only on Contiki path
- **Clean layout**: High-level traces don't clutter diagram
- **Focus on detail**: Diamond nodes draw attention to traced decisions

## Comparison with ProMoTA Framework

This example extends ProMoTA's Global Trace Map concept with **granularity selection**:

### Similarities

1. **Global Trace Map:** All models and traces as nodes in single graph
2. **Element-Level Traces:** Individual trace links as first-class entities
3. **Multi-Level Chains:** L0, L2 transformation levels
4. **Change Impact Analysis:** Forward/backward traceability queries

### Novel Aspects

1. **Selective Granularity:** Mix high-level and detailed traces in same system
2. **Visual Distinction:** Diamond nodes appear only where detailed tracing exists
3. **Scalability:** Reduce trace overhead for non-critical paths
4. **Engineering Realism:** Matches practical MDE workflows

### Use Cases Supported

✅ **Precise Impact Analysis:** "What EXACTLY is affected?" (Contiki path)
✅ **Broad Coverage:** "What transformations exist?" (All paths)
✅ **Risk Assessment:** "Where do we lack detailed tracing?" (Arduino, RIOT)
✅ **Trace Investment:** "Where should we add detail?" (Based on change frequency)
✅ **Design Rationale:** "Why this value?" (Backward trace on Contiki)

## Interactive Exploration

Open the visualization at `output_g_trace/WSN_region_trace.html` to:

### 1. Explore the Architecture

- **Drag nodes** to organize the 3-platform architecture
- **Observe branching** from GlobalView to 3 PSMs at L0
- **Follow parallel paths** through L2 to 3 C code outputs
- **Toggle dark mode** (🌙/☀️ button) for comfortable viewing

### 2. Compare Trace Granularities

**Hover over trace model nodes:**
- **Arduino/RIOT traces** (rectangles): Show minimal/no details
  - "Traced Rules: 0"
  - "Element Traces: 0"
  - "Attribute Traces: 0"
  - Container only - no trace content

- **Contiki traces** (rectangles): Show rich details
  - "Traced Rules: 1"
  - "Element Traces: 1"
  - "Attribute Traces: 1"
  - Expandable lists of element/attribute paths
  - Complete Region.diameter lineage

**Hover over element trace nodes (diamonds):**
- Only visible on Contiki path
- Show source/target element paths
- Show attribute mappings:
  - L0: diameter → diameter (copies)
  - L2: diameter → MAX_HOP_COUNT (derives using "10m per hop" rule)
- Show link types (copies, derives, transforms, generates)
- Display transformation intent and calculation formulas

### 3. Trace Change Impact

**Scenario Simulation:**
1. Locate **GlobalView** node (ellipse, L0)
2. Follow **3 solid arrows** to PSM nodes
3. Notice **diamonds** only on Contiki path
4. Trace **Contiki diamonds** to C code
5. Observe **no diamonds** on Arduino/RIOT paths

**Interpretation:**
- If Region changes: **Certain impact** on Contiki path
- If Region changes: **Uncertain impact** on Arduino/RIOT paths

### 4. Zoom and Focus

- **Zoom in** to read element trace details
- **Pan** to navigate the 3-platform layout
- **Reset/Center** buttons to restore default view

## Conclusion

The **WSN_region_trace** example demonstrates:

### Key Concepts

1. **Multi-Platform MDE:** Single high-level model generates code for 3 IoT platforms
2. **Selective Tracing:** Mix high-level and detailed traces based on criticality
3. **Scalable Traceability:** Balance precision vs. overhead for large systems
4. **Visual Clarity:** Diamond nodes highlight where detailed analysis is possible

### Practical Benefits

- **Precise impact analysis** where it matters most (critical paths)
- **Broad coverage** without trace information overload
- **Engineering realism** reflecting actual MDE practices
- **Visual communication** of traceability investments

### When to Use This Approach

✅ **Large multi-platform systems** where full detailed tracing is too expensive
✅ **Critical design decisions** that need complete lineage (e.g., safety parameters)
✅ **Evolving systems** where trace granularity can be upgraded incrementally
✅ **Team communication** to show which paths have detailed analysis support

This approach is essential for managing complexity in real-world, multi-platform, multi-level model-driven development of CPS systems.
