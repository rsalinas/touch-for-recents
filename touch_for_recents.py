#!/usr/bin/env python3
import argparse
import pathlib
import sys

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, GLib
except Exception as e:
    print("Error: PyGObject/GTK3 is missing.", file=sys.stderr)
    print("On Ubuntu/Debian try:", file=sys.stderr)
    print("  sudo apt install python3-gi gir1.2-gtk-3.0", file=sys.stderr)
    print(f"Detail: {e}", file=sys.stderr)
    sys.exit(2)


def add_to_recents(filename: str) -> bool:
    path = pathlib.Path(filename).expanduser()

    if not path.exists():
        print(f"Does not exist: {filename}", file=sys.stderr)
        return False

    if not path.is_file():
        print(f"Not a regular file: {filename}", file=sys.stderr)
        return False

    ok = Gtk.RecentManager.get_default().add_item(path.resolve().as_uri())

    if ok:
        print(f"Added to Recents: {path}")
    else:
        print(f"Could not add: {path}", file=sys.stderr)

    return ok


def flush_recents() -> None:
    # Gtk.RecentManager writes the .xbel on a timer, not synchronously: wait
    # (deterministically) for the file to change on disk before exiting, with
    # a fallback so we never hang.
    xbel = pathlib.Path(GLib.get_user_data_dir()) / "recently-used.xbel"
    before = xbel.stat().st_mtime_ns if xbel.exists() else 0
    loop = GLib.MainLoop()

    def written():
        if xbel.exists() and xbel.stat().st_mtime_ns != before:
            loop.quit()
            return False
        return True

    GLib.timeout_add(20, written)
    GLib.timeout_add(3000, loop.quit)  # fallback
    loop.run()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add one or more files to the GTK/GNOME 'Recents' list."
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="Files to mark as recent"
    )

    args = parser.parse_args()

    results = [add_to_recents(f) for f in args.files]
    if any(results):
        flush_recents()

    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
