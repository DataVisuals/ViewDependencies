import subprocess
import re
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config, ConfigBuilder
from pprint import pprint
import json

import subprocess
import re

st.set_page_config(layout="wide")
def get_dependency_graph(packages):
    """
    Generates a dependency graph using zero-based integer IDs for nodes and edges.

    Args:
        packages (list): List of packages with dependencies.

    Returns:
        tuple: A tuple containing two lists - nodes and edges.
    """
    # Mapping to keep track of unique node IDs
    node_id_map = {}
    nodes = []
    edges = []

    # Generate nodes and map each package to a unique integer ID
    for idx, package in enumerate(packages):
        package_key = package['package']['key']
        package_name = package['package']['package_name']
        node_id_map[package_key] = idx  # Map package key to integer ID
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
                edges.append(Edge(source=package['package']['key'], target=dependency['key']))

    return nodes, edges


# Parse JSON output for nodes and edges
result = subprocess.run(['pipdeptree', '--warn', 'silence', '--json'], stdout=subprocess.PIPE, text=True)
output = result.stdout
dependency_tree = json.loads(output)



# Get the graph
nodes, edges = get_dependency_graph(dependency_tree)

# 1. Build the config (with sidebar to play with options) .
config_builder = ConfigBuilder(nodes,edges=edges)
config = config_builder.build()

# 2. If your done, save the config to a file.
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
                    
                    # **kwargs
                    )



return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)

st.markdown("**Selected nodes**: %s" % return_value)