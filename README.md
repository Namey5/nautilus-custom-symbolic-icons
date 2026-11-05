# Custom Symbolic Icons — Nautilus Python Extension
Nautilus extension to add custom symbolic icons to folder bookmarks.
<img width="1373" height="790" alt="Screenshot From 2026-11-05 15-31-44" src="https://github.com/user-attachments/assets/1af728e7-0a8b-4c1d-8f80-75545a3d415e" />

## Installation
Copy `custom-symbolic-icons.py` to the `nautilus-python` extensions folder:
```bash
cp custom-symbolic-icons.py ~/.local/share/nautilus-python/extensions/
```
Then restart Nautilus:
```bash
nautilus -q
```

## Usage
There is currently no UI for overriding icons directly in Nautilus, but you can add it to the `Gio` metadata attribute `custom-symbolic-icon`
(which is more or less how regular icon overrides work behind the scenes):
```bash
# gio set [FOLDER PATH] metadata::custom-symbolic-icon [ICON NAME]
gio set ~/Games metadata::custom-symbolic-icon applications-games-symbolic
```
If you do this a bunch for the same folder you might need to restart Nautilus to see the updates.
