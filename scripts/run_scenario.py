"""Scenario runner entry point (implementation pending)."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a P-7 scenario")
    parser.add_argument("--config", required=True, help="Path to scenario YAML")
    parser.parse_args()
    raise SystemExit(
        "Scenario runner is a scaffold. Implement config loading and runtime startup first."
    )


if __name__ == "__main__":
    main()
