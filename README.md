# ADF-Python Sample Agents
## Overview
This is a sample agent for [ADF-Python(Agent Development Framework for Python)](https://github.com/adf-python/adf-core-python)

## Requirement
- Python (3.12 or higher)

## Installation
```bash
cd adf-sample-agent-python
pip install -r requirements.txt
```

## Usage
```bash
cd adf-sample-agent-python
python main.py -a {Number of AmbulanceTeam Agents} -f {Number of FireBrigade Agents} -p {Number of PoliceForce Agents}

# Example
# python main.py -a 10 -f 10 -p 10

# More information about command line arguments
# python main.py -help
```