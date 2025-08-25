# SAP

A simplified SAP-like system demonstrating a layered architecture.

## Structure

- `application/` – core business modules (`gl`, `ap`, `ar`, `inventory`).
- `data/` – SQLite wrapper and SQL migration scripts.
- `integration/` – internal REST-like interfaces implemented with a Flask blueprint.
- `presentation/` – Flask application exposing the integration layer.

## Usage

1. Install requirements: `pip install flask`.
2. Run the presentation layer: `python -m presentation.app`.
3. Interact with modules via HTTP endpoints, e.g., `GET /api/gl`.

This project is intentionally minimal and for demonstration purposes only.
