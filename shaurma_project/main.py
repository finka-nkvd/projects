from auth import AuthWindow
from frontend import Frontend
from backend import Backend


def main():
    backend = Backend()

    def start_app():
        app = Frontend(backend)
        app.run()

    auth_window = AuthWindow(start_app)
    auth_window.run()


if __name__ == "__main__":
    main()
