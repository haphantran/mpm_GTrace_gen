# Wireless Sensor Network - Multi-Platform Example

## Overview

This example demonstrates a **Wireless Sensor Network (WSN)** system with **2 transformation levels**, tracing from an abstract global view through platform-specific models to executable C code.

**File**: [src_artifacts/WSN_region_trace.xml](src_artifacts/WSN_region_trace.xml)

---

## System Goal

Transform a global view of a wireless sensor network into platform-specific C code:
1. **Level 0 (M2M)**: GlobalView → Platform-Specific Models (Arduino, RIOT, Contiki)
2. **Level 2 (M2T)**: PSMs → C Code (Platform-specific code generation)

---

## Architecture Overview

```
GlobalView (PIM - Platform Independent Model)
    ↓ L0 (Model-to-Model)
    ├─→ Arduino_PSM (PSM - Platform Specific Model)
    ├─→ RIOT_PSM (PSM)
    └─→ Contiki_PSM (PSM)
    ↓ L2 (Model-to-Text)
    ├─→ Arduino_C_Code (Code)
    ├─→ RIOT_C_Code (Code)
    └─→ Contiki_C_Code (Code)
```

**Key Features**:
- **6 TraceModels total**: 3 at L0 (GlobalView→PSM), 3 at L2 (PSM→Code)
- **2 transformation levels**: M2M → M2T
- **3 IoT platforms**: Arduino, RIOT OS, Contiki OS
- **Detailed trace links**: Focus on Contiki path to demonstrate element-level traceability
- **Color-coded by abstraction level**: Purple (PIM), Green (PSM), Yellow (Code), Blue (TraceModels)

---

## Transformation Flow

### **Level 0: GlobalView → Platform-Specific Models (M2M)**

**Input**: `GlobalView` (PIM) - Abstract specification of sensor network with:
- Topology information
- Region definition with diameter (100 meters)

#### Arduino Platform

**Transformation**: `GenArduino`
**TraceModel**: `Trace_GenArduino` (HIGH-LEVEL only)
**Output**: `Arduino_PSM` (PSM)

#### RIOT Platform

**Transformation**: `GenRIOT`
**TraceModel**: `Trace_GenRIOT` (HIGH-LEVEL only)
**Output**: `RIOT_PSM` (PSM)

#### Contiki Platform (DETAILED TRACING)

**Transformation**: `GenContiki`
**TraceModel**: `Trace_GenContiki` (DETAILED with trace links)
**Output**: `Contiki_PSM` (PSM)

**Trace Links** (Class-level tracing):

1. **Region → ContikiNetworkConfig**
   - **From**: `GlobalView::Topology::Region` (class)
   - **To**: `Contiki_PSM::NetworkConfig::ContikiNetworkConfig` (class)
   - **Type**: `transforms`
   - **Meaning**: The abstract Region concept is transformed into a platform-specific network configuration for Contiki

2. **RegionDiameter → NetworkDiameter**
   - **From**: `GlobalView::Topology::Region::RegionDiameter` (class)
   - **To**: `Contiki_PSM::NetworkConfig::ContikiNetworkConfig::NetworkDiameter` (class)
   - **Type**: `copies`
   - **Meaning**: The region diameter value (100m) is copied from the global view to the Contiki PSM

---

### **Level 2: PSMs → C Code (M2T)**

**Inputs**: `Arduino_PSM`, `RIOT_PSM`, `Contiki_PSM`

#### Arduino C Code

**Transformation**: `Arduino2Code` (Model-to-Text)
**TraceModel**: `Trace_Arduino2C` (HIGH-LEVEL only)
**Output**: `Arduino_C_Code`

#### RIOT C Code

**Transformation**: `RIOT2Code` (Model-to-Text)
**TraceModel**: `Trace_RIOT2C` (HIGH-LEVEL only)
**Output**: `RIOT_C_Code`

#### Contiki C Code (DETAILED TRACING)

**Transformation**: `Contiki2Code` (Model-to-Text)
**TraceModel**: `Trace_Contiki2C` (DETAILED with trace links)
**Output**: `Contiki_C_Code`

**Trace Link** (Class-to-code tracing with line numbers):

**NetworkDiameter → MAX_HOP_COUNT**
- **From**: `Contiki_PSM::NetworkConfig::ContikiNetworkConfig::NetworkDiameter` (class)
- **To**: `Contiki_C_Code::contiki_network.c::MAX_HOP_COUNT (line 12)` (C constant)
- **Type**: `derives`
- **Meaning**: The network diameter value (100m) is used to derive the maximum hop count constant
- **Derivation Rule**: `MAX_HOP_COUNT = ceiling(NetworkDiameter / 10)` where 10m is the assumed hop distance in Contiki mesh routing
- **Example**: 100m diameter → ceiling(100/10) = 10 hops
- **What is MAX_HOP_COUNT?**: A compile-time constant (`#define MAX_HOP_COUNT 10`) that limits the maximum number of hops a packet can traverse in the mesh network, preventing infinite routing loops

---

## Understanding Trace Links

### What is a Trace Link?

A **trace link** is a relationship that captures how elements from a source model are transformed into elements in a target model. Each trace link records:

- **Source element path**: Where the element comes from (e.g., `GlobalView::Topology::Region`)
- **Target element path**: Where it goes to (e.g., `Contiki_PSM::NetworkConfig::ContikiNetworkConfig`)
- **Link type**: How it's transformed (`transforms`, `copies`, `generates`, `derives`)
- **Context**: Which transformation created this link

### Trace Link Types

1. **transforms**: The source element is structurally transformed into the target
   - Example: `Region → ContikiNetworkConfig` (abstract concept becomes platform-specific config)

2. **copies**: The source element value is directly copied to the target
   - Example: `RegionDiameter → NetworkDiameter` (100m value copied unchanged)

3. **generates**: The source model element generates code/text in the target
   - Example: `ContikiNetworkConfig → network_config` (PSM class generates C struct)

4. **derives**: The target is calculated/derived from the source
   - Example: `NetworkDiameter → MAX_HOP_COUNT` (100m derives to 10 hops)

### Why Class-Level Tracing?

This example uses **class-level tracing** (not attribute-level) because:
- Our implementation supports element-level tracing
- Classes represent meaningful design decisions
- Line numbers show precise code locations
- Easier to visualize and understand

### Example: Complete Trace Chain

Following the **diameter** through the system:

```
RegionDiameter (100m) [GlobalView - PIM]
    ↓ (copies)
NetworkDiameter (100m) [Contiki_PSM - PSM]
    ↓ (derives via calculation: ceil(100/10) = 10)
MAX_HOP_COUNT (10) [Contiki_C_Code line 12 - Code]
```

This shows how an abstract regional property (100m diameter) flows through platform-specific modeling and finally becomes a concrete constant in C code.

---

## Change Impact Analysis Example

The trace links enable powerful **change impact analysis** - understanding what downstream artifacts are affected when you change something upstream.

### Scenario: Expanding Network Coverage

**Change Request**: The deployment area needs to expand from 100 meters to 200 meters diameter.

**Step 1: Identify the Change Location**
- Change: `GlobalView::Topology::Region::RegionDiameter` from 100m to 200m

**Step 2: Follow the Trace Links**

Using our trace links, we can automatically identify all affected artifacts:

1. **L0 Trace Link** (`Trace_GenContiki`):
   - `RegionDiameter → NetworkDiameter` (copies)
   - **Impact**: `Contiki_PSM::NetworkConfig::ContikiNetworkConfig::NetworkDiameter` will change from 100m to 200m

2. **L2 Trace Link** (`Trace_Contiki2C`):
   - `NetworkDiameter → MAX_HOP_COUNT` (derives)
   - **Impact**: `Contiki_C_Code::contiki_network.c::MAX_HOP_COUNT` (line 12) will change from 10 to 20
   - **Calculation**: ceiling(200m / 10m per hop) = 20 hops

**Step 3: Impact Summary**

| Artifact | Current Value | New Value | Change Type |
|----------|---------------|-----------|-------------|
| GlobalView RegionDiameter | 100m | 200m | **Manual Change** |
| Contiki_PSM NetworkDiameter | 100m | 200m | Automatic (copies) |
| Contiki_C_Code MAX_HOP_COUNT | 10 hops | 20 hops | Automatic (derives) |

**Step 4: Actions Required**

1. **Update PIM**: Change RegionDiameter in GlobalView model
2. **Re-run transformations**:
   - Run `GenContiki` to regenerate Contiki_PSM
   - Run `Contiki2Code` to regenerate C code
3. **Verify**: Confirm MAX_HOP_COUNT = 20 in generated code (line 12)
4. **Test**: Network can now route packets across the full 200m diameter

### Benefits of Trace Links for Impact Analysis

✅ **Complete Impact Visibility**: Know exactly which files and lines need regeneration
✅ **No Manual Search**: Don't need to grep through code to find diameter references
✅ **Derivation Rules Captured**: Understand HOW values are calculated (10m per hop rule)
✅ **Confidence in Changes**: Know all downstream effects before making the change
✅ **Documentation**: Trace links serve as living documentation of transformation logic

### Without Trace Links

Without traceability, you would need to:
- ❌ Manually search codebase for "diameter" or related terms
- ❌ Guess which constants might be derived from diameter
- ❌ Hope you found all affected locations
- ❌ Rediscover the hop calculation rule each time
- ❌ Risk missing indirect dependencies

---

## Why Focus Detailed Tracing on Contiki?

The example shows **different levels of tracing granularity**:

- **Arduino & RIOT paths**: High-level TraceModels only (no detailed trace links)
  - Demonstrates that not all transformations need detailed tracing
  - Shows the framework supports varying granularity

- **Contiki path**: Detailed trace links at both L0 and L2
  - **Pedagogical choice**: Demonstrates element-level traceability
  - Shows complete chain: PIM → PSM → Code
  - Illustrates both model-to-model and model-to-text tracing

This **selective tracing** approach is realistic - in practice, you trace what matters most for your use case.

---

## Abstraction Levels

The framework uses **LevelOfAbstraction** to categorize models:

### PIM (Platform Independent Model)
- **Color**: Purple (#9C27B0)
- **Example**: `GlobalView`
- **Purpose**: Abstract, platform-agnostic specification

### PSM (Platform Specific Model)
- **Color**: Green (#4CAF50)
- **Examples**: `Arduino_PSM`, `RIOT_PSM`, `Contiki_PSM`
- **Purpose**: Platform-specific design models

### Code
- **Color**: Yellow (#FFC107)
- **Examples**: `Arduino_C_Code`, `RIOT_C_Code`, `Contiki_C_Code`
- **Purpose**: Executable implementation

### TraceModel
- **Color**: Blue (#2196F3)
- **Examples**: `Trace_GenArduino`, `Trace_GenContiki`, `Trace_Contiki2C`
- **Purpose**: Records transformation traces and trace links

---

## Visualization

Generate the interactive D3.js visualization:

```bash
python3 generate_global_trace.py src_artifacts/WSN_region_trace.xml
open output_g_trace/WSN_region_trace.html
```

### What You'll See

**Nodes**:
- **Ellipses**: Models (colored by abstraction level - Purple/Green/Yellow)
- **Diamonds**: TraceModels (always blue)
- **Rounded rectangles**: Trace Links (sized to fit their names, colored by abstraction level)

**Links**:
- **Solid gray arrows (━━)**: Transformation flow (Model → TraceModel → Model)
- **Dashed green arrows (┅┅)**: Containment (TraceModel contains Trace Links)

**Color Scheme**:
- **Purple**: PIM (Platform Independent Models)
- **Green**: PSM (Platform Specific Models)
- **Yellow**: Code
- **Blue**: TraceModels

**Interactive Features**:
- **Hover** over trace links to see full source/target paths
- **Drag** nodes to rearrange
- **Zoom** and pan
- **Dark mode toggle**
- **Auto-layout** by transformation level (left to right)

---

## Example Trace Link Details

When you hover over a trace link in the visualization, you see:

**Trace Link: RegionDiameter → NetworkDiameter**
- From: `GlobalView::Topology::Region::RegionDiameter`
- To: `Contiki_PSM::NetworkConfig::ContikiNetworkConfig::NetworkDiameter`

This tells you:
1. **What was traced**: The RegionDiameter class
2. **Where it came from**: GlobalView's topology model
3. **Where it went**: Contiki PSM's network configuration
4. **The relationship**: The diameter property flows from abstract to platform-specific

---

## Key Concepts Demonstrated

### 1. **Class-Level Traceability**
- Traces between classes, not individual attributes
- Includes line numbers for code references
- Shows structural transformations

### 2. **Multi-Platform M2M**
- Single PIM to multiple PSMs
- Each platform gets its own transformation
- Selective detailed tracing (Contiki only)

### 3. **Model-to-Text Traceability**
- PSM classes to C code
- Line number precision
- Derived values (calculations during transformation)

### 4. **Selective Granularity**
- Not all transformations need detailed tracing
- Focus effort where it provides value
- Mix of high-level and detailed traces

### 5. **Visual Distinction**
- Different shapes for different node types
- Color-coding by abstraction level
- Dynamic sizing for trace links

---

## File Structure

```
src_artifacts/
├── metaModel.xml              # MPM_trace metamodel with LevelOfAbstraction
└── WSN_region_trace.xml       # This example

output_g_trace/
└── WSN_region_trace.html      # Generated visualization
```

---

## Complexity Metrics

- **Models**: 7 (1 PIM, 3 PSMs, 3 Code models)
- **TraceModels**: 6 (3 for M2M transformations, 3 for M2T transformations)
- **Trace Links**: 4 (2 for Contiki M2M, 2 for Contiki M2T)
- **Transformations**: 6 (3 M2M, 3 M2T)
- **Executions**: 6
- **Abstraction Levels**: 3 (PIM, PSM, Code)
- **Platforms**: 3 (Arduino, RIOT, Contiki)
- **Detailed trace paths**: 1 (Contiki end-to-end)

---

## Benefits

### 1. **Clear Traceability Chain**
- See how abstract concepts become concrete code
- Understand transformation decisions
- Trace value flow (100m → 10 hops)

### 2. **Realistic Complexity**
- Multiple platforms from single source
- Different tracing granularities
- Real IoT development scenario

### 3. **Educational Value**
- Demonstrates class-level tracing
- Shows model-to-model and model-to-text
- Illustrates selective detailed tracing

### 4. **Interactive Exploration**
- Visual representation of traces
- Hover for details
- Easy to understand relationships

---

## Use Cases

### For Network Engineers
- Understand how regional topology affects platform configurations
- See how diameter influences routing (hop count calculation)
- Trace network parameters to code constants

### For IoT Engineers
- See platform-specific model generation
- Understand PSM to code transformation
- Compare different platform approaches

### For Tool Developers
- Study traceability implementation
- Understand megamodel structure
- Learn visualization techniques

### For Researchers
- Analyze multi-level traceability
- Study selective tracing strategies
- Understand heterogeneous platform support

---

## Summary

This wireless sensor network example demonstrates:

✅ **Class-level traceability** with precise line numbers
✅ **Multi-platform support** (Arduino, RIOT, Contiki)
✅ **Selective detailed tracing** (focus on what matters)
✅ **Two transformation types** (M2M and M2T)
✅ **Abstraction level color-coding** (Purple PIM, Green PSM, Yellow Code, Blue TraceModels)
✅ **Interactive visualization** with dynamic sizing
✅ **Complete trace chains** from abstract models to executable code
✅ **Realistic complexity** without overwhelming detail

**Perfect balance of clarity and depth - shows practical traceability in multi-platform IoT development!**
