# Quick Start Guide

## Installation

```bash
# Install the package
uv pip install -e .
```

## Run the Example

```bash
# Generate visualization for the recommended example
.venv/bin/generate-global-trace src_artifacts/smart_home.xml -o output_g_trace/smart_home.html

# Open in browser
open output_g_trace/smart_home.html
```

## What You'll See

An interactive D3.js visualization showing:
- **5 trace nodes** organized by levels (L0, L1, L2)
- **Solid lines** showing transformation/execution relationships
- **Dotted lines** showing ancestor links (trace version evolution)
- **Color coding** by node type

### Trace Levels

- **Level 0** (Requirements → Architecture):
  - `Trace_Req2Arch_v1` - Baseline decomposition
  - `Trace_Req2Arch_v2_EnergyOpt` - Energy-optimized version (has ancestor link to v1)

- **Level 1** (Architecture → PIM):
  - `Trace_Arch2PIM_PID` - PID control algorithm
  - `Trace_EnergyArch2PIM` - Low-power optimization (has ancestor link to v2)

- **Level 2** (PIM → PSM):
  - `Trace_PIM2PSM_ESP32` - ESP32 platform mapping

### Ancestor Links

The dotted lines show trace version relationships:
```
Trace_Req2Arch_v1
    ⋮ (ancestor)
Trace_Req2Arch_v2_EnergyOpt
    ⋮ (ancestor)
Trace_EnergyArch2PIM
```

## Understanding the Example

Read the detailed explanation: [SMART_HOME_EXAMPLE.md](SMART_HOME_EXAMPLE.md)

**Key concepts**:
1. One transformation can have multiple executions (different versions)
2. Traces can have ancestor links showing evolution
3. Multiple design paths from same requirements
4. Simple trace structure: 1 rule, 1-2 links per trace

## Project Structure

```
src_artifacts/
├── metaModel.xml                 # Metamodel definition (includes ancestor relation)
├── smart_home.xml        # ⭐ Recommended simple example
├── mpm_4_levels_trace.xml        # 4-level working example
└── MPM_trace_example.xml         # Original example showing ancestor usage
```

## Next Steps

- Read [SMART_HOME_EXAMPLE.md](SMART_HOME_EXAMPLE.md) for detailed process explanation
- Check [TRACE_VISUALIZATION_GUIDE.md](TRACE_VISUALIZATION_GUIDE.md) for visualization strategies
- See [CLAUDE.md](CLAUDE.md) for metamodel documentation
