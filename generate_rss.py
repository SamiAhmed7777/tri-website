#!/usr/bin/env python3
"""Generate releases.xml (RSS 2.0) from GitHub releases API."""
import json
import urllib.request
import urllib.parse
import datetime
import hashlib
import re
from packaging.version import Version, InvalidVersion
from xml.sax.saxutils import escape

REPO = "SamiAhmed7777/triangles_v5"
SITE_URL = "https://cryptographic-triangles.org"
SITE_TITLE = "Cryptographic Triangles — Release Notes"
SITE_DESC = "Official release notes for the Cryptographic Triangles Qt Wallet. Subscribe to get notified when new versions ship."

API_URL = f"https://api.github.com/repos/{REPO}/releases?per_page=100"

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
    # Paragraphs (double newline).
    # If a paragraph contains a block-level element (<ul>, <ol>, <pre>),
    # split it: the block element becomes its own block, and any inline
    # content before/after is wrapped in its own <p>. This prevents
    # invalid HTML5 like <p>...<ul>...</ul></p> from being emitted when
    # the markdown is e.g. "Lead text:\n- item\n- item".
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
        # Split paragraph into pre-block / block / post-block segments.
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
    auto-generated release bodies, sometimes with slightly different URLs
    (one semantic, one commit-level). After our semantic-URL rewrite both
    lines collapse to the same <p>...</p> block. This pass removes any
    consecutive run of identical <p>...</p> blocks so the feed shows
    just one. First occurrence wins.
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


def _semantic_compare_urls(releases):
    """Build a map of tag -> correct prev-tag compare URL.

    GitHub's auto-generated release body sometimes uses a commit SHA in
    the 'compare/...' URL instead of the immediately previous version tag.
    This computes the canonical prev-tag -> this-tag URL by sorting all
    tags and using the version immediately preceding each one.
    """
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
            urls[tag] = f"https://github.com/{REPO}/compare/{tag}\u00b0"
        else:
            prev_tag = tag_versions[i - 1][1]
            urls[tag] = f"https://github.com/{REPO}/compare/{prev_tag}...{tag}"
    return urls


def build_rss(releases):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    compare_urls = _semantic_compare_urls(releases)
    for r in releases:
        tag = r.get('tag_name', '')
        name = r.get('name') or tag
        body = r.get('body') or ''
        # Rewrite the Full Changelog URL in the body to use the canonical
        # prev-tag -> this-tag compare URL instead of whatever GitHub
        # auto-generated (which is sometimes a commit SHA).
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
        except Exception:
            rss_date = now
        guid = f"tri-release-{tag}-{hashlib.md5(html_url.encode()).hexdigest()[:8]}"
        # Description
        desc = md_to_html(body)
        if not desc.strip():
            desc = f'<p>Release {escape(tag)} of Cryptographic Triangles Qt Wallet.</p>'
        desc = _dedup_html_paragraphs(desc)
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

def _is_desktop_release(r):
    """Desktop wallet release = stable, not a test tag, not a tri-pi ARM build."""
    tag = r.get('tag_name', '') or ''
    if r.get('prerelease'):
        return False
    if tag.endswith('.dist-test'):
        return False
    if tag.startswith('tri-pi-'):
        return False
    return True


if __name__ == "__main__":
    releases = fetch_releases()
    clean = [r for r in releases if _is_desktop_release(r)]
    print(f"Found {len(releases)} releases total, {len(clean)} desktop (filtering prereleases, dist-test, tri-pi-*)")
    rss = build_rss(clean)
    with open('/tmp/tri-website/releases.xml', 'w', encoding='utf-8') as f:
        f.write(rss)
    print(f"Written /tmp/tri-website/releases.xml ({len(rss):,} bytes, {len(clean)} items)")
