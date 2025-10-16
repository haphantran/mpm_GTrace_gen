# CPS Traceability Framework - AI Agent Guide

## Project Overview
This is a **traceability framework for Cyber-Physical Systems (CPS)** that models transformations, models, and their trace relationships using a model-driven engineering approach.

## Important Files
- **src_artifacts/metaModel.xml** - Core metamodel definition (stable, may have additions)
- **src_artifacts/MPM_trace_example.xml** - Example instance (may change completely)

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

## Multi-Platform Model-Driven Engineering
The framework supports transforming abstract models into multiple platform-specific models (e.g., Arduino, RIOT, Contiki) with full traceability of transformation decisions and element mappings.

## When Working with This Project
1. **Always check** the current `src_artifacts/metaModel.xml` for the complete class hierarchy and relationships
2. **Always check** the example XML files in `src_artifacts/` for current usage patterns
3. **Expect** new metamodel classes/relationships to be added over time
4. **Expect** example files to demonstrate different scenarios than described here
