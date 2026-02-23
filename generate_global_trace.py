#!/usr/bin/env python3
"""
Global Trace Generator with D3.js for CPS Traceability Framework

This script generates an interactive D3.js visualization with draggable nodes.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List
import argparse
import json


class GlobalTraceGeneratorD3:
    def __init__(self, example_xml_path: str):
        self.example_path = example_xml_path
        self.tree = ET.parse(example_xml_path)
        self.root = self.tree.getroot()
        self.nodes = {}
        self.trace_models = {}
        self.transformations = {}
        self.executions = {}
        self.models = {}  # Store Model nodes

    def parse_nodes(self):
        """Parse all nodes and index them"""
        for idx, node in enumerate(self.root.findall('nodes')):
            self.nodes[idx] = node

    def extract_models(self):
        """Extract all Model nodes"""
        for idx, node in self.nodes.items():
            if node.get('{http://www.omg.org/XMI}type') == 'mpm_trace:Model':
                name = node.get('name')
                conforms_to = node.get('conformsTo')
                associated_with = node.get('associatedWith')
                in_ref = node.get('In')  # Transformations this model is input to
                level_of_abstraction = node.get('LevelOfAbstraction')  # PIM, PSM, or Code

                self.models[idx] = {
                    'index': idx,
                    'name': name,
                    'conformsTo': conforms_to,
                    'associatedWith': associated_with,
                    'In': in_ref,
                    'LevelOfAbstraction': level_of_abstraction
                }

    def extract_trace_models(self):
        """Extract all TraceModel nodes"""
        for idx, node in self.nodes.items():
            if node.get('{http://www.omg.org/XMI}type') == 'mpm_trace:TraceModel':
                name = node.get('name')
                conforms_to = node.get('conformsTo')
                ancestor = node.get('ancestor')  # Extract ancestor link
                version = node.get('version')  # Extract version attribute

                traced_rules = []
                for rule in node.findall('contains'):
                    rule_data = {
                        'name': rule.get('name'),
                        'intents': [],
                        'trace_links': []
                    }

                    for intent in rule.findall('intents'):
                        intent_data = {
                            'name': intent.get('name'),
                            'params': [p.get('name') for p in intent.findall('params')]
                        }
                        rule_data['intents'].append(intent_data)

                    for link in rule.findall('traceLinks'):
                        link_data = {
                            'name': link.get('name'),
                            'sourceElementPath': link.get('sourceElementPath'),
                            'targetElementPath': link.get('targetElementPath'),
                            'sourceAttribute': link.get('sourceAttribute'),
                            'targetAttribute': link.get('targetAttribute'),
                            'linkType': link.get('linkType')
                        }
                        rule_data['trace_links'].append(link_data)

                    traced_rules.append(rule_data)

                self.trace_models[idx] = {
                    'index': idx,
                    'name': name,
                    'conformsTo': conforms_to,
                    'ancestor': ancestor,
                    'version': version,
                    'traced_rules': traced_rules
                }

    def extract_transformation_executions(self):
        """Extract all TransformationExecution nodes"""
        for idx, node in self.nodes.items():
            if node.get('{http://www.omg.org/XMI}type') == 'mpm_trace:TransformationExecution':
                name = node.get('name')
                generates = node.get('generates')

                self.executions[idx] = {
                    'index': idx,
                    'name': name,
                    'generates': generates
                }

    def extract_transformations(self):
        """Extract all Transformation nodes and build I/O relationships"""
        # First pass: extract transformations and their output models
        for idx, node in self.nodes.items():
            if node.get('{http://www.omg.org/XMI}type') == 'mpm_trace:Transformation':
                name = node.get('name')
                exec_ref = node.get('exec')

                # Handle both old format (IN/OUT uppercase) and new format (Out capitalized)
                in_ref = node.get('IN')
                out_ref = node.get('OUT') or node.get('Out')  # Try both formats

                self.transformations[idx] = {
                    'index': idx,
                    'name': name,
                    'exec': exec_ref,
                    'IN': in_ref,
                    'OUT': out_ref
                }

        # Second pass: handle new format (In on Model, Out on Transformation)
        # Check if any Model has 'In' relation pointing to transformations
        for idx, node in self.nodes.items():
            if node.get('{http://www.omg.org/XMI}type') == 'mpm_trace:Model':
                in_ref = node.get('In')  # Model -> Transformation (input)
                if in_ref:
                    # This model is input to transformation(s)
                    trans_indices = self.resolve_references_list(in_ref)
                    for trans_idx in trans_indices:
                        if trans_idx in self.transformations:
                            # Add this model to transformation's inputs
                            if not self.transformations[trans_idx]['IN']:
                                self.transformations[trans_idx]['IN'] = f'//@nodes.{idx}'
                            else:
                                # Append to existing inputs
                                self.transformations[trans_idx]['IN'] += f' //@nodes.{idx}'

    def resolve_reference(self, ref_path: str) -> int:
        """Convert XPath reference to node index"""
        if not ref_path:
            return None
        parts = ref_path.split('.')
        if len(parts) >= 2:
            return int(parts[-1])
        return None

    def resolve_references_list(self, ref_path: str) -> List[int]:
        """Convert space-separated XPath references to node indices"""
        if not ref_path:
            return []
        refs = ref_path.split()
        return [self.resolve_reference(ref) for ref in refs]

    def build_global_trace(self) -> Dict:
        """Build the global trace by connecting local traces via I/O dependencies"""
        trace_to_transformation = {}

        exec_to_trace = {}
        for trace_idx, trace_data in self.trace_models.items():
            for exec_idx, exec_data in self.executions.items():
                generates_idx = self.resolve_reference(exec_data['generates'])
                if generates_idx == trace_idx:
                    exec_to_trace[exec_idx] = trace_idx
                    break

        for trace_idx in self.trace_models.keys():
            for exec_idx, exec_trace_idx in exec_to_trace.items():
                if exec_trace_idx == trace_idx:
                    for trans_idx, trans_data in self.transformations.items():
                        # Handle multiple executions per transformation
                        exec_ref_indices = self.resolve_references_list(trans_data['exec'])
                        if exec_idx in exec_ref_indices:
                            trace_to_transformation[trace_idx] = trans_idx
                            break

        # Collect all ancestor relationships first
        ancestor_pairs = set()
        for trace_idx, trace_data in self.trace_models.items():
            if trace_data.get('ancestor'):
                ancestor_idx = self.resolve_reference(trace_data['ancestor'])
                if ancestor_idx is not None:
                    ancestor_pairs.add((ancestor_idx, trace_idx))

        # Find latest version for each transformation
        trans_to_latest_trace = {}
        for trace_idx, trans_idx in trace_to_transformation.items():
            trace_data = self.trace_models[trace_idx]
            version = int(trace_data.get('version', 1))

            if trans_idx not in trans_to_latest_trace:
                trans_to_latest_trace[trans_idx] = (trace_idx, version)
            else:
                current_latest_idx, current_version = trans_to_latest_trace[trans_idx]
                if version > current_version:
                    trans_to_latest_trace[trans_idx] = (trace_idx, version)

        # Extract just the trace indices of latest versions
        latest_trace_indices = {trace_idx for trace_idx, _ in trans_to_latest_trace.values()}

        trace_dependencies = {}

        for trace_idx, trans_idx in trace_to_transformation.items():
            # Only create links FROM latest version traces
            if trace_idx not in latest_trace_indices:
                continue

            trans_data = self.transformations[trans_idx]
            output_models = self.resolve_references_list(trans_data['OUT'])

            for other_trace_idx, other_trans_idx in trace_to_transformation.items():
                if trace_idx == other_trace_idx:
                    continue

                # Skip if these traces have ancestor relationship
                if (trace_idx, other_trace_idx) in ancestor_pairs or (other_trace_idx, trace_idx) in ancestor_pairs:
                    continue

                other_trans_data = self.transformations[other_trans_idx]
                input_models = self.resolve_references_list(other_trans_data['IN'])

                if any(out_model in input_models for out_model in output_models):
                    if trace_idx not in trace_dependencies:
                        trace_dependencies[trace_idx] = []
                    trace_dependencies[trace_idx].append(other_trace_idx)

        return {
            'trace_to_transformation': trace_to_transformation,
            'trace_dependencies': trace_dependencies,
            'exec_to_trace': exec_to_trace
        }

    def calculate_node_levels(self, dependencies: Dict) -> Dict[int, int]:
        """Calculate the level of each node in the dependency graph using BFS"""
        # Find source nodes (no incoming edges)
        all_nodes = set(self.trace_models.keys())
        nodes_with_incoming = set()
        for targets in dependencies.values():
            nodes_with_incoming.update(targets)

        source_nodes = all_nodes - nodes_with_incoming

        # BFS to calculate levels
        levels = {}
        queue = [(node, 0) for node in source_nodes]

        while queue:
            node, level = queue.pop(0)

            # Update level if we found a longer path to this node
            if node not in levels or level > levels[node]:
                levels[node] = level

                # Add children to queue
                if node in dependencies:
                    for child in dependencies[node]:
                        queue.append((child, level + 1))

        return levels

    def generate_d3_html(self, global_trace: Dict, source_filename: str) -> str:
        """Generate interactive D3.js visualization with draggable nodes"""
        trace_to_trans = global_trace['trace_to_transformation']
        dependencies = global_trace['trace_dependencies']

        # Calculate node levels
        node_levels = self.calculate_node_levels(dependencies)

        # Build nodes data - MODELS, TRACES, AND ELEMENT TRACES
        nodes_data = []
        element_trace_counter = 0

        # Add Model nodes
        for model_idx, model_data in self.models.items():
            # Determine which level this model belongs to based on transformations
            level = 0

            # Check if this model is output of any transformation
            for trans_idx, trans_data in self.transformations.items():
                if trans_data['OUT']:
                    out_indices = self.resolve_references_list(trans_data['OUT'])
                    if model_idx in out_indices:
                        # Find the trace for this transformation and use its level + 1
                        # (output model is one level higher than the transformation trace)
                        for trace_idx, trans_id in trace_to_trans.items():
                            if trans_id == trans_idx:
                                level = node_levels.get(trace_idx, 0) + 1
                                break
                        break

            # Get metamodel name
            mm_name = 'Unknown'
            if model_data['conformsTo']:
                mm_idx = self.resolve_reference(model_data['conformsTo'])
                if mm_idx in self.nodes:
                    mm_name = self.nodes[mm_idx].get('name', 'Unknown')

            nodes_data.append({
                'id': f'model_{model_idx}',
                'name': model_data['name'],
                'type': 'model',
                'metamodel': mm_name,
                'level': level,
                'LevelOfAbstraction': model_data.get('LevelOfAbstraction', 'Unknown')
            })

        # Add TraceModel nodes
        for trace_idx, trace_data in self.trace_models.items():
            trans_idx = trace_to_trans.get(trace_idx)
            trans_name = self.transformations[trans_idx]['name'] if trans_idx else 'Unknown'

            # Get input and output models for this transformation
            input_models = []
            output_models = []
            trace_abstraction_level = 'Unknown'
            if trans_idx:
                trans_data = self.transformations[trans_idx]
                if trans_data['IN']:
                    in_indices = self.resolve_references_list(trans_data['IN'])
                    input_models = [self.nodes[i].get('name', 'Unknown') for i in in_indices if i in self.nodes]
                if trans_data['OUT']:
                    out_indices = self.resolve_references_list(trans_data['OUT'])
                    output_models = [self.nodes[i].get('name', 'Unknown') for i in out_indices if i in self.nodes]
                    # Determine trace abstraction level from output model
                    if out_indices:
                        first_out_idx = out_indices[0]
                        if first_out_idx in self.models:
                            trace_abstraction_level = self.models[first_out_idx].get('LevelOfAbstraction', 'Unknown')

            # Get node level
            level = node_levels.get(trace_idx, 0)

            # Count attribute-level traces
            attr_traces = 0
            element_traces = 0
            for rule in trace_data['traced_rules']:
                for link in rule['trace_links']:
                    if isinstance(link, dict):
                        if link.get('sourceAttribute') or link.get('targetAttribute'):
                            attr_traces += 1
                        else:
                            element_traces += 1
                    else:
                        element_traces += 1

            nodes_data.append({
                'id': f'trace_{trace_idx}',
                'name': trace_data['name'],
                'type': 'trace',
                'transformation': trans_name,
                'input_models': input_models,
                'output_models': output_models,
                'num_rules': len(trace_data['traced_rules']),
                'num_element_traces': element_traces,
                'num_attribute_traces': attr_traces,
                'traced_rules': trace_data['traced_rules'],
                'level': level,
                'version': trace_data.get('version', ''),
                'LevelOfAbstraction': trace_abstraction_level
            })

        # Add trace link nodes (separate from TraceModel)
        trace_link_nodes = []
        for trace_idx, trace_data in self.trace_models.items():
            trans_idx = trace_to_trans.get(trace_idx)
            level = node_levels.get(trace_idx, 0)

            # Determine abstraction level from output model
            trace_abstraction_level = 'Unknown'
            if trans_idx and trans_idx in self.transformations:
                trans_data = self.transformations[trans_idx]
                if trans_data['OUT']:
                    out_indices = self.resolve_references_list(trans_data['OUT'])
                    if out_indices and out_indices[0] in self.models:
                        trace_abstraction_level = self.models[out_indices[0]].get('LevelOfAbstraction', 'Unknown')

            # Extract trace links from traced rules
            for rule in trace_data['traced_rules']:
                for link in rule['trace_links']:
                    if isinstance(link, dict) and (link.get('sourceElementPath') or link.get('targetElementPath')):
                        trace_link_nodes.append({
                            'id': f'tracelink_{trace_idx}_{len(trace_link_nodes)}',
                            'name': link.get('name', 'Unnamed'),
                            'type': 'trace_link',
                            'sourceElementPath': link.get('sourceElementPath', ''),
                            'targetElementPath': link.get('targetElementPath', ''),
                            'linkType': link.get('linkType', ''),
                            'level': level,
                            'parent_trace_id': f'trace_{trace_idx}',
                            'LevelOfAbstraction': trace_abstraction_level
                        })

        nodes_data.extend(trace_link_nodes)

        # Build links data - connecting Models and Traces
        links_data = []

        # Create links: Input Model → Trace → Output Model
        for trace_idx, trans_idx in trace_to_trans.items():
            trans_data = self.transformations[trans_idx]

            # Get input models for this transformation
            if trans_data['IN']:
                in_indices = self.resolve_references_list(trans_data['IN'])
                for in_idx in in_indices:
                    # Link: Input Model → Trace
                    links_data.append({
                        'source': f'model_{in_idx}',
                        'target': f'trace_{trace_idx}',
                        'type': 'model_to_trace'
                    })

            # Get output models for this transformation
            if trans_data['OUT']:
                out_indices = self.resolve_references_list(trans_data['OUT'])
                for out_idx in out_indices:
                    # Link: Trace → Output Model
                    links_data.append({
                        'source': f'trace_{trace_idx}',
                        'target': f'model_{out_idx}',
                        'type': 'trace_to_model'
                    })

        # Create containment links from TraceModel to its trace links
        containment_links = []
        for link_node in trace_link_nodes:
            containment_links.append({
                'source': link_node['parent_trace_id'],
                'target': link_node['id'],
                'type': 'containment'
            })

        # Build ancestor links (version evolution within same transformation)
        ancestor_links = []
        for trace_idx, trace_data in self.trace_models.items():
            if trace_data.get('ancestor'):
                ancestor_idx = self.resolve_reference(trace_data['ancestor'])
                if ancestor_idx is not None:
                    ancestor_links.append({
                        'source': f'trace_{ancestor_idx}',
                        'target': f'trace_{trace_idx}',
                        'type': 'evolution'
                    })

        # Generate HTML with embedded D3.js
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Global Trace Visualization - D3.js</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        :root {{
            --bg-primary: #f5f5f5;
            --bg-secondary: white;
            --bg-graph: #fafafa;
            --text-primary: #333;
            --text-secondary: #666;
            --border-color: #ddd;
            --shadow: rgba(0,0,0,0.1);
            --link-color: #999;
            --link-hover: #333;
            --node-stroke: #fff;
            --tooltip-bg: rgba(0, 0, 0, 0.9);
            --tooltip-text: white;
        }}

        body.dark-mode {{
            --bg-primary: #1a1a1a;
            --bg-secondary: #2d2d2d;
            --bg-graph: #242424;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --border-color: #444;
            --shadow: rgba(0,0,0,0.5);
            --link-color: #888;
            --link-hover: #ccc;
            --node-stroke: #2d2d2d;
            --tooltip-bg: rgba(255, 255, 255, 0.95);
            --tooltip-text: #1a1a1a;
        }}

        body {{
            margin: 0;
            padding: 10px;
            font-family: Arial, sans-serif;
            background-color: var(--bg-primary);
            transition: background-color 0.3s ease;
            overflow: hidden;
            height: 100vh;
            box-sizing: border-box;
        }}

        #container {{
            background-color: var(--bg-secondary);
            border-radius: 8px;
            box-shadow: 0 2px 4px var(--shadow);
            padding: 10px;
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
            height: calc(100vh - 20px);
            display: flex;
            flex-direction: column;
            box-sizing: border-box;
        }}

        h1 {{
            text-align: center;
            color: var(--text-primary);
            margin-top: 0;
            transition: color 0.3s ease;
        }}

        .source-info {{
            text-align: center;
            color: var(--text-secondary);
            font-size: 14px;
            margin-bottom: 15px;
            font-style: italic;
            transition: color 0.3s ease;
        }}

        #graph {{
            border: 1px solid var(--border-color);
            border-radius: 4px;
            background-color: var(--bg-graph);
            transition: background-color 0.3s ease, border-color 0.3s ease;
            display: block;
            width: 100%;
            flex: 1;
            min-height: 0;
        }}

        .link {{
            stroke: var(--link-color);
            stroke-opacity: 0.6;
            stroke-width: 2px;
            fill: none;
            marker-end: url(#arrowhead);
            transition: stroke 0.3s ease;
        }}

        .link:hover {{
            stroke: var(--link-hover);
            stroke-opacity: 1;
            stroke-width: 3px;
        }}

        .node circle, .node rect, .node ellipse, .node path {{
            stroke: var(--node-stroke);
            stroke-width: 3px;
            cursor: move;
            transition: stroke 0.3s ease;
        }}

        .node:hover circle, .node:hover rect, .node:hover ellipse, .node:hover path {{
            stroke-width: 5px;
        }}

        .node rect {{
            rx: 5;
            ry: 5;
        }}

        .node text {{
            font-size: 12px;
            pointer-events: none;
            text-anchor: middle;
            font-weight: bold;
            fill: var(--text-primary);
            transition: fill 0.3s ease;
        }}

        .tooltip {{
            position: absolute;
            padding: 12px;
            background-color: var(--tooltip-bg);
            color: var(--tooltip-text);
            border-radius: 6px;
            pointer-events: none;
            font-size: 12px;
            opacity: 0;
            transition: opacity 0.3s, background-color 0.3s ease, color 0.3s ease;
            max-width: 400px;
            box-shadow: 0 4px 6px var(--shadow);
            z-index: 1000;
        }}

        .legend {{
            margin-top: 20px;
            text-align: center;
            font-size: 14px;
            color: var(--text-secondary);
            transition: color 0.3s ease;
        }}

        .legend-item {{
            display: inline-block;
            margin: 0 15px;
        }}

        .legend-color {{
            display: inline-block;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            margin-right: 5px;
            vertical-align: middle;
        }}

        .controls {{
            text-align: center;
            margin-bottom: 15px;
        }}

        button {{
            padding: 8px 16px;
            margin: 0 5px;
            border: none;
            border-radius: 4px;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            font-size: 14px;
            line-height: 1.4;
            min-height: 36px;
            vertical-align: middle;
            transition: background-color 0.3s ease, transform 0.1s ease;
        }}

        button:hover {{
            background-color: #45a049;
            transform: translateY(-1px);
        }}

        button:active {{
            transform: translateY(0);
        }}

        #darkModeToggle {{
            background-color: #666;
            padding: 8px 16px;
            font-size: 14px;
            line-height: 1.4;
            min-height: 36px;
        }}

        #darkModeToggle:hover {{
            background-color: #555;
        }}

        body.dark-mode #darkModeToggle {{
            background-color: #f0f0f0;
            color: #1a1a1a;
        }}

        body.dark-mode #darkModeToggle:hover {{
            background-color: #e0e0e0;
        }}
    </style>
</head>
<body>
    <div id="container">
        <h1>Global Trace Visualization</h1>
        <div class="source-info">Source: {source_filename}</div>
        <div class="controls">
            <button onclick="resetPositions()">Reset Positions</button>
            <button onclick="centerGraph()">Center View</button>
            <button id="darkModeToggle" onclick="toggleDarkMode()">🌙 Dark Mode</button>
        </div>
        <svg id="graph"></svg>
        <div class="legend" id="legend">
            <!-- Legend will be dynamically generated -->
        </div>
    </div>
    <div class="tooltip" id="tooltip"></div>

    <script>
        // Data
        const nodes = {json.dumps(nodes_data, indent=8)};
        const links = {json.dumps(links_data, indent=8)};
        const containmentLinks = {json.dumps(containment_links, indent=8)};
        const ancestorLinks = {json.dumps(ancestor_links, indent=8)};

        // Combine all links for simulation
        const allLinks = [...links, ...containmentLinks, ...ancestorLinks];

        // Color scale for LevelOfAbstraction - distinct colors for PIM, PSM, Code
        const colorScale = d3.scaleOrdinal()
            .domain(['PIM', 'PSM', 'Code', 'Unknown'])
            .range(['#9C27B0', '#4CAF50', '#FFC107', '#666']);  // Purple for PIM, Green for PSM, Yellow for Code

        // Generate compact legend for LevelOfAbstraction
        const legend = d3.select("#legend");
        const abstractionLevels = ['PIM', 'PSM', 'Code'];

        // Compact color legend (inline)
        const colorLegend = legend.append("div").style("margin-bottom", "5px");
        abstractionLevels.forEach((level, i) => {{
            if (i > 0) colorLegend.append("span").html(" | ");
            colorLegend.append("span")
                .attr("class", "legend-color")
                .style("background-color", colorScale(level))
                .style("display", "inline-block")
                .style("width", "10px")
                .style("height", "10px")
                .style("margin-right", "3px");
            colorLegend.append("span")
                .style("font-size", "10px")
                .text(level);
        }});

        // Compact shape legend
        legend.append("div").attr("class", "legend-item").style("font-size", "9px")
            .html('⬭ Model | ◆ Trace | ⬬ Link');

        // Compact link legend
        legend.append("div").attr("class", "legend-item").style("font-size", "9px")
            .html('━ Flow | <span style="color: #4CAF50">┅</span> Contains');


        // Setup - Landscape orientation (full viewport, left-to-right flow)
        const graphEl = document.getElementById("graph");
        const width = graphEl.clientWidth || window.innerWidth - 40;
        const height = graphEl.clientHeight || window.innerHeight - 150;

        const svg = d3.select("#graph")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", `0 0 ${{width}} ${{height}}`)
            .attr("preserveAspectRatio", "xMidYMid meet");

        // Add arrowhead marker (smaller)
        svg.append("defs").append("marker")
            .attr("id", "arrowhead")
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 25)  // Position at edge of smaller ellipse
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
            .attr("fill", "#999");

        // Create zoom behavior
        const zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on("zoom", (event) => {{
                g.attr("transform", event.transform);
            }});

        svg.call(zoom);

        const g = svg.append("g");

        // Calculate level positions - arrange LEFT TO RIGHT (landscape)
        const levels = [...new Set(nodes.map(d => d.level))].sort((a, b) => a - b);
        const levelWidth = width / (levels.length + 1);
        const levelPositions = {{}};
        levels.forEach((level, i) => {{
            levelPositions[level] = (i + 1) * levelWidth;
        }});

        // Force simulation - landscape orientation (horizontal)
        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(allLinks).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("x", d3.forceX(d => levelPositions[d.level]).strength(0.5))  // X axis for levels (horizontal)
            .force("y", d3.forceY(height / 2).strength(0.1))  // Y axis for spreading (vertical)
            .force("collision", d3.forceCollide().radius(d => {{
                if (d.type === 'trace') return 45;
                if (d.type === 'trace_link') return 55;
                return 40;
            }}));

        // Dependency links (solid) with arrows
        const link = g.append("g")
            .selectAll("path")
            .data(links)
            .join("path")
            .attr("class", "link")
            .attr("marker-end", "url(#arrowhead)");

        // Containment links (dashed green) with arrows
        const containmentLink = g.append("g")
            .selectAll("path")
            .data(containmentLinks)
            .join("path")
            .attr("class", "link")
            .attr("marker-end", "url(#arrowhead)")
            .style("stroke", "#4CAF50")
            .style("stroke-dasharray", "3,3")
            .style("stroke-width", "1.5px");

        // Ancestor links (dotted blue)
        const ancestorLink = g.append("g")
            .selectAll("path")
            .data(ancestorLinks)
            .join("path")
            .attr("class", "link")
            .style("stroke", "#0066cc")
            .style("stroke-dasharray", "5,5")
            .style("stroke-width", "2px");

        // Nodes
        const node = g.append("g")
            .selectAll("g")
            .data(nodes)
            .join("g")
            .attr("class", "node")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        // Render different shapes based on type (SMALLER SIZES)
        node.each(function(d) {{
            const nodeGroup = d3.select(this);
            if (d.type === 'model') {{
                // Models as ellipses (SMALLER: 25x15 instead of 40x25)
                nodeGroup.append("ellipse")
                    .attr("rx", 25)
                    .attr("ry", 15)
                    .style("fill", d => colorScale(d.LevelOfAbstraction || 'Unknown'));
            }} else if (d.type === 'trace') {{
                // Trace models as diamonds (SMALLER: 22 instead of 35)
                const size = 22;

                nodeGroup.append("rect")
                    .attr("width", size)
                    .attr("height", size)
                    .attr("x", -size/2)
                    .attr("y", -size/2)
                    .attr("transform", "rotate(45)")
                    .style("fill", "#2196F3")  // Always blue for TraceModels
                    .style("stroke", "var(--text-primary)")
                    .style("stroke-width", 1);
            }} else if (d.type === 'trace_link') {{
                // Trace links as rounded rectangles (SMALLER)
                const fontSize = 8;
                const padding = 10;
                const boxHeight = 20;

                // Calculate width based on text length (smaller font)
                const textWidth = d.name.length * 5;
                const boxWidth = Math.max(80, textWidth + padding * 2);  // Min 80px

                nodeGroup.append("rect")
                    .attr("width", boxWidth)
                    .attr("height", boxHeight)
                    .attr("x", -boxWidth/2)
                    .attr("y", -boxHeight/2)
                    .style("fill", d => colorScale(d.LevelOfAbstraction || 'Unknown'))
                    .style("fill-opacity", 0.8)
                    .style("rx", 5)
                    .style("ry", 5)
                    .style("stroke", "var(--text-primary)")
                    .style("stroke-width", 0.5)
                    .style("stroke-opacity", 0.3);

                // Show full name (smaller font)
                nodeGroup.append("text")
                    .attr("y", 4)
                    .attr("text-anchor", "middle")
                    .style("font-size", fontSize + "px")
                    .style("fill", "var(--text-primary)")
                    .style("pointer-events", "none")
                    .text(d.name);
            }}
        }});

        // Add labels below nodes (SMALLER FONTS)
        node.filter(d => d.type === 'model').append("text")
            .attr("dy", 22)
            .attr("text-anchor", "middle")
            .style("font-size", "9px")
            .style("fill", "var(--text-primary)")
            .text(d => d.name);

        node.filter(d => d.type === 'trace').append("text")
            .attr("dy", 22)
            .attr("text-anchor", "middle")
            .style("font-size", "8px")
            .style("font-weight", "bold")
            .style("fill", "var(--text-primary)")
            .text(d => d.name.replace(/_v\d+$/, ''));

        // Tooltip
        const tooltip = d3.select("#tooltip");

        node.on("mouseenter", (event, d) => {{
            let tooltipHTML = '';

            if (d.type === 'model') {{
                // Model tooltip
                tooltipHTML = `
                    <strong>${{d.name}}</strong><br/>
                    <div style="margin-top: 3px;">Type: Model</div>
                    <div>Abstraction: ${{d.LevelOfAbstraction}}</div>
                    <div>Metamodel: ${{d.metamodel}}</div>
                `;
            }} else if (d.type === 'trace_link') {{
                // Trace link tooltip
                tooltipHTML = `
                    <strong>Trace Link: ${{d.name}}</strong><br/>
                    <div style="margin-top: 5px; font-size: 11px;">
                        <div style="color: #6c6;">From: ${{d.sourceElementPath}}</div>
                        <div style="color: #6cc; margin-top: 3px;">To: ${{d.targetElementPath}}</div>
                    </div>
                `;
            }} else {{
                // Trace model tooltip - simplified, no version or level
                const displayName = d.name.replace(/_v\d+$/, '');
                tooltipHTML = `
                    <strong>${{displayName}}</strong><br/>
                    <div style="margin-top: 3px;">Type: TraceModel</div>
                    <div>Transformation: ${{d.transformation}}</div>
                `;
            }}

            tooltip
                .style("opacity", 1)
                .html(tooltipHTML)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY + 10) + "px");  // Position slightly below the cursor
        }})
        .on("mouseleave", () => {{
            tooltip.style("opacity", 0);
        }});

        // Simulation tick
        simulation.on("tick", () => {{
            // Update all link types
            link.attr("d", d => {{
                return `M${{d.source.x}},${{d.source.y}} L${{d.target.x}},${{d.target.y}}`;
            }});

            containmentLink.attr("d", d => {{
                return `M${{d.source.x}},${{d.source.y}} L${{d.target.x}},${{d.target.y}}`;
            }});

            ancestorLink.attr("d", d => {{
                return `M${{d.source.x}},${{d.source.y}} L${{d.target.x}},${{d.target.y}}`;
            }});

            node.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        }});

        // Drag functions
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}

        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}

        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            // Keep node fixed at dragged position
            // Uncomment next two lines to allow node to float after drag
            // d.fx = null;
            // d.fy = null;
        }}

        // Reset positions
        function resetPositions() {{
            nodes.forEach(d => {{
                d.fx = null;
                d.fy = null;
            }});
            simulation.alpha(1).restart();
        }}

        // Center view
        function centerGraph() {{
            svg.transition().duration(750).call(
                zoom.transform,
                d3.zoomIdentity.translate(width / 2, height / 2).scale(1).translate(-width / 2, -height / 2)
            );
        }}

        // Dark mode toggle
        function toggleDarkMode() {{
            const body = document.body;
            const button = document.getElementById('darkModeToggle');
            const isDarkMode = body.classList.toggle('dark-mode');

            // Update button text
            button.textContent = isDarkMode ? '☀️ Light Mode' : '🌙 Dark Mode';

            // Save preference to localStorage
            localStorage.setItem('darkMode', isDarkMode ? 'enabled' : 'disabled');

            // Update arrowhead marker color
            updateArrowheadColor(isDarkMode);
        }}

        // Update arrowhead marker to match theme
        function updateArrowheadColor(isDarkMode) {{
            const arrowColor = isDarkMode ? '#888' : '#999';
            d3.select('#arrowhead path').attr('fill', arrowColor);
        }}

        // Handle window resize
        window.addEventListener('resize', () => {{
            const newWidth = graphEl.clientWidth;
            const newHeight = graphEl.clientHeight;
            svg.attr("width", newWidth).attr("height", newHeight)
               .attr("viewBox", `0 0 ${{newWidth}} ${{newHeight}}`);
        }});

        // Load dark mode preference on page load
        window.addEventListener('DOMContentLoaded', () => {{
            const darkMode = localStorage.getItem('darkMode');
            const button = document.getElementById('darkModeToggle');

            if (darkMode === 'enabled') {{
                document.body.classList.add('dark-mode');
                button.textContent = '☀️ Light Mode';
                updateArrowheadColor(true);
            }}
        }});
    </script>
</body>
</html>
"""
        return html

    def generate(self, source_filename: str) -> str:
        """Main generation method"""
        self.parse_nodes()
        self.extract_models()  # Extract Model nodes
        self.extract_trace_models()
        self.extract_transformation_executions()
        self.extract_transformations()

        # Debug: print transformation I/O relationships
        print("\n=== DEBUG: Transformation I/O Relationships ===")
        for trans_idx, trans_data in self.transformations.items():
            print(f"\nTransformation [{trans_idx}]: {trans_data['name']}")
            print(f"  IN: {trans_data['IN']}")
            print(f"  OUT: {trans_data['OUT']}")
            if trans_data['IN']:
                in_models = self.resolve_references_list(trans_data['IN'])
                print(f"  Input Models: {[self.nodes[i].get('name') for i in in_models]}")
            if trans_data['OUT']:
                out_models = self.resolve_references_list(trans_data['OUT'])
                print(f"  Output Models: {[self.nodes[i].get('name') for i in out_models]}")

        global_trace = self.build_global_trace()
        return self.generate_d3_html(global_trace, source_filename)


def main():
    import os

    parser = argparse.ArgumentParser(
        description='Generate Global Trace D3.js visualization from CPS Traceability Framework XML files'
    )
    parser.add_argument(
        'example_xml',
        nargs='?',
        default='src_artifacts/MPM_trace_example.xml',
        help='Path to the example XML file (default: src_artifacts/MPM_trace_example.xml)'
    )
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output HTML file path (default: output_g_trace/<xml_basename>.html)'
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    output_dir = 'output_g_trace'
    os.makedirs(output_dir, exist_ok=True)

    # If no output specified, generate default name from input XML
    if args.output is None:
        xml_basename = os.path.splitext(os.path.basename(args.example_xml))[0]
        args.output = os.path.join(output_dir, f'{xml_basename}.html')
    # If output specified without directory, put it in output_g_trace
    elif not os.path.dirname(args.output):
        args.output = os.path.join(output_dir, args.output)

    generator = GlobalTraceGeneratorD3(args.example_xml)
    result = generator.generate(args.example_xml)

    with open(args.output, 'w') as f:
        f.write(result)

    print(f"D3.js Global trace visualization saved to: {args.output}")
    print(f"Source XML: {args.example_xml}")


if __name__ == '__main__':
    main()
