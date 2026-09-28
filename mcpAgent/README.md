# MCP agent project

Run these commands from `mcpAgent/`:

```bash
uv sync
source .venv/bin/activate
uv run ragagent
```

Run a practice file with `python ../python/first.py` after activation.
Add dependencies with `uv add package-name`.

`src/ragagent/` contains the application package. `pyproject.toml` and
`uv.lock` define its dependencies; `.env` holds local configuration.
