#!/usr/bin/env python3
"""Build the final HTML and CSS with images inlined as data URIs."""
import base64
import os

LOGO_256 = '/tmp/tri-website/assets/logo-256.png'
LOGO_128 = '/tmp/tri-website/assets/logo-128.png'
LOGO_64 = '/tmp/tri-website/assets/logo-64.png'
LOGO_32 = '/tmp/tri-website/assets/logo-32.png'

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

LOGO_256_B64 = b64(LOGO_256)
LOGO_128_B64 = b64(LOGO_128)
LOGO_64_B64 = b64(LOGO_64)
LOGO_32_B64 = b64(LOGO_32)
FAVICON_B64 = b64(LOGO_32)  # 32x32 PNG works as favicon in modern browsers

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Cryptographic Triangles (TRI) is a privacy-focused cryptocurrency featuring Proof-of-Stake consensus, Tor v3 onion routing, and encrypted peer-to-peer messaging. Originally launched July 2014." />
  <meta name="theme-color" content="#e32105" />
  <meta property="og:title" content="Cryptographic Triangles Qt Wallet" />
  <meta property="og:description" content="Privacy-focused cryptocurrency with PoS staking, Tor v3 routing, and encrypted messaging." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://cryptographic-triangles.org" />
  <meta property="og:image" content="https://cryptographic-triangles.org/logo-256.png" />
  <title>Cryptographic Triangles — Privacy-focused cryptocurrency wallet</title>
  <link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,__FAVICON__" />
  <link rel="apple-touch-icon" href="data:image/png;base64,__LOGO256__" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <nav class="topnav">
    <div class="container nav-inner">
      <a class="brand" href="#">
        <img src="data:image/png;base64,__LOGO32__" alt="" width="28" height="28" />
        <span>Cryptographic Triangles</span>
      </a>
      <div class="nav-links">
        <a href="#features">Features</a>
        <a href="#download">Download</a>
        <a href="https://blocks.cryptographic-triangles.org/" rel="noopener" target="_blank">Block Explorer</a>
        <a href="#source">Source</a>
      </div>
    </div>
  </nav>

  <header class="hero">
    <div class="container">
      <img class="hero-logo" src="data:image/png;base64,__LOGO256__" alt="Cryptographic Triangles logo" width="128" height="128" />
      <h1>Cryptographic Triangles</h1>
      <p class="tagline">A privacy-focused cryptocurrency with Proof-of-Stake consensus, Tor v3 routing, and encrypted peer-to-peer messaging.</p>
      <div class="cta-row">
        <a href="#download" class="cta">Download for Windows</a>
        <a href="https://blocks.cryptographic-triangles.org/" rel="noopener" target="_blank" class="cta cta-secondary">View Block Explorer</a>
      </div>
      <p class="version-line">Latest stable: <strong>5.9.23</strong> · <a href="https://github.com/SamiAhmed7777/triangles_v5/releases">all releases</a></p>
    </div>
  </header>

  <section id="features">
    <div class="container">
      <h2>What it does</h2>
      <div class="features">
        <div class="feature">
          <div class="feature-icon">▲</div>
          <h3>Proof-of-Stake</h3>
          <p>33% annual reward for staking. No mining rigs, no electricity bills — stake your TRI and let the network do the work.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">◉</div>
          <h3>Tor v3 routing</h3>
          <p>Native Tor v3 onion routing for every transaction. Your IP address never reaches the peers you're talking to.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">✉</div>
          <h3>Encrypted messaging</h3>
          <p>Built-in peer-to-peer encrypted chat — talk to other TRI users without ever leaving the wallet, no third-party servers.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">⌘</div>
          <h3>Hash9 algorithm</h3>
          <p>A unique 13-step hash cascade. Designed in 2014, refined through a decade of cryptographic iteration, fully open-source.</p>
        </div>
      </div>
    </div>
  </section>

  <section id="download">
    <div class="container">
      <h2>Download</h2>
      <p>Cryptographic Triangles Qt Wallet is open-source software, released under the MIT License. The official source is the <a href="https://github.com/SamiAhmed7777/triangles_v5">triangles_v5 repository on GitHub</a>.</p>

      <div class="download-card">
        <div class="download-card-header">
          <h3>Windows (x64)</h3>
          <span class="download-size">~64 MB</span>
        </div>
        <p>Qt-based desktop wallet with full graphical interface. Built with NSIS, runs on Windows 10 and later.</p>
        <a href="https://github.com/SamiAhmed7777/triangles_v5/releases/download/v5.9.23/Cryptographic-Triangles-5.9.23-win-x64-setup.exe" class="btn">Download installer</a>
        <details class="hash-block">
          <summary>Verify your download (SHA-256)</summary>
          <code id="sha256">f970c1f7fa8609b676b51a9685a95bdde84f226707811c25f647b2c89974c7c7</code>
          <button type="button" class="copy-btn" data-target="sha256" aria-label="Copy SHA-256 to clipboard">Copy</button>
        </details>
        <p class="hash-hint">On Windows, verify with: <code>certutil -hashfile Cryptographic-Triangles-5.9.23-win-x64-setup.exe SHA256</code></p>
      </div>

      <p class="other-downloads">Looking for other platforms or older versions? See <a href="https://github.com/SamiAhmed7777/triangles_v5/releases">all releases on GitHub</a>. Source code and build instructions are in the <a href="https://github.com/SamiAhmed7777/triangles_v5">triangles_v5 repository</a>.</p>
    </div>
  </section>

  <section id="explorer" class="explorer-section">
    <div class="container">
      <h2>Block explorer</h2>
      <p>Every block, transaction, address, and validator on the Cryptographic Triangles network — searchable, with full Tor-v3 anonymized network metadata.</p>
      <a href="https://blocks.cryptographic-triangles.org/" rel="noopener" target="_blank" class="btn btn-large">Open the block explorer</a>
    </div>
  </section>

  <section id="privacy">
    <div class="container">
      <h2>Privacy by design</h2>
      <p>Cryptographic Triangles was built from the ground up for privacy. There are no centralized servers, no analytics, no telemetry, and no accounts. Wallet addresses are not linked to personal identity. Network traffic uses Tor v3 by default — your IP address never leaks to other peers, ever.</p>
      <p>Everything is open-source under the MIT license, so you can verify these claims yourself by reading the source code. We don't ask you to trust us; we publish the code that lets you check.</p>
    </div>
  </section>

  <section id="source">
    <div class="container">
      <h2>Source &amp; community</h2>
      <ul class="links">
        <li><strong>Main repo:</strong> <a href="https://github.com/SamiAhmed7777/triangles_v5">github.com/SamiAhmed7777/triangles_v5</a></li>
        <li><strong>Block explorer:</strong> <a href="https://blocks.cryptographic-triangles.org/">blocks.cryptographic-triangles.org</a></li>
        <li><strong>License:</strong> <a href="https://github.com/SamiAhmed7777/triangles_v5/blob/master/LICENSE">MIT</a></li>
        <li><strong>Releases &amp; changelog:</strong> <a href="https://github.com/SamiAhmed7777/triangles_v5/releases">github.com/SamiAhmed7777/triangles_v5/releases</a></li>
      </ul>
    </div>
  </section>

  <footer>
    <div class="container">
      <p>© 2014–2026 Cryptographic Triangles. Released under the MIT License.</p>
    </div>
  </footer>

  <script>
    (function () {
      var btn = document.querySelector('.copy-btn');
      if (!btn) return;
      btn.addEventListener('click', function () {
        var target = document.getElementById(btn.getAttribute('data-target'));
        if (!target) return;
        try {
          navigator.clipboard.writeText(target.textContent.trim());
          var orig = btn.textContent;
          btn.textContent = 'Copied!';
          setTimeout(function () { btn.textContent = orig; }, 1500);
        } catch (e) {
          var range = document.createRange();
          range.selectNode(target);
          window.getSelection().removeAllRanges();
          window.getSelection().addRange(range);
        }
      });
    })();
  </script>
</body>
</html>
'''

# Substitute the base64 placeholders
html = (HTML
    .replace('__LOGO32__', LOGO_32_B64)
    .replace('__LOGO256__', LOGO_256_B64)
    .replace('__FAVICON__', FAVICON_B64)
)

# Write the final HTML
with open('/tmp/tri-website/index.html', 'w') as f:
    f.write(html)

print(f"index.html written: {len(html):,} bytes")
print(f"  logo-32 base64:  {len(LOGO_32_B64):,} chars")
print(f"  logo-256 base64: {len(LOGO_256_B64):,} chars")