#!/usr/bin/env python3
"""Build site with Contact + FAQ sections added, logos inlined."""
import base64

LOGO_256 = '/tmp/tri-website/assets/logo-256.png'
LOGO_128 = '/tmp/tri-website/assets/logo-128.png'
LOGO_64 = '/tmp/tri-website/assets/logo-64.png'
LOGO_32 = '/tmp/tri-website/assets/logo-32.png'

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

LOGO_256_B64 = b64(LOGO_256)
LOGO_32_B64 = b64(LOGO_32)
FAVICON_B64 = b64(LOGO_32)

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
        <a href="#staking">Staking</a>
        <a href="#explorer">Block Explorer</a>
        <a href="#faq">FAQ</a>
        <a href="#contact">Contact</a>
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

  <section id="staking" class="staking-section">
    <div class="container">
      <h2>Staking &amp; network</h2>
      <p>Triangles runs on a pure Proof-of-Stake consensus model — no mining, no hardware arms race, no wasted energy.</p>

      <div class="staking-grid">
        <div class="staking-stat">
          <div class="stat-value">33%</div>
          <div class="stat-label">Annual staking reward</div>
        </div>
        <div class="staking-stat">
          <div class="stat-value">2014</div>
          <div class="stat-label">Network launched</div>
        </div>
        <div class="staking-stat">
          <div class="stat-value">Hash9</div>
          <div class="stat-label">13-step algorithm</div>
        </div>
      </div>

      <h3>How staking works</h3>
      <p>Open the Qt Wallet, hold TRI in your wallet, and you're eligible to be selected as a validator for the next block. No special hardware, no locked contracts — your wallet stays in your control the entire time. Rewards are paid in TRI and compound automatically as you continue to stake.</p>

      <p>For current network stats, total supply, and active validators, see the <a href="https://blocks.cryptographic-triangles.org/" rel="noopener" target="_blank">block explorer</a>.</p>
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

  <section id="faq">
    <div class="container">
      <h2>Frequently asked questions</h2>

      <details class="faq-item">
        <summary>Is Triangles a fork of Bitcoin / Monero / another coin?</summary>
        <p>Triangles has its own consensus algorithm (Hash9, a 13-step hash cascade designed in 2014) and its own codebase. It is not a Bitcoin fork and not a Monero fork. The wallet and node software are written in C++ with a Qt-based UI, fully open-source.</p>
      </details>

      <details class="faq-item">
        <summary>How is 33% APR staking sustainable?</summary>
        <p>Like any PoS coin, the rate reflects new TRI issued per year as a fraction of the staked supply. The exact emissions curve is documented in the source repository. As more TRI is staked, the per-staker yield naturally dilutes — early stakers receive higher relative rewards, later stakers receive less. There is no "infinite" issuance; the supply is capped.</p>
      </details>

      <details class="faq-item">
        <summary>What does "Tor v3 by default" actually do?</summary>
        <p>Every network peer connection is wrapped in a Tor v3 (next-generation onion) circuit. Your IP address is never exposed to peers you're transacting with, and vice versa. You can disable this in advanced settings if you need to, but for most users the default privacy posture is what you want.</p>
      </details>

      <details class="faq-item">
        <summary>Is the encrypted messaging a separate app?</summary>
        <p>No — it's built into the Qt Wallet. Open the messaging panel, add a contact by their TRI address, and you have end-to-end encrypted chat. The protocol is peer-to-peer (no servers), and messages route over the same Tor-v3 network as transactions.</p>
      </details>

      <details class="faq-item">
        <summary>Is this project still active?</summary>
        <p>Yes. Latest release v5.9.23 (June 2026). Source is updated regularly, releases happen on a steady cadence, and the block explorer at <a href="https://blocks.cryptographic-triangles.org/">blocks.cryptographic-triangles.org</a> is live.</p>
      </details>

      <details class="faq-item">
        <summary>How can I verify the source code matches the binary I downloaded?</summary>
        <p>Clone the <a href="https://github.com/SamiAhmed7777/triangles_v5">triangles_v5 repository</a>, check out the v5.9.23 tag, and follow the build instructions. Or just diff the binary against the official NSIS installer SHA-256 published on this page.</p>
      </details>
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

  <section id="contact" class="contact-section">
    <div class="container">
      <h2>Get in touch</h2>
      <p class="contact-lead">The Triangles development team is reachable primarily through Triangles' own encrypted peer-to-peer messaging — built into the wallet, routed over Tor v3, no third-party servers, no accounts.</p>

      <div class="contact-grid">
        <div class="contact-card">
          <div class="contact-icon">✉</div>
          <h3>Developer contact</h3>
          <p>The fastest way to reach the team. Open the Qt Wallet → Messages tab → add a contact by their TRI address. Everything stays end-to-end encrypted and IP-anonymous.</p>
        </div>

        <div class="contact-card">
          <div class="contact-icon">⚙</div>
          <h3>Bug reports &amp; code</h3>
          <p>Open a GitHub issue on the <a href="https://github.com/SamiAhmed7777/triangles_v5/issues">triangles_v5 repo</a>. Include the version, OS, and steps to reproduce. PRs welcome.</p>
        </div>

        <div class="contact-card">
          <div class="contact-icon">🔒</div>
          <h3>Security disclosures</h3>
          <p>Found a vulnerability? Reach the team through the wallet's encrypted messaging channel first. Don't post security issues publicly until a fix is released.</p>
        </div>
      </div>

      <p class="contact-note">We don't run official social media accounts. Anything claiming to be "official Triangles" on Twitter, Telegram, Discord, or Reddit is fan-run or impersonation. The <a href="https://github.com/SamiAhmed7777/triangles_v5">GitHub repository</a> and this website are the only public surfaces maintained by the development team.</p>
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

html = (HTML
    .replace('__LOGO32__', LOGO_32_B64)
    .replace('__LOGO256__', LOGO_256_B64)
    .replace('__FAVICON__', FAVICON_B64)
)

with open('/tmp/tri-website/index.html', 'w') as f:
    f.write(html)

print(f"index.html: {len(html):,} bytes")