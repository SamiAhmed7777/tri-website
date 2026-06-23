#!/usr/bin/env python3
"""Generate releases.xml (RSS 2.0) from GitHub releases API."""
import json
import urllib.request
import urllib.parse
import datetime
import hashlib
import re
from xml.sax.saxutils import escape

REPO = "SamiAhmed7777/triangles_v5"
SITE_URL = "https://cryptographic-triangles.org"
SITE_TITLE = "Cryptographic Triangles — Release Notes"
SITE_DESC = "Official release notes for the Cryptographic Triangles Qt Wallet. Subscribe to get notified when new versions ship."

API_URL = f"https://api.github.com/repos/{REPO}/releases?per_page=30"

def fetch_releases():
    req = urllib.request.Request(API_URL, headers={"User-Agent": "tri-website-rss-generator"})
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
    # Paragraphs (double newline)
    parts = re.split(r'\n\s*\n', md)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<h') or p.startswith('<ul') or p.startswith('<pre'):
            out.append(p)
        else:
            # Convert single newlines to <br>
            p = p.replace('\n', '<br>')
            out.append(f'<p>{p}</p>')
    return '\n'.join(out)

def build_rss(releases):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    for r in releases:
        tag = r.get('tag_name', '')
        name = r.get('name') or tag
        body = r.get('body') or ''
        html_url = r.get('html_url', '')
        published = r.get('published_at') or r.get('created_at', '')
        try:
            dt = datetime.datetime.fromisoformat(published.replace('Z', '+00:00'))
            rss_date = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
        except Exception:
            rss_date = now
        guid = f"tri-release-{tag}-{hashlib.md5(html_url.encode()).hexdigest()[:8]}"
        # Description
        desc = md_to_html(body)
        if not desc.strip():
            desc = f'<p>Release {escape(tag)} of Cryptographic Triangles Qt Wallet.</p>'
        # Author
        author = r.get('author', {}).get('login', 'SamiAhmed7777')
        # Installer link
        installer = f"https://github.com/{REPO}/releases/download/{tag}/Cryptographic-Triangles-{tag.lstrip('v')}-win-x64-setup.exe"
        items.append(f"""    <item>
      <title>{escape(name)}</title>
      <link>{html_url}</link>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{rss_date}</pubDate>
      <author>noreply@github.com ({escape(author)})</author>
      <category>release</category>
      <description><![CDATA[{desc}
<p><strong>Download:</strong> <a href="{installer}">Cryptographic-Triangles-{escape(tag.lstrip('v'))}-win-x64-setup.exe</a></p>
<p><strong>SHA-256:</strong> Available in the <a href="{html_url}">release notes on GitHub</a>.</p>]]></description>
    </item>""")
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
{chr(10).join(items)}
  </channel>
</rss>
"""

if __name__ == "__main__":
    releases = fetch_releases()
    # Filter out test releases (e.g., *.dist-test) and pre-releases
    clean = [r for r in releases if not r.get('prerelease') and not r.get('tag_name', '').endswith('.dist-test')]
    print(f"Found {len(releases)} releases total, {len(clean)} stable (filtering pre-releases and dist-test tags)")
    rss = build_rss(clean)
    with open('/tmp/tri-website/releases.xml', 'w', encoding='utf-8') as f:
        f.write(rss)
    print(f"Written /tmp/tri-website/releases.xml ({len(rss):,} bytes, {len(clean)} items)")
