# Wireless Sensor Network - Multi-Platform Integration Example

## Overview

This example demonstrates a **Wireless Sensor Network (WSN)** system with **3 transformation levels**, **System Diagram integration**, **Model-to-Text code generation**, and **version tracking**.

**File**: [src_artifacts/wireless_sensor_network.xml](src_artifacts/wireless_sensor_network.xml)

---

## System Goal

Transform a global view of a wireless sensor network into platform-specific C code through system integration:
1. **Level 0 (M2M)**: GlobalView → Platform-Specific Models (Arduino, RIOT, Contiki)
2. **Level 1 (M2M)**: PSMs → System Diagram (Multi-platform integration)
3. **Level 2 (M2T)**: System Diagram → C Code (Platform-specific code generation)

---

## Architecture Overview

```
GlobalView (Abstract sensor network)
    ↓ L0 (Model-to-Model)
    ├─→ Arduino_PSM
    ├─→ RIOT_PSM
    └─→ Contiki_PSM
    ↓ L1 (Integration)
SystemDiagram (Multi-platform mesh network)
    ↓ L2 (Model-to-Text)
    ├─→ Arduino_C_Code
    ├─→ RIOT_C_Code
    └─→ Contiki_C_Code
```

**Key Features**:
- **9 traces total** (with 3 ancestor links)
- **3 transformation levels**: M2M → Integration → M2T
- **System Diagram** integrates all platforms
- **Only C code** (simplified, consistent)
- **3 IoT platforms**: Arduino, RIOT OS, Contiki OS

---

## Transformation Flow

### **Level 0: GlobalView → Platform-Specific Models (M2M)**

**Input**: `GlobalView` - Abstract specification of sensor network

#### Arduino Platform (2 versions)

**Transformation**: `GenArduino`

**Version 1**:
- **Trace**: `Trace_GenArduino_v1` (version="1")
- **Intent**: NetworkConfiguration with WiFi
- **Links**: SensorNode → WiFiBoard

**Version 2** (ancestor: v1):
- **Trace**: `Trace_GenArduino_v2` (version="2", ancestor → v1)

**Output**: `Arduino_PSM`

#### RIOT Platform (2 versions)

**Transformation**: `GenRIOT`

**Version 1**: `Trace_GenRIOT_v1` (version="1")

**Version 2**: `Trace_GenRIOT_v2` (version="2", ancestor → v1)

**Output**: `RIOT_PSM`

#### Contiki Platform (1 version)

**Transformation**: `GenContiki`

**Version 1**: `Trace_GenContiki_v1` (version="1")

**Output**: `Contiki_PSM`

---

### **Level 1: PSMs → System Diagram (Integration)**

**Input**: `Arduino_PSM`, `RIOT_PSM`, `Contiki_PSM`

**Transformation**: `PSM2SystemDiagram` (Model-to-Model)

**Trace**: `Trace_PSM2SD_v1` (version="1")
- **Intent**: SystemIntegration with mesh topology
- **Links**:
  - Arduino_PSM → ArduinoNodes
  - RIOT_PSM → RIOTNodes
  - Contiki_PSM → ContikiNodes

**Output**: `SystemDiagram` (integrated multi-platform network)

**Purpose**: This level integrates all three platform-specific models into a single system diagram, representing the complete sensor network with nodes from all platforms working together in a mesh topology.

---

### **Level 2: System Diagram → C Code (M2T)**

**Input**: `SystemDiagram`

#### Arduino C Code (2 versions)

**Transformation**: `Arduino2Code` (Model-to-Text)

**Version 1**:
- **Trace**: `Trace_Arduino2C_v1` (version="1")
- **Intent**: Model2Text with C language
- **Params**: template = arduino_sensor.c
- **Links**: ArduinoNodes → setup(), SensorReading → loop()

**Version 2** (ancestor: v1):
- **Trace**: `Trace_Arduino2C_v2` (version="2", ancestor → v1)

**Output**: `Arduino_C_Code`

#### RIOT C Code (1 version)

**Transformation**: `RIOT2Code` (Model-to-Text)

**Version 1**:
- **Trace**: `Trace_RIOT2C_v1` (version="1")

**Output**: `RIOT_C_Code`

#### Contiki C Code (1 version)

**Transformation**: `Contiki2Code` (Model-to-Text)

**Version 1**:
- **Trace**: `Trace_Contiki2C_v1` (version="1")

**Output**: `Contiki_C_Code`

---

## Three-Level Traceability

### Level 0: Abstraction to Platform (M2M)
- **Type**: Model-to-Model transformation
- **Purpose**: Generate platform-specific models from abstract specification
- **Metamodel**: PSMM
- **Example**: GlobalView → Arduino_PSM (WiFi configuration)

### Level 1: Multi-Platform Integration (M2M)
- **Type**: Model-to-Model transformation
- **Purpose**: Integrate multiple platform models into system view
- **Metamodel**: SystemDiagramMM
- **Example**: 3 PSMs → SystemDiagram (mesh network)

### Level 2: System to Code (M2T)
- **Type**: Model-to-Text transformation
- **Purpose**: Generate executable C code from integrated system
- **Metamodel**: ATL (transformation language)
- **Example**: SystemDiagram → Arduino_C_Code (C functions)

---

## Why System Diagram Integration?

The System Diagram serves as a **crucial integration layer**:

1. **Multi-Platform View**: Combines Arduino, RIOT, and Contiki into one network
2. **System-Level Decisions**: Mesh topology, gateway configuration, routing
3. **Realistic Scenario**: Real WSN deployments use multiple platforms
4. **Traceability Checkpoint**: Capture how individual PSMs integrate into complete system
5. **Code Generation Input**: Generate platform-specific code with system-level context

**Example**: The Arduino code knows about RIOT and Contiki nodes in the system because it's generated from the SystemDiagram, not just Arduino_PSM.

---

## Version Tracking

**Version 1 Paths** (baseline):
- `Trace_GenArduino_v1` → `Trace_PSM2SD_v1` → `Trace_Arduino2C_v1`
- `Trace_GenRIOT_v1` → `Trace_PSM2SD_v1` → `Trace_RIOT2C_v1`
- `Trace_GenContiki_v1` → `Trace_PSM2SD_v1` → `Trace_Contiki2C_v1`

**Version 2 Paths** (evolved with ancestor links):
- `Trace_GenArduino_v2` → `Trace_PSM2SD_v1` → `Trace_Arduino2C_v2`
- `Trace_GenRIOT_v2` → `Trace_PSM2SD_v1` → (branches to v1 code)

All v2 traces have ancestor links to their v1 origins.

---

## Code Outputs

From System Diagram, we generate **3 C code outputs**:

| **Platform** | **Output Model** | **Use Case** |
|--------------|------------------|--------------|
| Arduino | `Arduino_C_Code` | Arduino sketches (.ino) |
| RIOT | `RIOT_C_Code` | RIOT OS applications |
| Contiki | `Contiki_C_Code` | Contiki processes |

**All C code** for consistency and simplicity.

---

## Trace Content Strategy

**Detailed Traces** (3 examples):
1. `Trace_GenArduino_v1` - L0 platform model generation
2. `Trace_PSM2SD_v1` - L1 multi-platform integration with 3 trace links
3. `Trace_Arduino2C_v1` - L2 Model-to-Text with template

**Simplified Traces** (6 traces):
- All v2 traces (showing evolution)
- Remaining L0 and L2 traces

---

## Key Concepts Demonstrated

### 1. **Three Transformation Levels**
- **L0**: Abstract → Platform (M2M)
- **L1**: Multi-Platform → Integrated System (M2M)
- **L2**: System → Code (M2T)

### 2. **System Integration**
- Multiple platforms combined into single system
- Mesh topology across heterogeneous nodes
- System-level trace decisions

### 3. **Model-to-Text Traceability**
- From integrated system to platform-specific code
- Template-based code generation
- Model elements → Code functions mapping

### 4. **Version Tracking**
- v1 = baseline
- v2 = evolved (with ancestor links)
- Works across all 3 levels

### 5. **Realistic IoT Scenario**
- Heterogeneous network (3 different platforms)
- System integration before code generation
- Multiple code outputs from single system

---

## Visualization Features

Generate visualization:
```bash
.venv/bin/generate-global-trace src_artifacts/wireless_sensor_network.xml
open output_g_trace/wireless_sensor_network.html
```

**What you'll see**:
- **9 trace nodes** arranged in 3 levels (L0, L1, L2)
- **L0 (blue)**: Platform model generation
- **L1 (green)**: System integration
- **L2 (yellow)**: Code generation
- **Solid lines**: Transformation flow between levels
- **Dotted blue lines**: 3 ancestor links (v1 → v2)
- **Integration point**: All L0 traces flow into single L1 trace (SystemDiagram)
- **Branching**: L1 trace flows to 3 L2 traces (one per platform)

**Legend**:
- ━━ Transformation Flow (Between Levels)
- ┅┅ Version Evolution (Within Same Transformation)

---

## Complexity Metrics

- **Total nodes**: 47
- **Metamodels**: 7 (Ecore, ATL, LTrace, GlobalViewMM, PSMM, SystemDiagramMM, CodeMM)
- **Roles**: 3 (Network Engineer, IoT Engineer, Embedded System Engineer)
- **Models**: 8 (1 GlobalView, 3 PSMs, 1 SystemDiagram, 3 Code)
- **Transformations**: 7
  - 3 at L0 (M2M to platforms)
  - 1 at L1 (M2M integration)
  - 3 at L2 (M2T to code)
- **Executions**: 9
- **Traces**: 9 (3 detailed, 6 simplified)
- **Levels**: 3 (L0: M2M, L1: Integration, L2: M2T)
- **Versions**: 2 (baseline and evolved)
- **Ancestor links**: 3
- **Integration points**: 1 (System Diagram)

---

## Benefits

### 1. **Clear Three-Level Structure**
- L0: Abstract → Platform
- L1: Platform → System (integration)
- L2: System → Code

### 2. **Realistic System Integration**
- Shows how multiple platforms combine
- System-level traceability
- Multi-platform mesh network

### 3. **Model-to-Text Traceability**
- Code generated from integrated system
- Template-based generation
- Trace system elements to code

### 4. **Simplified Code Generation**
- Only C (no C++, Rust complexity)
- Consistent across all platforms
- Easy to understand

### 5. **Version Management**
- Track evolution across all 3 levels
- Ancestor links show improvements
- Works with system integration

---

## Use Cases

### For Network Engineers
- Understand multi-platform system integration
- See mesh topology decisions in SystemDiagram
- Trace network configuration to code

### For IoT Engineers
- See platform model generation (L0)
- Understand system integration (L1)
- Trace to platform-specific code (L2)

### For Embedded System Engineers
- Understand code generation from system model
- See Model-to-Text transformation decisions
- Trace system elements to C functions

### For Researchers
- Study multi-level traceability (M2M → M2M → M2T)
- Analyze system integration patterns
- Understand heterogeneous IoT networks

---

## Summary

This wireless sensor network example demonstrates:

✅ **Three transformation levels** (L0: M2M, L1: Integration, L2: M2T)
✅ **System Diagram integration** (multi-platform mesh)
✅ **Model-to-Text traceability** (system → C code)
✅ **Multi-platform support** (Arduino, RIOT, Contiki)
✅ **Consistent code generation** (all C)
✅ **Version tracking** (v1, v2 with ancestors)
✅ **Realistic complexity** (system integration before code gen)

**Perfect balance of complexity and clarity - shows real multi-platform IoT development with complete traceability!**
