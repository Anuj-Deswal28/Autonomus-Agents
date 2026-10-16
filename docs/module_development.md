# Adding a P-7 Module

1. Create `modules/<module_name>/`.
2. Add `module.py` implementing `P7Module`.
3. Add a module-specific `config.yaml`.
4. Put domain behavior in `behaviors/`, system instances in `agents/`, and external integrations in `adapters/`.
5. Use shared P-7 models and interfaces; do not import another module's internal implementation.
6. Add unit and integration tests.
7. Register the module in a scenario YAML file.
