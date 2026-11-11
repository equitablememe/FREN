# FREN mobile notebook

The mobile notebook provides a browser interface for recording an investigation or working through a question. Start a notebook, add notes with sources or tests where relevant, and track next steps.

Run this from the repository root to serve the app locally.

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory mobile
```

Open `http://127.0.0.1:8765` in a browser. The app serves static files and uses the browser's local storage. The offline shell uses a service worker on HTTPS or localhost. Browser and device support for installation varies.

Use **Your data → Download backup** to export your notebooks. Import that backup in another browser or at a new site address to carry your notes over. **Export brief** creates a separate investigation record for an individual notebook. The current interface records your entries and does not call an AI model.

The app assets match the FREN mobile preview source. The repository's Apache-2.0 license applies.
