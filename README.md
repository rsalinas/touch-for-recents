# touch-for-recents

Add files to the GTK/GNOME **Recents** list (the one Nautilus shows) from the
command line, *without opening them*.

No native CLI does exactly this: `gio open` / `xdg-open` register a file in
Recents only as a side effect of opening it with its default app. This script
just registers it. Handy for surfacing in the GUI whatever you produced on the
console.

## Install

Needs PyGObject (GTK 3). On Ubuntu/Debian, either install the system package:

```sh
sudo apt install python3-gi gir1.2-gtk-3.0
```

or build it in a venv (needs cairo + gobject-introspection dev libs):

```sh
sudo apt install libcairo2-dev libgirepository1.0-dev gir1.2-gtk-3.0
pip install -r requirements.txt
```

## Usage

```sh
./touch_for_recents.py FILE [FILE ...]
```

```sh
./touch_for_recents.py report.pdf ~/Downloads/data.csv
```

Then open *Files* (Nautilus) → **Recents**. Requires GNOME's file history to be
on (*Settings → Privacy → File History*).

Exit code is `0` only if every file was added, `1` otherwise.

## Notes

`Gtk.RecentManager` flushes `recently-used.xbel` on a timer, not synchronously,
so the script waits for the file to actually hit disk before exiting (with a
3 s fallback). That's why a registered file reliably shows up.

## Test

```sh
python3 test_touch_for_recents.py
```
