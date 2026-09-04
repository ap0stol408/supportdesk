# Architecture

One process, Python standard library, SQLite on disk.
`server` translates HTTP to `web.Application`; `service` implements ticket
operations; `database` owns connections and schema; `auth` owns process-local
sessions; `templates` renders HTML. Runtime data stays under `.local/`.

This is a synthetic security evaluation service, not a production template.
The history simulates three fictional contributors, feature work and hotfixes.
