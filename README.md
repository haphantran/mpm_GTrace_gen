# CPS Traceability Framework - Global Trace Generator

A **model-driven traceability framework** for Cyber-Physical Systems (CPS) that generates interactive visualizations showing how changes propagate through multi-level model transformations.

## Overview

This project demonstrates **element-level traceability** in Model-Driven Engineering (MDE) for wireless sensor networks:

- **Multi-abstraction levels** (PIM → PSM → Code)
- **Element-level trace links** showing specific model element mappings
- **Change impact analysis** - trace how changes flow through transformations
- **Platform-specific models** (Arduino, RIOT, Contiki)
- **Interactive D3.js visualizations** with three node types (Models, TraceModels, Trace Links)

## Project Structure

```
mpm_trace_GTrace_gen/
├── src_artifacts/
│   ├── metaModel.xml                    # Core MPM_trace metamodel definition
│   └── WSN_region_trace.xml             # Wireless Sensor Network example with element-level traces
├── output_g_trace/
│   └── WSN_region_trace.html            # Pre-generated visualization
├── docs/
│   └── WSN_Region_Trace_Explanation.md  # Detailed example explanation (archived)
├── generate_global_trace.py             # Visualization generator script
├── pyproject.toml                       # Python project configuration
├── CLAUDE.md                            # Project instructions for AI agents
├── WIRELESS_SENSOR_NETWORK_EXAMPLE.md   # Example documentation with change impact analysis
├── README.md                            # This file
└── QUICK_START.md                       # Quick start guide
```

## Requirements

- **Python 3.8+**
- **uv** (recommended package manager)

## Installation

Install the package to make the `generate-global-trace` command available:

```bash
# Install the package
uv pip install -e .

# Activate the virtual environment
source .venv/bin/activate
```

This installs the package in editable mode and adds the script to your virtual environment's PATH.

## Usage

After installation, run the trace generator using one of these methods:

### Option 1: Using the full path to the script

```bash
# Generate visualization (outputs to output_g_trace/ by default)
.venv/bin/generate-global-trace src_artifacts/WSN_region_trace.xml

# Output: output_g_trace/WSN_region_trace.html

# Specify custom output name (still goes to output_g_trace/)
.venv/bin/generate-global-trace src_artifacts/WSN_region_trace.xml -o my_trace.html

# Output: output_g_trace/my_trace.html
```

### Option 2: After activating the virtual environment

```bash
source .venv/bin/activate
generate-global-trace src_artifacts/WSN_region_trace.xml
```

### Option 3: Run the Python script directly

```bash
python3 generate_global_trace.py src_artifacts/WSN_region_trace.xml
```

**Note**: All HTML outputs are automatically saved to the `output_g_trace/` folder.

### Command-line Options

```bash
generate-global-trace --help

Options:
  input_xml              Path to the MPM trace XML file
  -o, --output OUTPUT    Output HTML file name (default: output_g_trace/<xml_basename>.html)
  -h, --help            Show this help message
```

**Output folder**: All HTML files are saved to `output_g_trace/` by default.

## Example Model

### **WSN_region_trace.xml** - Wireless Sensor Network Example

Demonstrates **element-level traceability** for a wireless sensor network with multiple platform targets:

**Model Flow**:

- **PIM Level**: GlobalView (network topology model)
  - Contains Region with diameter specification (100m coverage)
- **PSM Level**: Three platform-specific models
  - Arduino_PSM - Arduino platform configuration
  - RIOT_PSM - RIOT OS platform configuration
  - Contiki_PSM - Contiki platform configuration
- **Code Level**: Platform-specific C code
  - Arduino_C_Code
  - RIOT_C_Code
  - Contiki_C_Code

**Element-Level Trace Links** (3 total):

1. **M2M Trace (GlobalView → Arduino_PSM)**: RegionDiameter → NetworkDiameter
2. **M2M Trace (GlobalView → Contiki_PSM)**: RegionDiameter → NetworkDiameter
3. **M2T Trace (Contiki_PSM → Contiki_C_Code)**: NetworkDiameter → MAX_HOP_COUNT
   - Derivation rule: `ceiling(diameter / 10m per hop)`
   - Example: 100m diameter → 10 hops

**Change Impact Analysis**:

When you change `RegionDiameter` from 100m to 200m in GlobalView:

- Contiki_PSM NetworkDiameter automatically updates to 200m (via trace link)
- Contiki_C_Code MAX_HOP_COUNT recalculates to 20 hops (via derivation rule)

See [WIRELESS_SENSOR_NETWORK_EXAMPLE.md](WIRELESS_SENSOR_NETWORK_EXAMPLE.md) for complete explanation.

```bash
# Generate visualization
.venv/bin/generate-global-trace src_artifacts/WSN_region_trace.xml

# Output: output_g_trace/WSN_region_trace.html
# Or open pre-generated: output_g_trace/WSN_region_trace.html
```

## Visualization Features

The generated HTML visualization includes:

- **Interactive D3.js force-directed graph**
- **Draggable nodes** - Click and drag to rearrange
- **Three node types with distinct shapes**:
  - **Ellipses** - Models (colored by abstraction level)
    - 🟣 Purple - PIM (Platform-Independent Models)
    - 🟢 Green - PSM (Platform-Specific Models)
    - 🟡 Yellow - Code artifacts
  - **Diamonds** - TraceModels (always 🔵 blue, represent transformation traces)
  - **Rounded rectangles** - Trace Links (individual element-to-element mappings)
- **Hover tooltips** - Show detailed information:
  - Models: name, abstraction level, metamodel
  - TraceModels: transformation name, I/O models, traced rules
  - Trace Links: source/target element paths, link type (copies/derives)
- **Two link types**:
  - **Solid gray arrows** - Transformation flow (Model → TraceModel → Model)
  - **Dashed green arrows** - Containment (TraceModel → Trace Links it contains)
- **Dark mode toggle** - Switch between light/dark themes with persistent preference
- **Zoom and pan controls** - Navigate the graph
- **Reset/center view** - Return to default view

## Metamodel

The core metamodel ([src_artifacts/metaModel.xml](src_artifacts/metaModel.xml)) defines:

**Primary Types**:

- `MetaModel` - Defines structure/schema for models
- `Model` - Instances conforming to metamodels
  - Has `LevelOfAbstraction` attribute (PIM, PSM, Code)
- `Transformation` - Model-to-model or model-to-text transformations
- `TransformationExecution` - Execution instances of transformations
- `TraceModel` - Contains traced rules that document transformation decisions
- `TracedRule` - Contains intents and trace links between model elements
- `TraceLink` - Element-level mappings with source/target paths and link types
- `Viewpoint` - Different perspectives on models

**Key Relationships**:

- Model → Transformation (`In` - input models)
- Transformation → Model (`Out` - output models)
- Transformation → TransformationExecution (`exec` - execution instances)
- TransformationExecution → TraceModel (`generates` - produces traces)
- TraceModel → TracedRule (`contains` - traced transformation rules)
- TracedRule → TraceLink (`traceLinks` - element-to-element mappings)

**Role Types**:

- IoT_Engineer
- Network_Engineer
- Data_Engineer
- Embedded_System_Engineer

## Development

### Python Script Structure

```python
# Main generator class
class GlobalTraceGeneratorD3:
    def parse_nodes()                # Parse XML nodes from megamodel
    def extract_trace_models()       # Extract TraceModels and their trace links
    def extract_trace_links()        # Extract individual element-level trace links
    def build_dependency_graph()     # Build transformation I/O dependencies
    def calculate_levels()           # Calculate hierarchical layout levels
    def generate_html()              # Generate interactive D3.js visualization
```

### Adding New Examples

1. Create new XML file in `src_artifacts/`
2. Follow metamodel structure from [metaModel.xml](src_artifacts/metaModel.xml)
3. Define models with `LevelOfAbstraction` attribute (PIM, PSM, Code)
4. Create transformations with input/output relationships:
   - Input: Model has `In="//@nodes.X"` pointing to Transformation
   - Output: Transformation has `Out="//@nodes.Y"` pointing to output Model
5. Add TraceModels with TracedRules containing TraceLinks:
   - `sourceElementPath` - Path to source model element
   - `targetElementPath` - Path to target model element
   - `linkType` - Relationship type (copies, derives, refines, etc.)
6. Run generator:

   ```bash
   python3 generate_global_trace.py src_artifacts/your_new_example.xml
   ```

## Use Cases

This framework supports various Model-Driven Engineering scenarios:

**Wireless Sensor Networks**:

- Multi-platform deployment (Arduino, RIOT, Contiki)
- Network topology and coverage modeling
- Routing parameter derivation from topology
- Element-level traceability for change impact analysis

**Traceability Applications**:

- **Change Impact Analysis** - Understand downstream effects of model changes
- **Compliance Documentation** - Trace requirements to implementation
- **Reverse Engineering** - Understand transformation decisions
- **Model Evolution** - Track how models change over time
- **Multi-Platform Consistency** - Ensure consistent mappings across platforms

## Troubleshooting

### Command not found: generate-global-trace

Make sure you've installed the package first:

```bash
uv pip install -e .
```

### XML parsing errors

- Ensure XML is well-formed
- Check that all XMI references use correct node indices (e.g., `//@nodes.0`)
- Validate against metamodel structure in [metaModel.xml](src_artifacts/metaModel.xml)
- Ensure `LevelOfAbstraction` attribute is set for all Model nodes

### Visualization not displaying

- Check browser console for JavaScript errors
- Ensure output HTML file was generated in `output_g_trace/`
- Open in a modern browser (Chrome, Firefox, Safari)
- Try the pre-generated example: `open output_g_trace/WSN_region_trace.html`

### Trace links not appearing

- Verify TraceModel has `contains` relationship to TracedRule
- Ensure TracedRule has `traceLinks` with valid sourceElementPath and targetElementPath
- Check that link names are descriptive (e.g., "NetworkDiameter -> MAX_HOP_COUNT")

## Contributing

See [CLAUDE.md](CLAUDE.md) for project instructions and guidelines for AI agents working on this codebase.

## Documentation

- [WIRELESS_SENSOR_NETWORK_EXAMPLE.md](WIRELESS_SENSOR_NETWORK_EXAMPLE.md) - Complete example walkthrough with change impact analysis
- [CLAUDE.md](CLAUDE.md) - Project instructions for AI agents
- [metaModel.xml](src_artifacts/metaModel.xml) - Core metamodel definition

## References

- **Model-Driven Engineering (MDE)** - Using metamodels to define transformations
- **Multi-Platform Model (MPM)** - Cross-platform development approach
- **Megamodeling** - Higher-order modeling for managing model transformations
- **D3.js** - Data-Driven Documents visualization library
- **Traceability** - Linking artifacts across development lifecycle
