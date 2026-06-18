# Writeboxes — Local Copy

A fully self-contained local copy of [Writebox](https://write-box.appspot.com/), the
distraction-free text editor. All assets are downloaded and served statically — no
server backend, no external API calls, no analytics. Renamed to **Writeboxes** to
distinguish from the original and avoid conflicts when installed as a PWA.

The JS bundle has been unminified with Prettier (`print-width: 120`, `no-semi`,
`single-quote`) for easier editing. The original was a single 1.37 MB line;
it now spans ~64,000 lines across 2.1 MB.

## Project Structure

```
writeboxes/
├── index.html                          # Entry point
├── index.js                            # Vite-bundled app (React 18, ProseMirror, jQuery)
├── style.css                           # Stylesheet (ProseMirror, markdown-body, fonts)
├── NotoSans-Light.ttf                  # Noto Sans Light font
├── spec.md                             # This file
├── manifest.json                       # PWA manifest (app name, icons, display mode)
├── sw.js                               # Service worker (caches assets for offline/install)
├── generate-icons.py                   # Script to regenerate placeholder icons
└── icon/
    ├── favicon.ico                     # Site favicon
    ├── icon-192.png                    # PWA icon 192×192 (placeholder)
    └── icon-512.png                    # PWA icon 512×512 (placeholder)
```

## Serve

```bash
python3 -m http.server 8080
```

No build step, no npm install.

## How the App Works

- **Editor**: ProseMirror (rich-text / plain-text modes) with a markdown preview
- **File storage**: `localStorage["pool"]` holds a JSON array of `{ wbFileInfo, contents }`
- **Current file**: `localStorage["wbFileInfo"]` tracks the active file's metadata
- **File manager**: Singleton `Gn` (class `JV`) reads/writes the `"pool"` array
- **Settings**: Zustand store persisted to individual `localStorage` keys
- **Auth**: Firebase config uses placeholder credentials (fails silently)
- **Cloud storage**: Dropbox, Google Drive, OneDrive, Box — disabled locally (buttons show error messages)

## PWA (Installable App)

Writeboxes is a Progressive Web App. It can be installed on ChromeOS (and other
platforms) directly from the browser without code signing, SSL certificates, or
the Chrome Web Store.

**Requirements:**
- Served over HTTPS or localhost (`python3 -m http.server` satisfies this)
- Opening `index.html` via `file://` does **not** support PWA installation

**How to install:**
1. Start the local server: `python3 -m http.server 8080`
2. Open `http://localhost:8080` in Chrome/ChromeOS
3. Click the install prompt in the address bar (or menu → "Install Writeboxes")
4. The app appears in the launcher/shelf and runs in its own window

**Files:**
- `manifest.json` — App metadata. Uses `id: "/writeboxes"` to avoid conflicting with the original Writebox
- `sw.js` — Service worker. Caches all static assets on install, serves from cache with network fallback
- `icon/icon-192.png`, `icon/icon-512.png` — Placeholder icons. Regenerate with `python3 generate-icons.py`

## Changes

- **PostHog removed** — Replaced PostHogProvider with a null context to fix startup crash
- **Toolbar always visible** — Removed jQuery fade-on-edit and hover-show/hide animations
- **File shortcut buttons** — Each local file gets a button in the toolbar (left side) that opens instantly on click. Updates on page load, file switch, and when the Open dialog opens/closes (no polling)
- **Startup API calls removed** — Disabled 404-ing calls to `/api/2/notifications`, `/api/2/auth/user`, and `/api/2/account` at startup
- **Save button removed** — Removed from toolbar since cloud sync is disabled
- **Backup & Restore** — Added to the overflow menu (⋮): Backup downloads all files as JSON; Restore imports a JSON file
- **Page load errors fixed** — Fixed duplicate `const` identifier errors and trailing-comma syntax errors
- **Save as removed** — Removed from overflow menu
- **Cloud auto-save disabled** — `shouldAutoSave()` returns `false`; auto-save effect is a no-op
- **Backup reads localStorage directly** — Reads `pool`, `wbFileInfo`, and `contents` keys to ensure the currently open file is always included
- **Statistics removed** — Removed from Settings panel, keyboard shortcut (Ctrl+Shift+S), and shortcut dialog; statistics bar always hidden
- **Auto Save removed** — Removed toggle from Settings panel; removed `toggleAutoSave` and `toggleShowStatistics` store functions; removed from default settings
- **File shortcut buttons fixed** — Buttons now resolve file index at click time by matching file ID against the current pool. Previously buttons stored a static array index which became stale whenever `getFile()` spliced the opened file out of the pool. Buttons could open wrong files, point out of bounds, or disappear. Each button now carries a `fileId`; on click it re-reads the pool via `__getFileList`, finds the matching ID, and passes the current index to `__openFile`.
- **Renamed to Writeboxes** — Title, About dialog, and PWA manifest all use "Writeboxes" to distinguish from the original Writebox and avoid conflicts when both are installed
- **PWA support** — Added `manifest.json`, `sw.js` (service worker), and icon generation script. App is installable on ChromeOS via localhost without code signing or SSL

### File Button Details

The pool (`localStorage["pool"]`) is a mutable array that changes on every open (`splice`) and save (`push`). The original button code captured the index at render time:

```
render: index = 3
click:  openFile(3)   ← pool may now be shorter/wrong
```

The fix defers index resolution to click time:

```
render: fileId = "localid-1718..."
click:  getFiles() → find index where fileId matches → openFile(currentIndex)
```

This is safe because:
- `__getFileList` is only used by the inline script (no other callers)
- `__openFile` still receives an integer index (no downstream changes)
- Deleted files gracefully result in no action (index resolves to -1)
- File IDs are unique (`localid-{timestamp} {random}`)

## Serving Options

| Method | URL | PWA Install | Notes |
|---|---|---|---|
| `python3 -m http.server 8080` | `http://localhost:8080` | Via Chrome menu only | Address bar shows "Not Secure"; install icon hidden behind warning |
| `python3 -m http.server` + self-signed cert | `https://localhost:8443` | Full (address bar icon) | Requires `openssl` one-time cert generation |
| GitHub Pages | `https://<user>.github.io/<repo>/` | Full (address bar icon) | HTTPS by default; push repo and enable Pages |
| `file://` (double-click index.html) | `file:///...` | No | Service worker does not register over file:// |

**Recommended:** GitHub Pages for hassle-free HTTPS and install prompt. For local use, the Chrome menu → "Install Writeboxes" works without any certificate setup.

## Recent Changes Recap

- Renamed app to **Writeboxes** (avoids conflict with original Writebox)
- Removed cloud features: PostHog, auto-save, save button, save-as, statistics, startup API calls
- Added **file shortcut buttons** in toolbar (each local file gets a clickable button; index resolved at click time by file ID)
- Added **Backup & Restore** to overflow menu (JSON export/import; reads localStorage directly)
- Added **PWA support** (`manifest.json`, `sw.js`, icons) for installation on ChromeOS and other platforms
