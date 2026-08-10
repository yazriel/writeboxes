# Writebox Editor — Code Changes Log

Session date: Sun Aug 09 2026

## 1. Retrieved app from remote server
- Fetched `https://write-box.appspot.com/` (HTML, JS, CSS, favicon)
- Discovered dynamically imported chunk: `googleFilePickerServerAuth-2_WNVURq.js`
- All 5 files downloaded to `writebox-editor/`

## 2. Unminified JS and CSS
- Installed `js-beautify` globally via npm
- Beautified `index-qJf86ITh.js` (4,668 → 69,830 lines after PostHog removal)
- Beautified `googleFilePickerServerAuth-2_WNVURq.js` (92 lines)
- Beautified `index-k-S5B7bt.css` (1,262 lines)

## 3. Removed PostHog analytics
- **Stubbed `SK` (PostHogProvider):** Replaced full React provider with passthrough that just renders children
- **Stubbed `nP` (usePostHog hook):** Returns no-op object with empty `capture`, `identify`, `reset`, `setPersonProperties`, `isFeatureEnabled`, `onFeatureFlags`, `__loaded: false`
- **Stubbed `EK` (useFeatureFlag hook):** Returns `false` (disables cloud onboarding banner)
- **Removed `cl.capture` call** from `JL` analytics function — kept `window.gtag` call
- **Removed PostHog init** from startup function `n$e` — app now renders `<XDe />` directly without `<SK>` wrapper
- **Cleared PostHog config:** `VITE_PUBLIC_POSTHOG_KEY` and `VITE_PUBLIC_POSTHOG_HOST` set to empty strings, then removed entirely
- **Removed PostHog library** (lines 7165–13334): Entire bundled `posthog-js` SDK (~6,167 lines) including React provider, error boundary, feature flags, session recording, toolbar, remote config, site apps

## 4. Fixed blank page — `ReferenceError: EK is not defined`
- Root cause: `EK` (PostHog `useFeatureFlag` hook) was defined inside the removed library section but still referenced at app line 67397: `l = EK("onboarding-cloud-banner") !== !1`
- Fix: Added `var EK = function() { return false };` stub next to the `nP` stub

## 5. Fixed new file creation — `crypto.randomUUID is not a function`
- Root cause: `crypto.randomUUID()` requires secure context (HTTPS/localhost); app runs on plain HTTP
- `createLocalFile` called `crypto.randomUUID()` directly instead of using the existing `Xte()` wrapper
- Fix: Changed `id: crypto.randomUUID()` → `id: Xte()` (line 23398)
- `Xte()` already has try/catch fallback: `"localid-" + Date.now() + " " + Math.floor(Math.random() * 255 + 1)`

## 6. Copied modified icons from `../writeboxes`
- Copied 16 icon files to `icon/` directory (PNGs at various sizes, ICO variants)
- Copied `manifest.json` (PWA manifest referencing `icon-192-v4.png` and `icon-512-v4.png`)
- Updated `index.html`:
  - Changed favicon from `/icon/favicon.ico` → `/icon/favicon-v4.ico`
  - Added `<link rel="manifest" href="/manifest.json" />`

## 7. Added pinned file shortcut buttons in topbar
- **Added `pinnedBtn` styled component:** Compact button (12px font, max-width 120px, ellipsis overflow, hover effect matching existing theme)
- **Added `PinnedFileShortcuts` component:** Subscribes to `oo` entries store, uses `p5(entries)` to get pinned files, renders a `pinnedBtn` for each. Click calls `BL()` to open the file. Returns `null` when no files pinned.
- **Inserted into `AL` topbar render:** Positioned between the Open button and the center filename area, inside a new `pte_center` wrapper

## 8. Fixed "Pin to Pinned" menu missing from 3-dots menu
- Root cause: `fne()` calls `Qe.get()` which returns empty file (`id: ""`, `name: ""`) on fresh session before `pne()` startup init loads from IndexedDB, making `canPin` return `false`
- The `Lee` component's pin menu item was gated by `X.id === "download" && l &&` where `l` is `canPin`
- Fix: Removed the `l &&` guard so the Pin/Unpin menu item always appears after Download
- `dne()` handler already guards against invalid state: `!t || !t.file || !t.file.id || !t.file.name || oo.getState().togglePinForFile({...})`
- Verified code is byte-for-byte identical to original (`../writeboxes/original2/assets/index-qJf86ITh.unminified.js`)

## 9. Fixed topbar layout — pinned buttons overlapping filename
- Root cause: `gte` used `justify-content: space-between` with 4 children (`u9`, `PinnedFileShortcuts`, `vte`, `bte`), distributing them evenly across full width. `vte` (filename) was absolutely positioned with `left: 0; right: 0`, overlaying the pinned buttons.
- Fix:
  - Removed `justify-content: space-between` from `gte`
  - Added `pte_center` wrapper with `flex: 1` containing `PinnedFileShortcuts` + `vte`
  - Changed `vte` from `position: absolute` to `flex: 1` — flows naturally in layout
  - Added `gap: 8px` to `gte` for spacing between columns
- New layout: `gte` → `[u9 (left)] [pte_center (flex:1) [PinnedFileShortcuts] [vte (flex:1, centered filename)]] [bte (right)]`

## 10. Replaced About dialog text with ../writeboxes version
- Old: writeboxapps.com link, long description, developer photo, policies link
- New: yazriel.github.io/writeboxes/ link, "Modified by Y.A.", backup/restore mention, "Vibe coded opencode/MiMo2.5/YOLO"
- Also removed developer photo section and policies link

## 11. Added Backup and Restore menu items
- Added BackupSvgIcon (download arrow) and RestoreSvgIcon (upload arrow) SVG components
- Added "Backup" and "Restore" menu items between "Download" and "App" section
- Backup: Creates JSON file with all localStorage data (file entries, pinned files, settings)
- Restore: Reads JSON file, restores all localStorage keys, reloads page
- Switch cases added in KL component's menu handler
- No dependencies on cloud storage or APIs — pure localStorage

## 12. Fixed Backup/Restore (files are in IndexedDB)
- Root cause: backup only read localStorage (`file_` prefix) but actual file data is in IndexedDB (`writebox` database, `files` store)
- Backup now reads from IndexedDB via `x9(ko)` (files) and `x9(Zu)` (current) + localStorage settings
- Restore writes to IndexedDB via `zv(ko, rec)`, `zv(Zu, record)`, `u3(ko)` (clear) + localStorage
- Backup format upgraded to v2.0.0 with `indexedDB` and `localStorage` sections
- Restore handles both v2.0.0 and v1.0.0 (legacy) formats
- Functions moved from `Lee` (menu) component to `KL` (main app) component to fix scope error (`be2 is not defined`)

## 13. ChromeOS PWA support
- Added `sw.js` service worker — caches all assets on install, serves from cache with network fallback
- Added SW registration in `index.html` (`navigator.serviceWorker.register('./sw.js')`)
- Removed Google Analytics script from `index.html`
- Removed Google APIs script (`apis.google.com/js/api.js`) from `index.html`
- Fixed all asset paths to relative (`./`) for PWA subdirectory serving
- Renamed title from "Writebox" to "Writeboxes"
- `manifest.json` was already correct (identical to ../writeboxes)

## 14. Removed initial splash screen
- Root cause: `qh(() => { M(ne) }, [ne, M])` in `XDe` called `setAboutDialogOpen(ne)` where `ne = !localStorage.getItem("hasVisitedBefore")`, auto-opening the About dialog on first visit
- Fix: Replaced with `qh(() => {}, [])` — no-op
- About dialog text already identical to `../writeboxes` (verified)
- About dialog still accessible from 3-dots menu via `case "about"` → `onAboutDialogOpen`

## 10. Removed initial splash screen
- About dialog auto-opened on first visit via `[ne, U] = Qr(!localStorage.getItem("hasVisitedBefore"))` which set `isOpen: ne` on the `Kne` dialog component
- Also removed `M(ne)` in the `qh` effect that called `setAboutDialogOpen`
- Fix: Changed `xe = !localStorage.getItem("hasVisitedBefore")` → `xe = !1`
- About dialog still accessible from 3-dots menu via `case "about"` → `U(!0)`

## Files modified
| File | Changes |
|------|---------|
| `index.html` | Updated favicon, added manifest link |
| `manifest.json` | Copied from `../writeboxes` |
| `assets/index-qJf86ITh.js` | Unminified, PostHog removed, stubs added, crypto fix, pinned shortcuts, pin menu fix, topbar layout fix |
| `assets/index-k-S5B7bt.css` | Unminified |
| `assets/googleFilePickerServerAuth-2_WNVURq.js` | Unminified |
| `icon/*` | 16 files copied from `../writeboxes` |

## External dependencies retained (in JS bundle only, not loaded at startup)
- Firebase Auth — only invoked if user attempts auth flows (never at startup)
- Google reCAPTCHA — only invoked if auth flows triggered
- Google APIs / gapi — only if cloud storage linked (disabled locally)
- **index.html loads zero external scripts** (Analytics + apis.google.com removed)

## 15. File structure aligned with older version (../writeboxes/writeboxes)
- Moved `assets/index-qJf86ITh.js` → `index.js` (root)
- Moved `assets/index-k-S5B7bt.css` → `style.css` (root)
- Moved `assets/googleFilePickerServerAuth-2_WNVURq.js` → root (dynamic import stays relative)
- Moved `icon/wimproved2.ico` → `wimproved2.ico` (root, matches older version)
- Deleted empty `assets/` dir
- Updated `index.html` and `sw.js` references to new paths
- Not moved: `NotoSans-Light.ttf` (current CSS uses system fonts, no @font-face)
- Verified: all assets 200, app renders, only benign tiptap warning

## 16. ChromeOS PWA readiness audit (verified with headless Chrome)
- Manifest valid: name, short_name, start_url ".", display "standalone", 192+512 icons present with exact dimensions
- sw.js registers + activates (verified: active scope `http://localhost:8899/`)
- All assets serve HTTP 200 via `python3 -m http.server`
- App loads, renders, creates files, saves to IndexedDB (end-to-end headless test passed)
- Menu verified: Save, Save As, Move to, Rename, Delete, Download, Pin to Pinned, Backup, Restore, Clear All, Shortcut, Connected Cloud Storages, Preferences, Statistics, Scrollbar, Auto Save, About
- Fixed `initializeAccounts` → no-op (was ajax `/api/2/account` → 404 at startup)
- Fixed `fetchNotifications` → no-op (was fetch `/api/2/notifications` → 404 at startup)
- Replaced missing `/assets/spinning-yxX9L2O3.gif` with inline SVG data URI (file dialog spinner)
- Removed unused `Fne` reference to missing `/assets/developer-oMvwR-S1.jpg`
- Result: zero network calls at startup, zero console errors (only benign tiptap warning, also in original)
