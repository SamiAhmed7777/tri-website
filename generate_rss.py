#!/usr/bin/env python3
"""Generate releases.xml (RSS 2.0) from the GitHub releases of both Triangles clients:
the classic C++/Qt wallet (triangles_v5) and the Rust client (tri7)."""
import json
import urllib.request
import datetime
import hashlib
import re
from packaging.version import Version, InvalidVersion
from xml.sax.saxutils import escape

SOURCES = [
    ("classic-wallet", "SamiAhmed7777/triangles_v5"),
    ("tri7", "SamiAhmed7777/tri7"),
]
SITE_URL = "https://cryptographic-triangles.org"
SITE_TITLE = "Cryptographic Triangles — Release Notes"
SITE_DESC = ("Official release notes for the Cryptographic Triangles clients (classic C++/Qt "
             "wallet and the tri7 Rust client). Subscribe to get notified when new versions ship.")

def fetch_releases(repo):
    api = f"https://api.github.com/repos/{repo}/releases?per_page=100"
    req = urllib.request.Request(api, headers={"User-Agent": "tri-website-rss-generator"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def md_to_html(md):
    """Minimal markdown → HTML for release notes (preserves paragraphs, lists, code blocks, links)."""
    if not md:
        return ""
    md = escape(md)
    # Code blocks (``` ... ```)
    md = re.sub(r'```(\w*)\n(.*?)\n```', r'<pre><code class="language-\1">\2</code></pre>', md, flags=re.DOTALL)
    # Inline code
    md = re.sub(r'`([^`]+)`', r'<code>\1</code>', md)
    # Links [text](url)
    md = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', md)
    # Headers (## ###)
    md = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', md, flags=re.MULTILINE)
    md = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', md, flags=re.MULTILINE)
    md = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', md, flags=re.MULTILINE)
    md = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', md, flags=re.MULTILINE)
    # Bold / italic
    md = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', md)
    md = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', md)
    # List items
    md = re.sub(r'^\s*[-*]\s+(.+)$', r'<li>\1</li>', md, flags=re.MULTILINE)
    md = re.sub(r'(<li>.*?</li>(?:\s*<li>.*?</li>)*)', r'<ul>\1</ul>', md, flags=re.DOTALL)
    # Paragraphs (double newline).
    # If a paragraph contains a block-level element (<ul>, <ol>, <pre>),
    # split it: the block element becomes its own block, and any inline
    # content before/after is wrapped in its own <p>.
    parts = re.split(r'\n\s*\n', md)
    out = []
    block_re = re.compile(r'(<ul\b.*?</ul>|<ol\b.*?</ol>|<pre\b.*?</pre>)', re.DOTALL)
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<h') or p.startswith('<ul') or p.startswith('<pre'):
            out.append(p)
            continue
        segments = block_re.split(p)
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            if block_re.fullmatch(seg):
                out.append(seg)
            else:
                seg = seg.replace('\n', '<br>')
                out.append(f'<p>{seg}</p>')
    return '\n'.join(out)

def _dedup_html_paragraphs(html):
    """Remove consecutive duplicate <p>...</p> blocks in rendered HTML.

    GitHub Actions sometimes writes the '**Full Changelog**:' line twice in
    auto-generated release bodies, sometimes with slightly different URLs.
    First occurrence wins.
    """
    if not html:
        return html
    pattern = re.compile(r'<p[^>]*>.*?</p>', re.DOTALL)
    parts = pattern.split(html)
    matches = pattern.findall(html)
    out = []
    last = None
    for pre, block in zip(parts, matches):
        normalized = re.sub(r'\s+', ' ', block).strip()
        if normalized == last:
            continue  # skip duplicate
        out.append(pre)
        out.append(block)
        last = normalized
    out.append(parts[-1])
    return ''.join(out)


def _semantic_compare_urls(releases, repo):
    """Build a map of tag -> correct prev-tag compare URL, per repository."""
    tag_versions = []
    for r in releases:
        tag = r.get('tag_name', '') or ''
        try:
            v = Version(tag.lstrip('v'))
            tag_versions.append((v, tag))
        except InvalidVersion:
            continue
    tag_versions.sort(key=lambda x: x[0])
    urls = {}
    for i, (_, tag) in enumerate(tag_versions):
        if i == 0:
            urls[tag] = f"https://github.com/{repo}/compare/{tag}"
        else:
            prev_tag = tag_versions[i - 1][1]
            urls[tag] = f"https://github.com/{repo}/compare/{prev_tag}...{tag}"
    return urls


def _installer_asset(r, tag, repo):
    """Pick the Windows setup.exe asset if present; else fall back to the release page."""
    for a in r.get('assets', []) or []:
        name = a.get('name', '')
        if name.endswith('setup.exe'):
            return a.get('browser_download_url'), name
    return f"https://github.com/{repo}/releases/tag/{tag}", None


def build_rss(releases_with_repo):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    compare_cache = {}
    for label, repo, r in releases_with_repo:
        if (repo, 'urls') not in compare_cache:
            compare_cache[(repo, 'urls')] = _semantic_compare_urls(
                [x for (l, rp, x) in releases_with_repo if rp == repo], repo)
        compare_urls = compare_cache[(repo, 'urls')]
        tag = r.get('tag_name', '')
        name = r.get('name') or tag
        body = r.get('body') or ''
        if tag in compare_urls:
            body = re.sub(
                r'\*\*Full Changelog\*\*:\s*https?://[^\s)]+',
                f'**Full Changelog**: {compare_urls[tag]}',
                body,
            )
        html_url = r.get('html_url', '')
        published = r.get('published_at') or r.get('created_at', '')
        try:
            dt = datetime.datetime.fromisoformat(published.replace('Z', '+00:00'))
            rss_date = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
            sort_key = dt
        except Exception:
            rss_date = now
            sort_key = datetime.datetime.now(datetime.timezone.utc)
        guid = f"tri-release-{label}-{tag}-{hashlib.md5(html_url.encode()).hexdigest()[:8]}"
        desc = md_to_html(body)
        if not desc.strip():
            desc = f'<p>Release {escape(tag)} of Cryptographic Triangles ({escape(label)}).</p>'
        desc = _dedup_html_paragraphs(desc)
        author = r.get('author', {}).get('login', 'SamiAhmed7777')
        installer, installer_name = _installer_asset(r, tag, repo)
        if installer_name:
            download_html = (f'<p><strong>Download:</strong> <a href="{installer}">'
                             f'{escape(installer_name)}</a></p>')
        else:
            download_html = (f'<p><strong>Download:</strong> <a href="{installer}">'
                             f'release page for {escape(tag)}</a></p>')
        items.append((sort_key, f"""    <item>
      <title>{escape(name)}</title>
      <link>{html_url}</link>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{rss_date}</pubDate>
      <author>noreply@github.com ({escape(author)})</author>
      <category>release</category>
      <category>{escape(label)}</category>
      <description><![CDATA[{desc}
{download_html}<p><strong>SHA-256:</strong> Published in the <a href="{html_url}">release notes on GitHub</a> and on the website's download section.</p>]]></description>
    </item>"""))
    # newest first, regardless of source repo
    items.sort(key=lambda x: x[0], reverse=True)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SITE_TITLE}</title>
    <link>{SITE_URL}/releases.xml</link>
    <atom:link href="{SITE_URL}/releases.xml" rel="self" type="application/rss+xml" />
    <description>{SITE_DESC}</description>
    <language>en-us</language>
    <managingEditor>noreply@cryptographic-triangles.org (Cryptographic Triangles)</managingEditor>
    <webMaster>noreply@cryptographic-triangles.org (Cryptographic Triangles)</webMaster>
    <copyright>Copyright © 2014–2026 Cryptographic Triangles. Released under the MIT License.</copyright>
    <lastBuildDate>{now}</lastBuildDate>
    <generator>tri-website-rss-generator (GitHub Actions)</generator>
{chr(10).join(x[1] for x in items)}
  </channel>
</rss>
"""

def _is_desktop_release(r):
    """Desktop release = stable, not a test tag, not a tri-pi ARM build."""
    tag = r.get('tag_name', '') or ''
    if r.get('prerelease'):
        return False
    if tag.endswith('.dist-test'):
        return False
    if tag.startswith('tri-pi-'):
        return False
    return True

if __name__ == "__main__":
    import os
    merged = []
    for label, repo in SOURCES:
        rels = [r for r in fetch_releases(repo) if _is_desktop_release(r)]
        print(f"{repo}: {len(rels)} desktop releases")
        merged.extend((label, repo, r) for r in rels)
    rss = build_rss(merged)
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "releases.xml")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(rss)
    print(f"Written {out_path} ({len(rss):,} bytes, {len(merged)} items)")
