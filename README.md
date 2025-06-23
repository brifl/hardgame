## Project Overview

This repository hosts **HardGame**, a lightweight, Flask-based multiplayer RPG platform featuring live chat logs, turn-based gameplay, and extensible world state management. It leverages **Flask-SQLAlchemy** for relational data modeling and persistence ([flask-sqlalchemy.readthedocs.io](https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/?utm_source=chatgpt.com)), **htmx** for progressive enhancement of real-time interactions ([htmx.org](https://htmx.org/docs/?utm_source=chatgpt.com)), and **Server-Sent Events** (SSE) to push new log entries to all connected players without manual refresh ([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events?utm_source=chatgpt.com)). Sessions and players are identified by short, unguessable codes generated with Python’s **secrets** module ([docs.python.org](https://docs.python.org/3/library/secrets.html?utm_source=chatgpt.com)), while all data lives in a SQLite database for zero-config setup ([sqlite.org](https://www.sqlite.org/docs.html?utm_source=chatgpt.com)). Future extensions include LLM-driven DM responses via the OpenAI ChatCompletion API ([platform.openai.com](https://platform.openai.com/docs/api-reference/chat?utm_source=chatgpt.com)), JSON-Patch updates for fine-grained entity diffs ([datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc6902?utm_source=chatgpt.com)), and themable UI skins for different RPG styles.

## Features

* **Session & Player Codes:** 6-character, easy-to-share codes with ambiguity-free characters ([docs.python.org](https://docs.python.org/3/library/secrets.html?utm_source=chatgpt.com)).
* **Real-Time Log Streaming:** SSE endpoint streams each new `LogEntry` bubble directly into the browser via htmx ([mathspp.com](https://mathspp.com/blog/streaming-data-from-flask-to-htmx-using-server-side-events?utm_source=chatgpt.com)).
* **Turn Endpoint:** Atomic “player action + DM placeholder” loop under a single `/turn` API call.
* **State Persistence:** SQLite backend managed through Flask-SQLAlchemy; no external DB required ([digitalocean.com](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application?utm_source=chatgpt.com)).
* **Extensible Entity Updates:** Optional JSON-Patch diffs returned by turn calls for updating character stats, inventory, and location state ([datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc6902?utm_source=chatgpt.com)).
* **Modular Design:** Blueprints separate sessions, players, and API routes for maintainability.

## Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/hardgame.git
   cd hardgame
   ```
2. **Create & activate a virtualenv**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app**

   ```bash
   flask run
   ```

   Visit `http://localhost:5000/` to start a new session.

## Usage

* **Create a session:** Navigate to `/session/new` (root redirects here).
* **Add yourself as a player:** Enter a unique name under `/session/<code>/player/new`.
* **Play turns:** Type actions and hit **Send**; observe live DM bubbles appear.
* **Multi-player:** Open the same session code in multiple browsers or devices for real-time play.

## Development

* **Blueprints:**

  * `routes/sessions.py` – session creation
  * `routes/players.py`  – player onboarding & game view
  * `routes/api.py`      – logs, players, turn, and stream endpoints
* **Models:** Defined in `models.py` (Session, Player, LogEntry, Location, etc.).
* **Utilities:** Code generation in `utils.py` using `secrets` ([docs.python.org](https://docs.python.org/3/library/secrets.html?utm_source=chatgpt.com)).
* **Templates & Static:** Jinja2 for HTML partials; CSS under `static/style.css`.

## Roadmap

1. **Suggested-Action Buttons & Dice UI**
2. **JSON-Patch State Diffs**
3. **Location & Map Persistence**
4. **LLM-Driven DM Narration**
5. **OOC Chat & WebSockets**
6. **Themed UI Skins**

Each milestone ships with a clear “Definition of Done” ensuring full test coverage and documentation before proceeding.

## Contributing

1. Fork the repo and create a feature branch (`git checkout -b feature/YourFeature`)
2. Commit your changes with clear messages
3. Run tests and ensure existing functionality passes
4. Submit a pull request for review

Please adhere to the [Code of Conduct](./CODE_OF_CONDUCT.md).

## License

This project is released under the **MIT License**, a short and permissive license requiring preservation of copyright notices ([choosealicense.com](https://choosealicense.com/licenses/mit/?utm_source=chatgpt.com)).

```text
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy...
```
