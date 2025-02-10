
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
