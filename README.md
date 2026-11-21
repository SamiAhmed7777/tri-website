# Cryptographic Triangles — Website

Static marketing/download site for the Cryptographic Triangles clients, served at
<https://cryptographic-triangles.org>.

## Files

- `index.html` — single-page site (both clients: tri7 + classic Qt wallet)
- `styles.css` — all styling (dark by default, respects `prefers-color-scheme`)
- `assets/fonts/` — self-hosted Sora + IBM Plex woff2 (latin subsets; see OFL-NOTICE.txt).
  The site makes zero third-party requests: no font CDN, no analytics.
- `llms.txt` — plain-text summary for AI assistants; kept consistent with index.html
- `releases.xml` — RSS feed, generated from BOTH release repos by `generate_rss.py`
  (triangles_v5 + tri7; runs in GitHub Actions every 6 hours)
- `validate_site.py` — pre-deploy checks: HTML balance, WCAG contrast (>=4.5:1),
  AI-slop pattern absence, copy-honesty greps, SHA-256/size cross-check against the
  GitHub release API, link liveness, llms.txt consistency
- `generate_rss.py`, `.github/workflows/rss.yml` — RSS generation + schedule
- `build_inline.py`, `build_with_contact.py` — legacy build helpers (index.html is
  maintained directly; the build scripts are kept for reference)

## Local preview + validation

```bash
python3 -m http.server 8000
python3 validate_site.py   # must print OVERALL: GREEN before any deploy
```

## Deploy

Host: `samihost` (`194.163.161.162`), docroot
`/home/cryptographic-triangles.org/public_html/` (www-data-owned). The live docroot
and this repo must be kept in sync: scp the changed files, `chown www-data:www-data`,
verify with curl + md5sum. Always sync live -> repo before editing if drift is suspected.

The block explorer subdomain (`blocks.cryptographic-triangles.org`) is served from
DNS2 (Caddy -> SvelteKit on 127.0.0.1:3052) and needs its DNS A record + Caddy site
block to stay intact; the site's live block-height counter reads the explorer's
`__data.json` (CORS-allowlisted for this origin in the explorer's hooks.server.ts).

## Updating content

Edit `index.html` / `styles.css`, run `validate_site.py`, commit, push, deploy.
Copy-honesty rules (judge-enforced, keep for every round): routing is per peer
address (.onion to Tor, .b32.i2p to I2P); no absolute privacy claims; installer
SHA-256 is an integrity check, not provenance; package-channel pills must match the
live registries; tri7 speaks clearnet in addition to Tor/I2P (the classic wallet is
Tor/I2P-only by default); both clients are MIT-licensed (classic `COPYING`, tri7
`LICENSE`).

## License

Content released under the MIT License, matching the
[triangles_v5 COPYING](https://github.com/SamiAhmed7777/triangles_v5/blob/master/COPYING)
and the [tri7 LICENSE](https://github.com/SamiAhmed7777/tri7/blob/master/LICENSE).
