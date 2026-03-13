"""Development entrypoint for the HBnB Part 3 application."""

import os

from app import create_app

app = create_app(os.getenv("FLASK_ENV", "default"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
