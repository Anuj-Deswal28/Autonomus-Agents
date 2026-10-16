# P-7 Architecture

## Dependency direction

Domain modules depend on stable contracts in `core/interfaces` and shared models in `core/models`.
The core must not import domain-specific modules. The runtime wires services and module instances
together. Transport implementations are interchangeable behind a transport interface.

## Key boundaries

- `core/environment`: simulated world state
- `core/environment/registry.py`: known nodes/capabilities registry
- `runtime`: application lifecycle and service wiring
- `transport`: delivery mechanism
- `coordination`: algorithms/protocols for coordinating independent systems
- `results`: generated run artifacts, not application logic
