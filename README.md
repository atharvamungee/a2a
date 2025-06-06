# A2A Multi-Agent PoC

This repo contains a small proof of concept showing how to build multiple
A2A agents that communicate with each other. It defines:

- `Time Agent` – returns the current Pacific time.
- `Location Agent` – returns a random place in NYC.
- `Info Agent` – combines the time and location tools.
- `Orchestrator Agent` – routes user queries to the other agents using the A2A
  protocol and combines their responses.

A minimal client is provided to test the setup.

## Running the demo

Install dependencies (ideally inside a virtual environment):

```bash
pip install -r requirements.txt
```

Start the agents in separate terminals:

```bash
python agents/time_agent.py
python agents/location_agent.py
python agents/info_agent.py
python agents/orchestrator_agent.py
```

Query the orchestrator:

```bash
python client.py "Can you tell me the time and the location?"
```

The orchestrator fetches results from the three agents via the A2A
protocol and prints the combined response.
