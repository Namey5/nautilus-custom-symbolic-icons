# Custom Symbolic Icons — Nautilus Python Extension
Nautilus/GNOME Files extension to add custom symbolic icons to folder bookmarks.
<img width="1373" height="790" alt="Screenshot From 2026-11-05 15-31-44" src="https://github.com/user-attachments/assets/1af728e7-0a8b-4c1d-8f80-75545a3d415e" />

## Installation
Requires [nautilus-python](https://gitlab.gnome.org/GNOME/nautilus-python) (available in various package managers).

Copy `custom-symbolic-icons.py` to the `nautilus-python` extensions folder:
```bash
cp custom-symbolic-icons.py ~/.local/share/nautilus-python/extensions/
```
Then restart Nautilus:
```bash
nautilus -q
```

## Usage
A file context action has been added to override the icon name, although annoyingly this won't show when right-clicking a bookmark - 
instead you'll need to navigate to the actual folder in Nautilus and set it from there.

<img width="331" height="558" alt="image" src="https://github.com/user-attachments/assets/4acde577-1b55-491e-bfec-22767ea23189" />
<img width="268" height="140" alt="image" src="https://github.com/user-attachments/assets/8a414e4e-d9bc-4379-bb0b-68e9a2ace2b2" />

Alternatively, you can add it to the metadata attribute `custom-symbolic-icon` directly via `Gio`
(which is more or less how regular icon overrides work behind the scenes):
```bash
# gio set [FOLDER PATH] metadata::custom-symbolic-icon [ICON NAME]
gio set ~/Games metadata::custom-symbolic-icon applications-games-symbolic
```

## Known Issues
- Small delay when first opening Nautilus for icons to update.
- Setting an icon might not update on other open windows.
- Clearing an icon won't update until you open a new window.
