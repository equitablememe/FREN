# FREN mobile notebook

The mobile notebook provides a browser interface for recording an investigation or working through a question. Start a notebook, add notes with sources or tests where relevant, and track next steps.

**Public FREN Mobile:** https://equitablememe.github.io/FREN/ (GitHub Pages; no account, model connection or cloud sync).

The **Return to Resolucent review ↩** link opens https://www.resolucent.com/#fren-handoff in the same browser tab, avoiding unreliable popups on some browsers. Export a notebook with **Export brief** first; then select that exported file on Resolucent. Returning does not send notes automatically.

**Important migration note:** browsers isolate local storage by site address. Notes saved at localhost, another FREN address, or another device will not appear automatically at the public Pages URL. Open the old location, choose **Your data → Download backup**, and import that backup from **Your data → Bring your work back** at the public address. Keep backups of work that matters.

Run this from the repository root to serve the app locally.

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory mobile
```

Open `http://127.0.0.1:8765` in a browser. The app serves static files and uses the browser's local storage. The offline shell uses a service worker on HTTPS or localhost. Browser and device support for installation varies.

Use **Your data → Download backup** to export your notebooks. Import that backup in another browser or at a new site address to carry your notes over. **Export brief** creates a separate investigation record for an individual notebook. The current interface records your entries and does not call an AI model.

The app assets match the FREN mobile preview source. The repository's Apache-2.0 license applies.
