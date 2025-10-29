# Smart Home Multi-Platform Trace Example

## Overview

This example demonstrates a **Smart Home IoT System** with **4 transformation levels**, **branching paths**, and **version tracking** for complete design traceability.

**File**: [src_artifacts/smart_home.xml](src_artifacts/smart_home.xml)

---

## System Goal

Transform smart home requirements into multiple platform-specific code implementations:
1. **Control Branch (v1)**: Standard PID control → ESP32 → C++
2. **Control Branch (v2)**: Energy-optimized adaptive control
3. **Analytics Branch (v1)**: Data analytics → Server → Python/Java

---

## Transformation Flow

### **Level 0: Requirements → Architecture**

**Input Model**: `SmartHomeRequirements`

**Transformation**: `Requirements2Architecture` (2 executions, 2 versions)

#### Execution V1
- **Trace**: `Trace_Req2Arch_v1` (**version="1"**)
- **Intent**: FunctionalDecomposition with component-based strategy
- **Links**: TempReq → TempSensor, Heater

#### Execution V2 (Energy Optimized)
- **Trace**: `Trace_Req2Arch_v2_EnergyOpt` (**version="2"**, ancestor: v1)
- **Intent**: EnergyAwareDecomposition with 30% power reduction
- **Links**: TempReq → LowPowerSensor, SmartHeater

**Output Model**: `SmartHomeArchitecture` (branching point!)

---

### **Level 1A: Architecture → Control PIM**

**Input Model**: `SmartHomeArchitecture`

**Transformation**: `Architecture2ControlPIM` (2 executions, 2 versions)

#### Execution V1 (PID)
- **Trace**: `Trace_Arch2ControlPIM_PID` (**version="1"**)
- **Intent**: AlgorithmSelection - PID algorithm
- **Links**: TempSensor → TemperatureInput, Heater → PIDController

#### Execution V2 (Adaptive)
- **Trace**: `Trace_Arch2ControlPIM_Adaptive` (**version="2"**, ancestor: v1 PID)
- **Intent**: AdaptiveAlgorithmSelection - Adaptive algorithm
- **Links**: LowPowerSensor → TemperatureInput, SmartHeater → AdaptiveController

**Output Model**: `TempControlPIM`

---

### **Level 1B: Architecture → Analytics PIM (BRANCH!)**

**Input Model**: `SmartHomeArchitecture`

**Transformation**: `Architecture2AnalyticsPIM` (1 execution)

- **Trace**: `Trace_Arch2Analytics` (**version="1"**)
- **Intent**: AnalyticsDesign with time-series processing
- **Links**: TempSensor → DataCollector, HistoricalData → TrendAnalyzer

**Output Model**: `DataAnalyticsPIM`

---

### **Level 2A: Control PIM → ESP32 PSM**

**Input Model**: `TempControlPIM`

**Transformation**: `ControlPIM2PSM` (1 execution)

- **Trace**: `Trace_ControlPIM2ESP32` (**version="1"**)
- **Intent**: EmbeddedPlatformMapping to ESP32
- **Links**: PIDController → ESP32_Task, TemperatureInput → ADC_Channel

**Output Model**: `ESP32_PSM`

---

### **Level 2B: Analytics PIM → Server PSM (BRANCH!)**

**Input Model**: `DataAnalyticsPIM`

**Transformation**: `AnalyticsPIM2PSM` (1 execution)

- **Trace**: `Trace_Analytics2Server` (**version="1"**)
- **Intent**: ServerPlatformMapping to Linux Server
- **Links**: DataCollector → RESTEndpoint, TrendAnalyzer → AnalyticsService

**Output Model**: `Server_PSM`

---

### **Level 3A: ESP32 PSM → C++ Code**

**Input Model**: `ESP32_PSM`

**Transformation**: `ESP32_PSM2Code` (1 execution)

- **Trace**: `Trace_ESP32_CPP` (**version="1"**)
- **Intent**: CodeGeneration in C++
- **Links**: ESP32_Task → temp_control_task(), ADC_Channel → adc1_get_raw()

**Output Model**: `ESP32_CPP_Code`

---

### **Level 3B: Server PSM → Python/Java Code**

**Input Model**: `Server_PSM`

**Transformation**: `ServerPSM2Code` (2 executions, same version)

#### Execution 1 (Python)
- **Trace**: `Trace_Server2Python` (**version="1"**)
- **Intent**: CodeGeneration in Python with FastAPI
- **Links**: RESTEndpoint → @app.post(), AnalyticsService → class TrendAnalyzer

**Output Model**: `Python_Code`

#### Execution 2 (Java)
- **Trace**: `Trace_Server2Java` (**version="1"**)
- **Intent**: CodeGeneration in Java with Spring Boot
- **Links**: RESTEndpoint → @PostMapping(), AnalyticsService → class TrendAnalyzer

**Output Model**: `Java_Code`

---

## Version Tracking Strategy

### Version Attribute
Each trace has a **`version` attribute** (type: NUMBER) to identify which design path it belongs to:

```xml
<nodes xmi:type="mpm_trace:TraceModel" name="Trace_Req2Arch_v1" version="1">
  <!-- Baseline design path -->
</nodes>

<nodes xmi:type="mpm_trace:TraceModel" name="Trace_Req2Arch_v2_EnergyOpt" version="2">
  <!-- Energy-optimized design path -->
</nodes>
```

### How Versions Work

**Version 1 Path (Baseline Control)**:
- L0: `Trace_Req2Arch_v1` (version="1")
- L1: `Trace_Arch2ControlPIM_PID` (version="1")
- L2: `Trace_ControlPIM2ESP32` (version="1")
- L3: `Trace_ESP32_CPP` (version="1")

**Version 2 Path (Energy Optimized)**:
- L0: `Trace_Req2Arch_v2_EnergyOpt` (version="2")
- L1: `Trace_Arch2ControlPIM_Adaptive` (version="2")

**Version 1 Path (Analytics)**:
- L1: `Trace_Arch2Analytics` (version="1")
- L2: `Trace_Analytics2Server` (version="1")
- L3: `Trace_Server2Python` (version="1")
- L3: `Trace_Server2Java` (version="1")

**Key Rule**: Traces with the **same version number** belong to the **same design path**.

---

## Ancestor Links

The **`ancestor` attribute** shows version evolution:

```xml
<!-- V2 evolved from V1 -->
<nodes xmi:type="mpm_trace:TraceModel" name="Trace_Req2Arch_v2_EnergyOpt"
       version="2"
       ancestor="//@nodes.27">  <!-- Points to v1 -->
```

**Ancestor vs Version**:
- **Version**: Groups traces in the same design path
- **Ancestor**: Shows how one version evolved from another

**Example**:
- `Trace_Arch2ControlPIM_Adaptive` (v2) has ancestor pointing to `Trace_Arch2ControlPIM_PID` (v1)
- This means: "Version 2 was refined from Version 1"

---

## Complete Design Paths

### Path 1: Baseline Control → ESP32 C++ (Version 1)
```
SmartHomeRequirements
  ↓ [Requirements2Architecture v1] → Trace v1
SmartHomeArchitecture
  ↓ [Architecture2ControlPIM PID] → Trace v1
TempControlPIM
  ↓ [ControlPIM2PSM ESP32] → Trace v1
ESP32_PSM
  ↓ [ESP32_PSM2Code] → Trace v1
ESP32_CPP_Code
```

**All traces**: version="1"

---

### Path 2: Energy Optimized Control (Version 2)
```
SmartHomeRequirements
  ↓ [Requirements2Architecture v2] → Trace v2 (ancestor: v1)
SmartHomeArchitecture
  ↓ [Architecture2ControlPIM Adaptive] → Trace v2 (ancestor: v1 PID)
TempControlPIM
  (continues to ESP32...)
```

**All traces**: version="2"

---

### Path 3: Analytics → Python Server (Version 1)
```
SmartHomeRequirements
  ↓ [Requirements2Architecture v1] → Trace v1
SmartHomeArchitecture
  ↓ [Architecture2AnalyticsPIM] → Trace v1
DataAnalyticsPIM
  ↓ [AnalyticsPIM2PSM] → Trace v1
Server_PSM
  ↓ [ServerPSM2Code Python] → Trace v1
Python_Code
```

**All traces**: version="1"

---

### Path 4: Analytics → Java Server (Version 1)
```
(Same as Path 3 until Server_PSM)
Server_PSM
  ↓ [ServerPSM2Code Java] → Trace v1
Java_Code
```

**All traces**: version="1"

---

## Simplified Trace Structure

Each trace has **1 rule** with **1-2 trace links** for clarity:

### Example: Trace_Req2Arch_v1
```xml
<nodes xmi:type="mpm_trace:TraceModel" name="Trace_Req2Arch_v1" version="1">
  <contains name="DecomposeToComponents">
    <intents name="FunctionalDecomposition">
      <params name="strategy = component_based"/>
    </intents>
    <traceLinks name="TempReq -> TempSensor"/>
    <traceLinks name="TempReq -> Heater"/>
  </contains>
</nodes>
```

**Components**:
- **version="1"**: This trace belongs to design path version 1
- **Rule name**: What was done (DecomposeToComponents)
- **Intent**: Why it was done (FunctionalDecomposition)
- **Parameters**: How it was done (component_based strategy)
- **Links**: Element mappings (TempReq maps to TempSensor and Heater)

---

## Key Concepts Demonstrated

### 1. Version Tracking
- **version attribute** groups traces into design paths
- Traces with same version belong together
- Enables querying: "Show me all traces for version 1"

### 2. Branching Paths
- Architecture splits into **Control** and **Analytics** concerns
- Server PSM generates **both Python and Java** code
- Multiple valid implementation paths from same requirements

### 3. Ancestor Links
- Show design evolution and refinement
- Version 2 traces point to their Version 1 origins
- Creates a lineage: v1 → v2 (energy optimized)

### 4. Multi-Level Traceability
- **Level 0**: Requirements → Architecture
- **Level 1**: Architecture → PIM (branching!)
- **Level 2**: PIM → PSM (platform-specific)
- **Level 3**: PSM → Code (C++, Python, Java)

### 5. Multiple Code Outputs
- Same PSM generates multiple language implementations
- Python (FastAPI) and Java (Spring Boot) from same Server_PSM
- Shows platform versatility

---

## Visualization Features

Run the visualization:
```bash
.venv/bin/generate-global-trace src_artifacts/smart_home.xml
open output_g_trace/smart_home.html
```

**What you'll see**:
- **Node labels**: Show trace name with version (e.g., "Trace_Req2Arch_v1 (v1)")
- **Colors**: Nodes colored by transformation level (L0-L3)
- **Solid lines**: Transformation dependencies
- **Dotted blue lines**: Ancestor relationships
- **Tooltip**: Hover to see version, transformation, rules, and level
- **Interactive**: Drag nodes, zoom, reset positions

**Legend shows**:
- Level colors (L0, L1, L2, L3)
- Solid lines = Dependencies
- Dotted lines = Ancestors (version evolution)

---

## Benefits

### 1. Complete Traceability
Follow requirements all the way to code in any language

### 2. Version Management
Clear grouping of traces by design path version

### 3. Design Evolution
Ancestor links show how designs were refined

### 4. Multi-Platform Support
Single architecture → multiple platforms (ESP32, Server)

### 5. Multi-Language Support
Single PSM → multiple languages (C++, Python, Java)

### 6. Impact Analysis
- "Which traces belong to version 2?" → Filter by version="2"
- "How did v2 evolve from v1?" → Follow ancestor links
- "What code is generated?" → Trace path to Level 3

---

## File Statistics

- **Total nodes**: 41
- **Metamodels**: 3
- **Roles**: 2
- **Models**: 8
- **Transformations**: 7
- **Executions**: 10
- **Traces**: 10 (2 with ancestor links)
- **Levels**: 4 (L0, L1, L2, L3)
- **Versions**: 2 (baseline and energy-optimized)
- **Code Outputs**: 3 (C++, Python, Java)

Complex enough to show real multi-platform scenarios, simple enough to understand!
