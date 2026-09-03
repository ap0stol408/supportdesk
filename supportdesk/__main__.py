import argparse
from pathlib import Path

from supportdesk.auth import SessionRegistry
from supportdesk.config import Settings
from supportdesk.database import initialize
from supportdesk.server import make_server
from supportdesk.web import Application


def main() -> None:
    parser = argparse.ArgumentParser(description="Local SupportDesk evaluation fixture")
    parser.add_argument("--data-dir", type=Path, default=Path(".local"))
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    settings = Settings(args.data_dir / "tickets.sqlite3", args.data_dir / "attachments")
    initialize(settings.database)
    settings.attachments.mkdir(parents=True, exist_ok=True)
    sessions = SessionRegistry()
    print("Synthetic local fixture. Do not deploy.", flush=True)
    print(f"Alice bearer token: {sessions.issue(1)}", flush=True)
    print(f"Bob bearer token: {sessions.issue(2)}", flush=True)
    with make_server(Application(settings, sessions), args.port) as server:
        print(f"Listening on http://127.0.0.1:{server.server_port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
