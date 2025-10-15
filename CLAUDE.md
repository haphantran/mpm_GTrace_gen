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

### Key Relationships
- Models and transformations **conform to** metamodels
- Transformations have **input models** (IN) and **output models** (OUT)
- Transformations have **executions** that produce results
- Executions **generate** trace models
- Models can be **associated with roles**
- Models can be **represented through viewpoints**
- Traced rules contain **intents** describing transformation purpose
- Trace links connect **source elements** to **target elements**

## Typical Usage Pattern (from examples)
1. Source model(s) defined with metamodel conformance
2. Transformation(s) defined with input/output model specifications
3. Transformation execution generates:
   - Output model(s)
   - Trace model capturing:
     - Transformation intents (why the transformation was done)
     - Element-to-element trace links
     - Parameters used in the transformation
4. Models associated with appropriate engineering roles
5. Models viewed through different viewpoints as needed

## Multi-Platform Model-Driven Engineering
The framework supports transforming abstract models into multiple platform-specific models (e.g., Arduino, RIOT, Contiki) with full traceability of transformation decisions and element mappings.

## When Working with This Project
1. **Always check** the current `src_artifacts/metaModel.xml` for the complete class hierarchy and relationships
2. **Always check** the example XML files in `src_artifacts/` for current usage patterns
3. **Expect** new metamodel classes/relationships to be added over time
4. **Expect** example files to demonstrate different scenarios than described here
