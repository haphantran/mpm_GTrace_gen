# CPS Traceability Framework - Global Trace Generator

A **model-driven traceability framework** for Cyber-Physical Systems (CPS) that generates interactive visualizations of multi-level transformations, models, and trace relationships.

## Overview

This project models and visualizes traceability in CPS development through:
- **Multi-level transformations** (Requirements → Architecture → PIM → PSM → Code → Deployment)
- **Multiple execution versions** of the same transformation
- **Platform variants** (ESP32, Arduino, RIOT OS, etc.)
- **Design alternatives** (PID vs Fuzzy Logic, energy vs security optimizations)
- **Interactive D3.js visualizations** with draggable nodes

## Project Structure

```
mpm_trace_GTrace_gen/
├── src_artifacts/
│   ├── metaModel.xml                          # Core metamodel definition
│   ├── MPM_trace_example.xml                  # Original example
│   ├── mpm_4_levels_trace.xml                 # 4-level trace example
│   ├── smart_building_5_levels_trace.xml      # 5-level Smart Building IoT example
│   └── smart_building_multi_exec_trace.xml    # Multi-execution/version example
├── generate_global_trace.py                   # Main visualization generator
├── pyproject.toml                             # Project configuration
├── CLAUDE.md                                  # Project instructions for AI agents
└── TRACE_VISUALIZATION_GUIDE.md               # Ancestry visualization guide
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
.venv/bin/generate-global-trace src_artifacts/smart_home.xml

# Output: output_g_trace/smart_home.html

# Specify custom output name (still goes to output_g_trace/)
.venv/bin/generate-global-trace src_artifacts/mpm_4_levels_trace.xml -o my_trace.html

# Output: output_g_trace/my_trace.html
```

### Option 2: After activating the virtual environment
```bash
source .venv/bin/activate
generate-global-trace src_artifacts/smart_home.xml
```

### Option 3: Run the Python script directly
```bash
python generate_global_trace.py src_artifacts/smart_home.xml
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

## Example Models

### 1. **smart_home.xml** ⭐ RECOMMENDED
Multi-branch Smart Home IoT system with **4 transformation levels**:
- **Multiple execution versions** (baseline and energy-optimized)
- **Ancestor links** showing trace version evolution (blue dotted lines)
- **Branching paths**: Control (Embedded) + Analytics (Server)
- **Code generation**: C++, Python, and Java variants
- **10 traces** showing different design decisions

**Branches**:
- Path A: Requirements → Control PIM → ESP32 PSM → C++ Code
- Path B: Requirements → Analytics PIM → Server PSM → Python/Java Code

See [BRANCHING_PATHS_EXAMPLE.md](BRANCHING_PATHS_EXAMPLE.md) for detailed explanation.

```bash
.venv/bin/generate-global-trace src_artifacts/smart_home.xml
# Output: output_g_trace/smart_home.html
```

### 2. **mpm_4_levels_trace.xml**
Working 4-level example demonstrating multi-level traceability:
- Platform-specific models (Arduino, RIOT, Contiki)
- Multiple transformations per level
- Proper level hierarchy (L0 → L3)

### 3. **smart_building_5_levels_trace.xml**
Complete 5-level transformation chain for a Smart Building IoT system:
- **Level 1**: Requirements → System Architecture
- **Level 2**: System Architecture → Platform-Independent Model (PIM)
- **Level 3**: PIM → Platform-Specific Models (ESP32, Sensor Network)
- **Level 4**: PSM → Code Generation (C++, configuration files)
- **Level 5**: Code → Deployment Packages

Features:
- Real HVAC control with PID algorithm
- MQTT communication protocol
- ESP32 platform mapping
- FreeRTOS task scheduling
- OTA firmware updates

### 2. **smart_building_multi_exec_trace.xml**
Extended example with **multiple executions** and **trace versions**:

**Multiple Versions**:
- `v1.0` - Baseline design
- `v2.0_EnergyOptimized` - Low-power sensors, energy harvesting
- `v3.0_SecureMode` - TLS encryption, secure boot

**Platform Variants**:
- ESP32 (WiFi, MQTT, 240MHz)
- Arduino Uno (Serial, 16MHz, memory-optimized)
- RIOT OS (6LoWPAN, CoAP, Nordic nRF52840)

**Algorithm Variants**:
- PID control (classic)
- Fuzzy Logic control (Mamdani inference)

### 3. **mpm_4_levels_trace.xml**
4-level trace example for testing basic functionality

## Visualization Features

The generated HTML visualization includes:

- **Interactive D3.js force-directed graph**
- **Draggable nodes** - Click and drag to rearrange
- **Color-coded nodes**:
  - 🔵 Blue - MetaModels
  - 🟢 Green - Models
  - 🟠 Orange - Transformations
  - 🟣 Purple - Transformation Executions
  - 🔴 Red - Trace Models
- **Hover tooltips** - Show node details
- **Zoom and pan** - Navigate large graphs
- **Link relationships**:
  - Solid lines - Metamodel-defined relationships
  - Dotted lines - Inferred ancestry (see guide below)

## Ancestry Visualization

For multi-execution traces, see [TRACE_VISUALIZATION_GUIDE.md](TRACE_VISUALIZATION_GUIDE.md) for:

- **Dotted link strategies** for trace ancestry
- **Version evolution** (vertical dotted lines)
- **Variant siblings** (horizontal dotted lines)
- **Design propagation** (diagonal dotted lines)
- **Detection algorithms** for inferring relationships
- **Interactive comparison** features

## Metamodel

The core metamodel ([src_artifacts/metaModel.xml](src_artifacts/metaModel.xml)) defines:

**Primary Types**:
- `MetaModel` - Defines structure/schema
- `Model` - Instances conforming to metamodels
- `Transformation` - Model-to-model transformations
- `TransformationExecution` - Execution instances
- `TraceModel` - Contains traced rules
- `TracedRule` - Transformation intents and trace links
- `Viewpoint` - Different model perspectives

**Key Relationships**:
- Model → Transformation (`In` - input)
- Transformation → Model (`Out` - output)
- Transformation → TransformationExecution (`exec`)
- TransformationExecution → TraceModel (`generates`)
- TraceModel → TracedRule (`contains`)

**Role Types**:
- IoT_Engineer
- Network_Engineer
- Data_Engineer
- Embedded_System_Engineer

## Development

### Project Structure

```python
# Main generator class
class GlobalTraceGeneratorD3:
    def parse_nodes()           # Parse XML nodes
    def extract_trace_models()  # Extract trace information
    def build_d3_graph()        # Build graph structure
    def generate_html()         # Generate interactive visualization
```

### Adding New Examples

1. Create new XML file in `src_artifacts/`
2. Follow metamodel structure from [metaModel.xml](src_artifacts/metaModel.xml)
3. Use consistent naming for multiple executions:
   - `Exec_{Name}_v{version}_{Variant}`
   - `Trace_{Name}_v{version}_{Variant}`
4. Run generator:
   ```bash
   uv run generate-global-trace src_artifacts/your_new_example.xml
   ```

## Examples of Real-World CPS Scenarios

The examples model realistic IoT/CPS scenarios:

- **Smart Building Energy Management**
  - Temperature control (PID/Fuzzy Logic)
  - Occupancy-based automation
  - Energy harvesting support

- **Multi-Platform Deployment**
  - ESP32 (high-performance, WiFi)
  - Arduino (low-cost, constrained resources)
  - RIOT OS (IoT operating system, 6LoWPAN)

- **Communication Protocols**
  - MQTT (publish-subscribe)
  - CoAP (constrained devices)
  - Serial (wired communication)

- **Security Variants**
  - TLS encryption
  - Device authentication
  - Secure boot
  - Intrusion detection

## Troubleshooting

### Command not found: generate-global-trace
Make sure you've installed the package first:
```bash
uv pip install -e .
```

### XML parsing errors
- Ensure XML is well-formed
- Check that all XMI references use correct node indices
- Validate against metamodel structure

### Visualization not displaying
- Check browser console for JavaScript errors
- Ensure output HTML file was generated
- Open in a modern browser (Chrome, Firefox, Safari)

## Contributing

See [CLAUDE.md](CLAUDE.md) for project instructions and guidelines for AI agents working on this codebase.

## License

[Add your license here]

## References

- **Model-Driven Engineering** - Using metamodels to define transformations
- **Multi-Platform Model (MPM)** - Cross-platform development approach
- **D3.js** - Data visualization library
- **ATL** - ATLAS Transformation Language
- **SysML** - Systems Modeling Language
