"""Run the local technical Flask scaffold."""

from todo_board_ssc.backend.app import create_app
from todo_board_ssc.backend.runtime import DEFAULT_HOST, DEFAULT_PORT


def main() -> None:
    """Run the local application using approved loopback defaults."""
    create_app().run(host=DEFAULT_HOST, port=DEFAULT_PORT)


if __name__ == "__main__":
    main()
