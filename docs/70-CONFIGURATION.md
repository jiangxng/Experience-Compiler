# Configuration

`config/ec.example.toml` is the starting template. Production secrets belong in a secret manager, never committed TOML. Configuration precedence should evolve to: immutable defaults < environment config < deployment overrides < secrets < tenant policy, with every effective config snapshot hashable for reproducibility.
