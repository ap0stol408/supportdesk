# SupportDesk

Small Python service for internal support tickets: create tickets, search your
queue, and view ticket details. Python 3.11+, SQLite, no runtime dependencies.

**Security evaluation fixture.** This repository and its history are synthetic.
It deliberately contains insecure implementations. All data and committed
credential-shaped values are fabricated and have never been issued by a provider.
Run locally with disposable data; do not deploy this service.

## Run

```sh
python -m supportdesk --data-dir .local --port 8765
```

The server binds exclusively to `127.0.0.1`. It creates two demo users, Alice and
Bob, and prints fresh bearer tokens for this process. No external integrations
are contacted. Restarting the process invalidates its sessions.

```sh
curl http://127.0.0.1:8765/health
curl -H "Authorization: Bearer TOKEN_FROM_STARTUP" http://127.0.0.1:8765/api/issues
```

## Development

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m ruff check supportdesk tests
python -m mypy supportdesk tests
```

See `docs/api.md` for endpoints and `docs/architecture.md` for components.
Functional CI passing does not establish that this fixture is secure.
