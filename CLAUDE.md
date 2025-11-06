# CPS Traceability Framework - AI Agent Guide

## Project Overview
This is a **megamodel-based traceability framework for Cyber-Physical Systems (CPS)** that captures multi-level model transformations, their execution traces, and version evolution relationships. The framework uses a model-driven engineering approach to maintain comprehensive traceability across complex transformation chains.

## Important Files
- **src_artifacts/metaModel.xml** - Core megamodel metamodel definition (MPM_trace metamodel)
- **src_artifacts/wireless_sensor_network.xml** - Multi-level wireless sensor network example (L0→L1→L2 transformations)
- **src_artifacts/WSN_element_trace.xml** - Element-level tracing example showing attribute traces (Arduino PSM → Code)
- **src_artifacts/WSN_region_trace.xml** - **Region dimension tracing example** showing how changes in Region (diameter, coverageDimension) propagate through Contiki/TinyOS PSMs to C code
- **generate_global_trace.py** - Python script to generate interactive D3.js visualizations of global traces showing both Models and TraceModels
- **output_g_trace/** - Directory containing generated HTML visualizations

> ⚠️ **IMPORTANT**: Always read the actual `src_artifacts/metaModel.xml` and example files for the latest information. The metamodel may have new classes/relationships added, and examples can be completely different from what's described here.

## Core Metamodel Concepts

### Primary Types
- **MetaModel** - Defines the structure/schema that models conform to
- **Model** - Instances conforming to metamodels; can have multiple viewpoint representations
- **Transformation** - Defines model-to-model transformations with input/output models
- **TransformationExecution** - Execution instances of transformations that generate trace models
- **TraceModel** - Contains traced rules that capture transformation intent and element links
- **TracedRule** - Contains transformation intents (with parameters) and trace links between source/target model elements
- **Viewpoint** - Different perspectives on models (e.g., Network, Sensor Data, Control Flow)

### Role Types
- IoT_Engineer
- Network_Engineer
- Data_Engineer
- Embedded_System_Engineer

### Key Relationships (Updated Metamodel)

**Input/Output Model Relationships:**
- **Model → Transformation (Input)**: Model has `In` relation (many) pointing to Transformation(s) it serves as input for
- **Transformation → Model (Output)**: Transformation has `Out` relation (many) pointing to output Model(s)
- ⚠️ **Breaking Change**: Old format had `IN` and `OUT` attributes on Transformation. New format splits these:
  - Input: Stored on Model as `In` attribute
  - Output: Stored on Transformation as `Out` attribute

**Other Relationships:**
- Models and transformations **conform to** metamodels
- Transformations have **exec** relation (many) to TransformationExecution
- TransformationExecution **generates** relation (many) to TraceModel
- Models can be **associated with roles** (associatedWith)
- Models can be **represented through viewpoints** (representedAs)
- Traced rules contain **intents** describing transformation purpose
- Trace links connect **source elements** to **target elements**

## Typical Usage Pattern (from examples)
1. Source model(s) defined with metamodel conformance
2. Define transformation(s) with:
   - Input: Source Model has `In="//@nodes.X"` pointing to Transformation
   - Output: Transformation has `Out="//@nodes.Y"` pointing to output Model
   - Execution: Transformation has `exec="//@nodes.Z"` pointing to TransformationExecution
3. TransformationExecution generates TraceModel via `generates="//@nodes.W"`
4. TraceModel captures:
   - Transformation intents (why the transformation was done)
   - Element-to-element trace links
   - Parameters used in the transformation
5. Models associated with appropriate engineering roles
6. Models viewed through different viewpoints as needed

**Example XML Structure:**
```xml
<!-- Input Model points to Transformation -->
<nodes xmi:type="mpm_trace:Model" name="SourceModel" In="//@nodes.5"/>

<!-- Transformation points to output and execution -->
<nodes xmi:type="mpm_trace:Transformation" name="MyTransform"
       Out="//@nodes.7" exec="//@nodes.8"/>

<!-- Output Model -->
<nodes xmi:type="mpm_trace:Model" name="OutputModel"/>

<!-- Execution generates trace -->
<nodes xmi:type="mpm_trace:TransformationExecution" name="MyExec"
       generates="//@nodes.9"/>

<!-- Trace Model -->
<nodes xmi:type="mpm_trace:TraceModel" name="MyTrace"/>
```

## Multi-Level Transformation Architecture

The framework supports **hierarchical transformation chains** across multiple levels:

### Transformation Levels (as seen in wireless_sensor_network.xml)

- **L0 (Level 0)**: Domain model to platform-specific models
  - Example: GlobalView → Arduino_PSM, RIOT_PSM, Contiki_PSM
  - Multiple transformations at this level (GenArduino, GenRIOT, GenContiki)
  - Each transformation can have multiple executions with version evolution

- **L1 (Level 1)**: Integration/composition of L0 outputs
  - Example: PSMs → SystemDiagram (integration point)
  - Consolidates multiple platform-specific models into unified view

- **L2 (Level 2)**: Code generation from platform models
  - Example: Arduino_PSM → Arduino_C_Code, RIOT_PSM → RIOT_C_Code
  - M2T (Model-to-Text) transformations producing executable code

### Global Trace Visualization

The **generate_global_trace.py** script analyzes megamodel instances and generates interactive visualizations showing **Models**, **TraceModels**, AND **Element-Level Trace Links** in the global trace map:

**Key Features:**
- Parses XML megamodel instances to extract:
  - **Model nodes** (input/output models like GlobalView, PSMs, Code artifacts)
  - **TraceModel nodes** (local traces from individual transformations)
  - **Element-Level Trace Link nodes** (individual trace links extracted from TraceModels)
  - Transformation I/O relationships (which models flow between transformations)
  - TransformationExecution instances and their generated traces
  - Version evolution chains (ancestor relationships between traces)
- Builds **global trace dependencies** by connecting models, traces, and element traces through transformation chains
- Calculates **hierarchical levels** (L0, L1, L2...) using BFS on dependency graph
- Generates **interactive D3.js visualization** with:
  - **Three types of nodes**, all color-coded by level:
    - **Model nodes** (ellipses) - e.g., GlobalView, Arduino_PSM, Arduino_C_Code
    - **TraceModel nodes** (rectangles) - e.g., Trace_GenArduino_v1
    - **Element Trace Link nodes** (diamonds) - e.g., "diameter → transmissionRange"
  - Complete traceability flow showing:
    - Model → TraceModel → Model (high-level transformation flow)
    - Model → ElementTraceLink → Model (detailed element/attribute-level traces)
  - Two types of links:
    - **Solid arrows**: Transformation flow (Model to Trace to Model, Model to ElementTrace to Model)
    - **Dotted arrows**: Version evolution (between trace versions)
  - Tooltips showing:
    - For Models: name, metamodel, level
    - For TraceModels: transformation name, I/O models, traced rules, element-level traces, attribute-level traces
    - For Element Traces: source/target element paths, source/target attributes, link type, parent trace
  - Draggable nodes with zoom and pan capabilities
  - Interactive controls:
    - Reset/center view buttons
    - **Dark mode toggle** (🌙/☀️) with persistent preference storage
    - Smooth transitions between light and dark themes

**Usage:**
```bash
# Generate visualization from default example
python3 generate_global_trace.py

# Generate from specific XML file
python3 generate_global_trace.py src_artifacts/wireless_sensor_network.xml

# Specify output file
python3 generate_global_trace.py src_artifacts/wireless_sensor_network.xml -o custom_output.html
```

**Output:**
- HTML file in `output_g_trace/` directory (default: `<xml_basename>.html`)
- Standalone file with embedded D3.js (no external dependencies except D3 CDN)

## Element-Level and Attribute-Level Traceability

The framework supports **fine-grained traceability** at three levels:

1. **Model-level**: Trace from entire source model to entire target model
   - Example: `GlobalView → Arduino_PSM`

2. **Element-level**: Trace from specific model elements to target elements
   - Example: `GlobalView::Topology::Region → Contiki_PSM::NetworkConfig::ContikiNetworkConfig`
   - Uses `sourceElementPath` and `targetElementPath` attributes in TraceLink

3. **Attribute-level**: Trace from specific attributes to target attributes with transformation rules
   - Example: Region `diameter` (100m) → Calculated `MAX_HOP_COUNT` (10 hops) using "10m per hop" rule
   - Uses `sourceAttribute`, `targetAttribute`, and `linkType` in TraceLink
   - Supports calculated transformations with documented rules in Intent parameters

**TraceLink Attributes:**

```xml
<!-- L0: Copy coverage requirement -->
<traceLinks name="diameter -> diameter"
            sourceElementPath="GlobalView::Topology::Region"
            targetElementPath="Contiki_PSM::NetworkConfig::ContikiNetworkConfig"
            sourceAttribute="diameter"
            targetAttribute="diameter"
            linkType="copies"/>

<!-- L2: Calculate routing parameter using transformation rule -->
<traceLinks name="diameter -> MAX_HOP_COUNT"
            sourceElementPath="Contiki_PSM::NetworkConfig::ContikiNetworkConfig"
            targetElementPath="Contiki_C_Code::Constants::MAX_HOP_COUNT"
            sourceAttribute="diameter"
            targetAttribute="value"
            linkType="derives"/>
<!-- Transformation rule documented in Intent: "10m per hop" -->
<!-- Calculation: ceil(diameter / 10) -->
```

**Real-world Example (WSN_region_trace.xml):**

- **Change scenario**: Region dimension in GlobalView affects routing calculations
- **Impact propagation**:
  - L0: Region → Contiki PSM (diameter → diameter, copies 100m coverage requirement)
  - L2: Contiki PSM → Contiki C Code (diameter → MAX_HOP_COUNT using "10m per hop" transformation rule)
- **Traceability**: Complete attribute-level trace showing how coverage requirements are transformed using platform-specific rules (documented in Intent) to produce routing parameters

## Multi-Platform Model-Driven Engineering

The framework supports transforming abstract models into multiple platform-specific models (e.g., Arduino, RIOT, Contiki, TinyOS) with full traceability of transformation decisions and element mappings.

**Real-world Example (wireless_sensor_network.xml):**
- Single high-level GlobalView model
- Generates 3 platform-specific models (Arduino, RIOT, Contiki PSMs)
- Each transformation has multiple execution versions (v1, v2...)
- PSMs integrated into unified SystemDiagram
- Each PSM transformed to platform-specific C code
- Complete traceability chain: GlobalView → PSM → SystemDiagram → C_Code

## When Working with This Project

1. **Always check** the current `src_artifacts/metaModel.xml` for the complete class hierarchy and relationships
2. **Always check** the example XML files in `src_artifacts/` for current usage patterns
3. **Expect** new metamodel classes/relationships to be added over time
4. **Expect** example files to demonstrate different scenarios than described here
5. **Run generate_global_trace.py** on new examples to visualize the transformation architecture and trace dependencies
