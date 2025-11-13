# Quick Start Guide

## Installation

```bash
# Install the package
uv pip install -e .
```

## Run the Example

```bash
# Option 1: Open pre-generated visualization
open output_g_trace/WSN_region_trace.html

# Option 2: Regenerate the visualization
python3 generate_global_trace.py src_artifacts/WSN_region_trace.xml

# Option 3: Use the installed command (after activating virtual environment)
source .venv/bin/activate
generate-global-trace src_artifacts/WSN_region_trace.xml
```

## What You'll See

An interactive D3.js visualization showing:

- **Three types of nodes** with distinct shapes:
  - **Ellipses** - Models (7 total: 1 PIM, 3 PSMs, 3 Code artifacts)
  - **Diamonds** - TraceModels (6 total: 3 M2M traces, 3 M2T traces)
  - **Rounded rectangles** - Trace Links (3 element-level mappings)
- **Color coding by abstraction level**:
  - 🟣 Purple - PIM (GlobalView)
  - 🟢 Green - PSM (Arduino_PSM, RIOT_PSM, Contiki_PSM)
  - 🟡 Yellow - Code (Arduino_C_Code, RIOT_C_Code, Contiki_C_Code)
  - 🔵 Blue - TraceModels (always blue, regardless of abstraction)
- **Two link types**:
  - Solid gray arrows - Transformation flow
  - Dashed green arrows - Containment (TraceModel contains Trace Links)

## Element-Level Trace Links

The example demonstrates **3 element-level trace links**:

1. **GlobalView → Arduino_PSM**
   - `RegionDiameter → NetworkDiameter`
   - Link type: copies

2. **GlobalView → Contiki_PSM**
   - `RegionDiameter → NetworkDiameter`
   - Link type: copies

3. **Contiki_PSM → Contiki_C_Code**
   - `NetworkDiameter → MAX_HOP_COUNT`
   - Link type: derives
   - Transformation rule: `ceiling(diameter / 10m per hop)`

## Interactive Features

- **Hover tooltips** - See detailed information for each node
- **Drag nodes** - Rearrange the layout
- **Zoom/Pan** - Navigate the graph
- **Dark mode toggle** (🌙) - Switch themes
- **Reset view** - Return to default layout

## Understanding the Example

Read the complete explanation: [WIRELESS_SENSOR_NETWORK_EXAMPLE.md](WIRELESS_SENSOR_NETWORK_EXAMPLE.md)

**Key concepts**:

1. **Multi-platform transformation** - One PIM generates three PSMs (Arduino, RIOT, Contiki)
2. **Element-level traceability** - Track specific model elements through transformations
3. **Derivation rules** - Capture HOW values are calculated (diameter → hop count)
4. **Change impact analysis** - Understand what changes when you modify upstream models

## Example Change Impact

**Scenario**: Change network diameter from 100m to 200m in GlobalView

**Impact** (traceable via element-level links):

1. Contiki_PSM `NetworkDiameter` updates to 200m (via "copies" link)
2. Contiki_C_Code `MAX_HOP_COUNT` recalculates to 20 hops (via "derives" link with 10m/hop rule)

See [WIRELESS_SENSOR_NETWORK_EXAMPLE.md](WIRELESS_SENSOR_NETWORK_EXAMPLE.md) for detailed change impact analysis.

## Project Structure

```
src_artifacts/
├── metaModel.xml              # Core MPM_trace metamodel definition
└── WSN_region_trace.xml       # ⭐ Wireless Sensor Network example
```

## Next Steps

- Read [WIRELESS_SENSOR_NETWORK_EXAMPLE.md](WIRELESS_SENSOR_NETWORK_EXAMPLE.md) for complete example explanation
- Study [metaModel.xml](src_artifacts/metaModel.xml) to understand the metamodel
- See [CLAUDE.md](CLAUDE.md) for project instructions and metamodel documentation
- Try modifying [WSN_region_trace.xml](src_artifacts/WSN_region_trace.xml) and regenerating
