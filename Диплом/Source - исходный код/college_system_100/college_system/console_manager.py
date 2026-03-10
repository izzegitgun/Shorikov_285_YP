import os
import sys
import time
import webbrowser
from subprocess import Popen, CREATE_NEW_CONSOLE


BANNER = r"""
╔══════════════════════════════════════════════╗
║       КПСУ  – консоль управления             ║
╠══════════════════════════════════════════════╣
║  1. Запустить сервер                         ║
║  2. Остановить сервер                        ║
║  3. Открыть сайт в браузере                  ║
║  4. Выход                                    ║
╚══════════════════════════════════════════════╝
"""

SERVER_URL = "http://127.0.0.1:8000/"
_server_process: Popen | None = None


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_status() -> None:
    global _server_process
    print()
    if _server_process and _server_process.poll() is None:
        print("  Статус сервера: запущен ✅")
        print(f"  Адрес: {SERVER_URL}")
    else:
        print("  Статус сервера: остановлен ⛔")
    print()


def start_server() -> None:
    """Запуск Django runserver в отдельном консольном окне."""
    global _server_process

    if _server_process and _server_process.poll() is None:
        print("\nСервер уже запущен.")
        time.sleep(1.5)
        return

    manage_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = [sys.executable, "manage.py", "runserver", "0.0.0.0:8000"]

    try:
        env = os.environ.copy()
        # Для локальной разработки используем SQLite, чтобы не зависеть от PostgreSQL
        env["USE_SQLITE_FOR_DEV"] = "True"
        _server_process = Popen(
            cmd,
            cwd=manage_dir,
            env=env,
            creationflags=CREATE_NEW_CONSOLE if os.name == "nt" else 0,
        )
        print("\nСервер запускается...")
    except Exception as exc:  # noqa: BLE001
        print(f"\nОшибка при запуске сервера: {exc}")
    time.sleep(1.8)


def stop_server() -> None:
    """Попытаться мягко остановить сервер, запущенный из этого меню."""
    global _server_process

    if not _server_process or _server_process.poll() is not None:
        print("\nСервер не запущен из этого менеджера.")
        time.sleep(1.5)
        return

    _server_process.terminate()
    print("\nОстанавливаю сервер...")
    try:
        _server_process.wait(timeout=5)
    except Exception:  # noqa: BLE001
        _server_process.kill()
        print("Сервер был принудительно завершён.")
    _server_process = None
    time.sleep(1.8)


def open_site() -> None:
    print(f"\nОткрываю сайт: {SERVER_URL}")
    webbrowser.open(SERVER_URL)
    time.sleep(1.5)


def main() -> None:
    while True:
        clear_screen()
        print(BANNER)
        print_status()
        choice = input("  Выберите пункт меню (1–4): ").strip()

        if choice == "1":
            start_server()
        elif choice == "2":
            stop_server()
        elif choice == "3":
            open_site()
        elif choice == "4":
            clear_screen()
            print("До встречи в КПСУ 2025 👋")
            time.sleep(1.2)
            break
        else:
            print("\nНеизвестная команда. Введите 1, 2, 3 или 4.")
            time.sleep(1.5)


if __name__ == "__main__":
    main()

