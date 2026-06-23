# Cryptographic Triangles — Website

Static marketing/download site for the Cryptographic Triangles Qt Wallet, served at <https://cryptographic-triangles.org>.

## Files

- `index.html` — single-page site
- `styles.css` — all styling (dark by default, respects `prefers-color-scheme`)

No build step. No JS frameworks. Vanilla HTML/CSS + ~25 lines of JS for the copy-to-clipboard button on the SHA-256 hash.

## Local preview

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy to cPanel

This site is designed to deploy to the existing Liquid Web cPanel that already handles DNS for `cryptographic-triangles.org` (server `cloud01.elitehost.net`, IP `69.167.170.22`).

### Option A — cPanel Git Version Control (recommended)

1. In cPanel: **Files → Git Version Control → Create**
2. Clone URL: `https://github.com/SamiAhmed7777/tri-website.git`
3. Document root: `/home/samihost/cryptographic-triangles.org/`
4. After first clone, in cPanel: **Manage → Pull or Deploy → Update from Remote**

### Option B — Manual rsync

```bash
rsync -avz --delete -e 'ssh -p 22022' \
  ./ samihost@cloud01.elitehost.net:/home/samihost/cryptographic-triangles.org/
```

### DNS

DNS for `cryptographic-triangles.org` already resolves to `69.167.170.22` (verified). cPanel will serve the site on the configured document root.

## Updating content

Edit `index.html` / `styles.css`, commit, push. If Git Version Control is configured in cPanel, the next pull picks it up automatically.

## License

Content released under the MIT License, matching the [triangles_v5 wallet repository](https://github.com/SamiAhmed7777/triangles_v5/blob/master/LICENSE).
