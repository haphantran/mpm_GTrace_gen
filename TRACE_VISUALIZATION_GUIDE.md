# Multi-Version Trace Visualization Guide

## Overview
This document describes how to visualize trace ancestry relationships using **dotted links** for trace models generated from multiple executions of the same transformation.

## Trace Ancestry Concept

Since the metamodel doesn't have explicit ancestry links, we can **deduce ancestry relationships** based on:
1. **Same source transformation** - Multiple executions of the same transformation
2. **Version progression** - Indicated by version numbers in trace names and parameters
3. **Variant types** - Different design decisions (optimization targets, platform choices)

## Visualization Strategy

### Solid Links (Metamodel-defined)
These are direct relationships defined in the metamodel:
- **Transformation → TransformationExecution** (`exec` relation)
- **TransformationExecution → TraceModel** (`generates` relation)
- **Model → Transformation** (`In` relation - input)
- **Transformation → Model** (`Out` relation - output)
- **TraceModel → TracedRule** (`contains` relation)
- **TracedRule → Intent/TraceLink** (`intents`, `traceLinks` relations)

### Dotted Links (Inferred Ancestry)
These show relationships between trace model **versions/variants**:

#### 1. **Version Lineage** (Vertical Dotted Lines)
Connect trace models from the same transformation that represent version evolution:
```
Trace_Req2SysArch_v1.0
    ⋮ (dotted)
Trace_Req2SysArch_v2.0_EnergyOptimized
    ⋮ (dotted)
Trace_Req2SysArch_v3.0_SecureMode
```

**Identification criteria:**
- Same base transformation name
- Sequential version numbers (v1.0 → v2.0 → v3.0)
- Evolution of same design concern

#### 2. **Variant Branches** (Horizontal Dotted Lines)
Connect trace models representing alternative design choices at the same level:
```
Trace_PIM2PSM_ESP32 ⋯⋯⋯ Trace_PIM2PSM_Arduino ⋯⋯⋯ Trace_PIM2PSM_RIOT
```

**Identification criteria:**
- Same source transformation or parallel transformations
- Same version number but different suffixes (ESP32, Arduino, RIOT)
- Different platforms/strategies/optimizations

#### 3. **Cross-Level Dependencies** (Diagonal Dotted Lines)
Connect traces when a specific trace version influences traces in the next level:
```
Trace_Req2SysArch_v2.0_EnergyOptimized
    ⋱ (dotted diagonal)
        Trace_EnergyOptArch2PSM
```

**Identification criteria:**
- Trace name carries forward optimization/variant suffix
- Parameters reference parent trace decisions
- Design decision propagation across levels

## Detection Algorithm for Visualization

### Pseudo-code for Ancestry Detection:

```python
def detect_ancestry_links(trace_models):
    ancestry_links = []

    # 1. Detect Version Lineage
    grouped_by_base_name = group_by_transformation(trace_models)
    for base_name, traces in grouped_by_base_name.items():
        sorted_traces = sort_by_version(traces)
        for i in range(len(sorted_traces) - 1):
            ancestry_links.append({
                'from': sorted_traces[i],
                'to': sorted_traces[i + 1],
                'type': 'version_evolution',
                'style': 'vertical_dotted'
            })

    # 2. Detect Variant Branches
    grouped_by_level = group_by_transformation_level(trace_models)
    for level, traces in grouped_by_level.items():
        same_version_traces = group_by_version(traces)
        for version, variant_traces in same_version_traces.items():
            if len(variant_traces) > 1:
                # Create mesh of dotted links between variants
                for i, trace1 in enumerate(variant_traces):
                    for trace2 in variant_traces[i+1:]:
                        ancestry_links.append({
                            'from': trace1,
                            'to': trace2,
                            'type': 'variant_sibling',
                            'style': 'horizontal_dotted'
                        })

    # 3. Detect Cross-Level Dependencies
    for trace in trace_models:
        variant_suffix = extract_variant_suffix(trace.name)
        if variant_suffix:
            # Look for traces in next level with same suffix
            child_traces = find_traces_with_suffix(
                trace_models,
                variant_suffix,
                next_level(trace.level)
            )
            for child in child_traces:
                ancestry_links.append({
                    'from': trace,
                    'to': child,
                    'type': 'design_propagation',
                    'style': 'diagonal_dotted'
                })

    return ancestry_links
```

### Helper Functions:

```python
def extract_version(trace_name):
    """Extract version like 'v1.0', 'v2.0' from trace name"""
    import re
    match = re.search(r'v(\d+\.\d+)', trace_name)
    return match.group(1) if match else None

def extract_variant_suffix(trace_name):
    """Extract variant like 'EnergyOptimized', 'ESP32', 'Secure'"""
    import re
    # After version number, get suffix
    match = re.search(r'v\d+\.\d+_(.+)$', trace_name)
    return match.group(1) if match else None

def get_base_transformation_name(trace_name):
    """Extract base transformation name without version/variant"""
    # Remove 'Trace_' prefix and version/variant suffix
    import re
    base = trace_name.replace('Trace_', '')
    base = re.sub(r'_v\d+\.\d+.*$', '', base)
    return base
```

## Visualization Layout Suggestions

### D3.js Force-Directed Graph
```javascript
// Different link styles based on relationship type
const linkStyles = {
    'metamodel': {
        'stroke': '#333',
        'stroke-width': 2,
        'stroke-dasharray': null
    },
    'version_evolution': {
        'stroke': '#0066cc',
        'stroke-width': 1.5,
        'stroke-dasharray': '5,5'
    },
    'variant_sibling': {
        'stroke': '#cc6600',
        'stroke-width': 1,
        'stroke-dasharray': '2,3'
    },
    'design_propagation': {
        'stroke': '#00cc66',
        'stroke-width': 1,
        'stroke-dasharray': '8,4,2,4'
    }
};
```

### Layered Layout (Hierarchical)
```
Level 1:  [Trace_v1.0] ⋯⋯ [Trace_v2.0] ⋯⋯ [Trace_v3.0]
              │              │              │
              ↓              ↓              ↓
Level 2:  [PIM_v1_PID] ⋯⋯⋯⋯⋯⋯⋯⋯ [PIM_v2_Fuzzy]
              │                            │
              ↓                            ↓
Level 3:  [ESP32] ⋯ [Arduino] ⋯ [RIOT]   [ESP32_Fuzzy]
```

## Visual Legend

| Link Type | Style | Color | Meaning |
|-----------|-------|-------|---------|
| Solid line | ──────── | Black | Metamodel-defined relationship |
| Dotted vertical | ⋮ | Blue | Version evolution (same transformation) |
| Dotted horizontal | ⋯⋯⋯ | Orange | Variant siblings (alternative designs) |
| Dash-dot diagonal | ⋱ | Green | Design decision propagation |

## Example Trace Chains in the Model

### Chain 1: Version Evolution
```
Requirements2SystemArchitecture
├─> Exec_v1.0 ──> Trace_v1.0 (baseline)
├─> Exec_v2.0 ──> Trace_v2.0_EnergyOptimized
└─> Exec_v3.0 ──> Trace_v3.0_SecureMode

Ancestry: Trace_v1.0 ⋮ Trace_v2.0 ⋮ Trace_v3.0
```

### Chain 2: Platform Variants
```
PIM2PlatformSpecific
├─> Exec_ESP32 ──> Trace_PIM2PSM_ESP32
├─> Exec_Arduino ──> Trace_PIM2PSM_Arduino
└─> Exec_RIOT ──> Trace_PIM2PSM_RIOT

Ancestry: ESP32 ⋯⋯⋯ Arduino ⋯⋯⋯ RIOT (siblings)
```

### Chain 3: Algorithm Variants
```
SystemArch2PlatformIndependent
├─> Exec_v1.0 ──> Trace_SysArch2PIM_v1.0_PID
└─> Exec_v2.0 ──> Trace_SysArch2PIM_v2.0_FuzzyLogic

Ancestry: PID ⋯⋯⋯ FuzzyLogic (alternative algorithms)
```

## Interactive Features

When implementing visualization:

1. **Hover on dotted link** → Show ancestry relationship type and reason
2. **Click on trace node** → Highlight all related traces (ancestors, descendants, siblings)
3. **Filter by variant type** → Show only specific design path (e.g., energy-optimized chain)
4. **Compare traces** → Side-by-side view of trace models to see differences in intents/parameters

## Trace Comparison View

When comparing two related traces, highlight differences:

```
Trace_v1.0                          Trace_v2.0_EnergyOptimized
──────────────────────────────────────────────────────────────
control_algorithm = PID      →      control_algorithm = energy_aware
sensor_density = normal      →      sensor_density = reduced
                             +      power_mode = low_power
                             +      harvesting_type = solar
```

## Implementation Tips

1. **Store metadata** - Add annotations to trace models with:
   - `version_number`
   - `variant_type`
   - `parent_trace` (manual annotation if needed)

2. **Use naming conventions** - Consistent naming helps automated detection:
   - `Trace_{TransformationName}_v{major}.{minor}_{VariantSuffix}`

3. **Color coding** - Use colors to represent:
   - Optimization targets (blue = performance, green = energy, red = security)
   - Platform types (purple = embedded, yellow = desktop)
   - Design maturity (light to dark for v1 → v2 → v3)

## Query Examples

Users might want to ask:
- "Show all traces derived from v2.0 energy-optimized architecture"
- "Compare PID vs Fuzzy Logic control traces"
- "What changed between ESP32 v1.0 and v2.0 implementations?"

The visualization should support these queries through filtering and highlighting.
