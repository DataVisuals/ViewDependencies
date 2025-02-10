

# Documentation for Dependency Visualization Script

## Overview

This script generates an interactive network graph representing the dependencies of Python packages installed in your environment. It uses `pipdeptree` to obtain the dependency information, `NetworkX` for graph manipulation, and `streamlit_agraph` for visualization.

## Dependencies

Ensure you have the following libraries installed:
- `streamlit`
- `streamlit-agraph`
- `networkx`
- `pipdeptree`
- `json`

You can install them using pip:
```sh
pip install streamlit streamlit-agraph networkx pipdeptree json
```

## Script Explanation

### Imports
```python
import subprocess
import re
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config, ConfigBuilder
from pprint import pprint
import json
import networkx as nx
```
These imports provide the necessary functions and classes for creating and visualizing the dependency graph.

### Streamlit Configuration
```python
st.set_page_config(layout="wide")
```
This sets the layout of the Streamlit app to a wide format, providing more space for the visualization.

### Graph Creation Function
```python
G = nx.DiGraph()
def deps2graph(packages):
    # Mapping to keep track of unique node IDs
    node_id_map = {}
    nodes = []
    edges = []

    # Generate nodes and map each package to a unique integer ID
    for idx, package in enumerate(packages):
        package_key = package['package']['key']
        package_name = package['package']['package_name']
        node_id_map[package_key] = idx  # Map package key to integer ID
        G.add_node(package_name)
        nodes.append(Node(id=package_name,
                          label=package_name,
                          size=30))
        
    # Generate edges using the integer IDs
    for package in packages:
        source_id = node_id_map[package['package']['key']]
        for dependency in package.get('dependencies', []):
            dep_key = dependency['key']
            if dep_key in node_id_map:
                target_id = node_id_map[dep_key]
                G.add_edge(package['package']['key'], dependency['key'])
                edges.append(Edge(source=package['package']['key'], target=dependency['key']))

    for node in nodes:
        degrees = G.degree(node.id)
        size = (degrees * 5) + 10
        node.size = size
        if degrees < 1:
            node.color = "red"
                    
    return nodes, edges
```
This function creates the network graph from the dependency data obtained from `pipdeptree`. It generates nodes and edges, maps packages to unique IDs, and adjusts node sizes and colors based on their degrees.

### Dependency Parsing Function
```python
def get_dependencies():
    result = subprocess.run(['pipdeptree', '--warn', 'silence', '--json'], stdout=subprocess.PIPE, text=True)
    output = result.stdout
    dependency_tree = json.loads(output)
    return dependency_tree
```
This function runs the `pipdeptree` command to obtain the dependency tree in JSON format and returns it as a Python dictionary.

### Main Script Logic
```python
dependency_tree = get_dependencies()
config = None

# Get the graph
nodes, edges = deps2graph(dependency_tree)

# 1. Build the config (with sidebar to play with options).
try:
    config = Config(from_json="config.json")
except:
    config_builder = ConfigBuilder()
    config = config_builder.build()

# 2. If you're done, save the config to a file.
config.save("config.json")

# 3. Simple reload from json file (you can bump the builder at this point.)
config = Config(from_json="config.json")

if not config:
    config = Config(width=1300,
                    height=800,
                    directed=True, 
                    physics=True, 
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightColor="#F7A7A6",
                    collapsible=True,
                    node={'color': 'lightblue', 'size': 15},
                    link={'color': 'black', 'width': 2}
                    )
```
This section handles the configuration of the visualization. It attempts to load the configuration from a JSON file. If it fails, it builds a new configuration and saves it to a file.

### Visualization
```python
return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)

if return_value:    
    md = ("**Selected nodes**: %s" % return_value) + "<br>" + \
        ("**Is Needed By**: %s" % ",".join([x for x in G.predecessors(return_value)]) + "<br>") + \
        ("**Needs**: %s" % ",".join([x for x in G.successors(return_value)])) 
    st.markdown(md, unsafe_allow_html=True)
```
This final section generates the interactive graph using `agraph` and displays selected nodes' details.

## How to Use

1. **Run the Script**:
   - Ensure you have all the required dependencies installed.
   - Save the script as `view_deps.py`.
   - Run the script using Streamlit:
   ```sh
   streamlit run view_deps.py
   ```

2. **Interact with the Graph**:
   - The Streamlit app will open in your default web browser.
   - Explore the interactive network graph, zoom, and pan to view dependencies.
   - Click on nodes to see more details about their dependencies and what depends on them.
