<!-- ──────────────────────────────────────────────────────────────── -->
<!--  Fuad Ahamed · GitHub Profile README                             -->
<!--  Banner source + build script: assets/render/                    -->
<!-- ──────────────────────────────────────────────────────────────── -->

<div align="center">

<!-- Banner: a rendered particle iris (~400k emitters, depth of field, motion blur, bloom). Source in assets/render/ -->
<picture>
  <img src="assets/banner-purple-team.webp" width="100%" alt="Fuad Ahamed: SOC analyst and penetration tester, with agentic AI and full-stack skills. An animated particle iris: blue-team particles at the rim flow inward and turn red-team crimson at the core while a radar sweep turns and one red threat is tracked into containment" />
</picture>

<h3>Security engineer who builds: blue-team detection, red-team testing, and the AI and full-stack skills to ship my own tools.</h3>

<p>SOC & detection engineering · penetration testing · agentic AI · full-stack · 3D digital twins</p>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=21&duration=2800&pause=900&color=A878FF&center=true&vCenter=true&width=640&lines=SOC+Analyst+%C2%B7+Detection+Engineering;Penetration+Tester+%C2%B7+Offensive+Security;Purple+Team%3A+blue+%2B+red%2C+one+person;Agentic+AI+%C2%B7+Full-Stack+%C2%B7+Digital+Twins;2%C3%97+1st-Place+Hackathon+Winner" alt="typing intro" />

<br/><br/>

<a href="https://github.com/FuadAhamed91"><img src="https://img.shields.io/badge/GitHub-FuadAhamed91-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
<a href="mailto:fuadoow@gmail.com"><img src="https://img.shields.io/badge/Email-fuadoow%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
<!-- LinkedIn badge: uncomment and set your URL
<a href="https://www.linkedin.com/in/YOUR-HANDLE/"><img src="https://img.shields.io/badge/LinkedIn-Fuad%20Ahamed-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
-->

<br/><br/>

<img src="https://komarev.com/ghpvc/?username=FuadAhamed91&style=flat-square&color=a878ff&label=Profile+Views" alt="profile views" />
<a href="https://github.com/FuadAhamed91?tab=followers"><img src="https://img.shields.io/github/followers/FuadAhamed91?style=flat-square&logo=github&label=Followers&color=6096ff" alt="followers" /></a>
<img src="https://img.shields.io/badge/Based%20in-UAE-2ea043?style=flat-square&logo=googlemaps&logoColor=white" alt="location" />

<br/><br/>

<img src="https://img.shields.io/badge/SOC%20Analyst-1F6FEB?style=flat-square" alt="SOC Analyst" />
<img src="https://img.shields.io/badge/Penetration%20Tester-D7263D?style=flat-square" alt="Penetration Tester" />
<img src="https://img.shields.io/badge/Purple%20Team-7C3AED?style=flat-square" alt="Purple Team" />
<img src="https://img.shields.io/badge/Detection%20Engineering-0F766E?style=flat-square" alt="Detection Engineering" />
<img src="https://img.shields.io/badge/Agentic%20AI-9333EA?style=flat-square" alt="Agentic AI" />
<img src="https://img.shields.io/badge/Full--Stack-2EA043?style=flat-square" alt="Full-Stack" />
<img src="https://img.shields.io/badge/2%C3%97%201st%20Place-C9A227?style=flat-square" alt="2× 1st place" />

</div>

<br/>

<img src="assets/divider.svg" width="100%" alt="" />

## 🛡️ Security First

I work both sides of the wire. On the **blue team** I build detections and prove they fire. On the **red team** I find the way in before someone else does. And because I'm also a developer, I build the tools, dashboards and agents I need to do both.

| 🔵 Blue team · SOC & detection | 🔴 Red team · penetration testing | 🟣 Agentic AI & security tooling |
|---|---|---|
| Endpoint telemetry with **Wazuh + Sysmon**. Techniques detonated with **Atomic Red Team**. Rules written in **Sigma** first, then as SIEM-native rules, with coverage measured against **MITRE ATT&CK**. | Recon and enumeration (**Nmap**), web-app testing against the **OWASP Top 10** (**Burp Suite**), exploitation and post-exploitation in authorised labs (**Metasploit**), packet analysis (**Wireshark**), and reports that explain the fix. | Agents that watch and pay: **AgentSentinel** sells monitoring to AI agents over **x402**. Security tools I wrote myself: a phishing-link scorer and a runtime firewall for IDE plugins. LLM features built to **fail safe**. |

**How I write a detection** (from [`cloud-soc-lab`](https://github.com/FuadAhamed91/cloud-soc-lab)):

```text
 detonate ──▶ collect ──▶ analyse ──▶ write rule ──▶ re-detonate ──▶ record
 Atomic Red   Sysmon →    decide the   Sigma first,   must fire, and   ATT&CK coverage
 Team         Wazuh       logic        then Wazuh     must NOT fire    matrix updated
                                                      on benign noise
```

### 🔐 Security Projects

**🧪 [cloud-soc-lab](https://github.com/FuadAhamed91/cloud-soc-lab)**: SOC + cloud detection-engineering lab
> Built to answer the interview question *"Show me a detection you wrote, and how you know it works."* Simulate the attacker, find the gaps in default detection, write the rule, and prove it.
- Endpoint lab: **Wazuh + Sysmon + Atomic Red Team**, with custom rules mapped to ATT&CK and a test record for every technique.
- Next: cloud detection (**CloudTrail / GuardDuty → SIEM**, Stratus Red Team, **Terraform**, Prowler) and serverless phishing triage.
- ⚙️ `Wazuh` `Sysmon` `Sigma` `Atomic Red Team` `MITRE ATT&CK` `Vagrant` `Terraform`

**🎣 [phishing-detector-extension](https://github.com/FuadAhamed91/phishing-detector-extension)**: hover a link, see where it *really* goes
> A Chrome (MV3) extension that gives every link a 1–100 safety score, with the reasons. No network calls, no data collection.
- Unwraps Google, Microsoft Safe Links, Proofpoint and Barracuda redirectors, then scores the real destination.
- Catches look-alike domains (`amaz0n`, `rnicrosoft`, Cyrillic punycode), the `user@host` trick, raw IPs, abused TLDs and brand names on domains the brand doesn't own. ~80 impersonated brands covered.
- ⚙️ `JavaScript` `Chrome MV3` `public-suffix parsing` `homograph detection`

**🧱 [PluginFence](https://github.com/bilal-feroz/PluginFence)**: a runtime firewall for IntelliJ plugins *(team build)*
> IDE plugins run with full access to your SSH keys, `.env` files and cloud credentials. PluginFence watches what a plugin *actually* tries to do, then allows it, blocks it or raises an alert, and flags behaviour that changes after an update.
- ⚙️ `Kotlin` `JVM agent (java.lang.instrument)` `policy engine` · I built the hackathon pitch deck.

**🔗 [AgentSentinel](https://github.com/FuadAhamed91/agentsentinel)**: monitoring sold *to* AI agents
> Live on the XDC AI marketplace. Agents pay per call in USDC (x402) for an on-chain merchant leaderboard and for price, gas and wallet watches that catch the moves that happen between two checks.
- ⚙️ `Node.js` `XDC` `x402` `USDC` `SQLite` `Replit`

### 🧰 Security Toolbox

<div align="center">

**Blue team**

<img src="https://img.shields.io/badge/Wazuh-0098DB?style=for-the-badge" alt="Wazuh" />
<img src="https://img.shields.io/badge/Sysmon-0078D4?style=for-the-badge" alt="Sysmon" />
<img src="https://img.shields.io/badge/Sigma%20Rules-1C3C3C?style=for-the-badge" alt="Sigma" />
<img src="https://img.shields.io/badge/Atomic%20Red%20Team-B91C1C?style=for-the-badge" alt="Atomic Red Team" />
<img src="https://img.shields.io/badge/MITRE%20ATT%26CK-C20000?style=for-the-badge" alt="MITRE ATT&CK" />
<img src="https://img.shields.io/badge/CloudTrail%20%C2%B7%20GuardDuty-232F3E?style=for-the-badge" alt="AWS CloudTrail and GuardDuty" />

**Red team**

<img src="https://img.shields.io/badge/Kali%20Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white" alt="Kali Linux" />
<img src="https://img.shields.io/badge/Nmap-0E83CD?style=for-the-badge" alt="Nmap" />
<img src="https://img.shields.io/badge/Burp%20Suite-FF6633?style=for-the-badge&logo=burpsuite&logoColor=white" alt="Burp Suite" />
<img src="https://img.shields.io/badge/Metasploit-2596CD?style=for-the-badge&logo=metasploit&logoColor=white" alt="Metasploit" />
<img src="https://img.shields.io/badge/Wireshark-1679A7?style=for-the-badge&logo=wireshark&logoColor=white" alt="Wireshark" />
<img src="https://img.shields.io/badge/OWASP%20Top%2010-000000?style=for-the-badge&logo=owasp&logoColor=white" alt="OWASP Top 10" />

**Scripting & infrastructure**

<img src="https://skillicons.dev/icons?i=linux,bash,powershell,python,aws,terraform,docker&theme=dark" alt="scripting and infrastructure" />

</div>

<img src="assets/divider.svg" width="100%" alt="" />

## 🏆 Hackathon Wins

<div align="center">

<img src="assets/wins.png" width="100%" alt="Two first places: AI Everything Hackathon with UnderGrid, and Oriane × Replit (1st of 48 teams) with PRE//FLIGHT" />

</div>

| Result | Event | Build | What it does |
|---|---|---|---|
| 🥇 **1st Place** | **AI Everything Hackathon** | **[UnderGrid](https://github.com/bilal-feroz/qoder-hackathon)** | A live 3D digital twin of a city's underground water, sewage, power and cooling network. It connects weak sensor signals (a 2.7% pressure drop, wetter soil, warmer ground), pinpoints the failing pipe and the spot on it, forecasts the failure window, and hands crews a repair plan. In the demo scenario, an ~AED 660K planned repair avoids ~AED 5.94M of damage. |
| 🥇 **1st Place** (of 48 teams) | **Build for the Video Economy** (Oriane × Replit, Dubai) | **PRE//FLIGHT** | Tells brands whether their campaign idea has already been done, *before* they spend money shooting it. It searches real Instagram and TikTok videos through Oriane, shows how crowded the idea is, and points to where there's still room. [Demo video →](https://www.youtube.com/watch?v=g_B3rjgLcC4) |

**Other competition builds**

| Event | Build | |
|---|---|---|
| 🎮 **Cambridge × Arcade AI Hackathon** (Game Tech Track) | **[Materialize](https://github.com/FuadAhamed91/Materialize)** | Type any object, an LLM works out its real-world physics, and it materializes · [play](https://materialize-eight.vercel.app) |
| 📡 **ATRC Advanced Technology Pioneers 2026** (EDGE Challenge) | **[FlexiPath](https://github.com/FuadAhamed91/FlexiPath)** | Predictive, traffic-aware connectivity across Wi-Fi / 5G / LEO / wired, shown on a Three.js drone digital twin |
| 🏜️ **Sharjah Tourism Innovation Hackathon** | **[Fadhal](https://github.com/Mohammad-Umar7/LOCALDAYS)** | Book Sharjah's living traditions and step inside each venue in 3D · [live](https://localdays.vercel.app) |
| 🛡️ Team hackathon build | **[PluginFence](https://github.com/bilal-feroz/PluginFence)** | Runtime firewall for IntelliJ plugins |

<img src="assets/divider.svg" width="100%" alt="" />

## 🛠️ …and I Build, Too

Security is easier when you can build what you defend. These are the products, twins and games I've shipped or committed to.

### 🌆 UnderGrid: Underground Infrastructure Digital Twin · 🥇 AI Everything

<a href="https://github.com/bilal-feroz/qoder-hackathon"><img src="https://img.shields.io/badge/Code-UnderGrid-181717?style=flat-square&logo=github" alt="code" /></a>
<img src="https://img.shields.io/badge/Team-Awaiz%20%C2%B7%20Bilal%20%C2%B7%20Umar%20%C2%B7%20Fuad-7C3AED?style=flat-square" alt="team" />

- **Flow →** DETECT a subsurface anomaly → PREDICT the failure horizon (36–52 h) → PRIORITIZE by the hospitals, schools and traffic nearby → PLAN the crew, detours, parts and dig.
- **The twin →** the city turns see-through, the faulty pipe glows, and the affected buildings light up. I built the **+48H view**, which shows the burst if nobody acts.
- ⚙️ `TypeScript` `Three.js` `3D digital twin` `sensor simulation`

### 🏥 CareLoop: Post-Discharge Patient Follow-Up on WhatsApp

<a href="https://github.com/FuadAhamed91/-DischargeIQ"><img src="https://img.shields.io/badge/Code-DischargeIQ-181717?style=flat-square&logo=github" alt="code" /></a>
<a href="https://discharge-iq.vercel.app"><img src="https://img.shields.io/badge/Live-Demo-2ea043?style=flat-square&logo=vercel&logoColor=white" alt="demo" /></a>

- A nurse drops in the discharge PDF and Gemini reads it into a care plan, which the nurse approves before the patient gets it on WhatsApp. Symptom reports are triaged against the patient's own warning signs, and they still escalate when the model is down.
- **Security model →** multi-tenant Postgres with **Row Level Security** on every row, six staff roles, and secrets kept in Supabase Vault. About 90 of the commits are mine.
- ⚙️ `Next.js 16` `TypeScript` `Supabase` `Twilio WhatsApp` `Gemini 2.5 Flash` `Vercel`

### 📡 FlexiPath: Predictive Connectivity Engine · ATRC EDGE 2026

<a href="https://github.com/FuadAhamed91/FlexiPath"><img src="https://img.shields.io/badge/Code-FlexiPath-181717?style=flat-square&logo=github" alt="code" /></a>

- Two identical drones fly the same corridor (dock → Wi-Fi → 5G → LEO satellite). One runs FlexiPath and the other a legacy stack, under the same seeded radio field. FlexiPath predicts that a path is failing and moves before the break.
- Compared against MPTCP and 3GPP ATSSS baselines, with ablations, prediction precision and recall, and held-out seeds. Negative results are reported too.
- ⚙️ `JavaScript` `Three.js` `Blender Python` `network simulation`

### 🧪 Materialize · 🔎 The Spooky Crime Scene: games

<a href="https://materialize-eight.vercel.app"><img src="https://img.shields.io/badge/Play-Materialize-2ea043?style=flat-square&logo=unity&logoColor=white" alt="play Materialize" /></a>
<a href="https://the-spooky-crime-scene.vercel.app"><img src="https://img.shields.io/badge/Play-Spooky%20Crime%20Scene-2ea043?style=flat-square&logo=unity&logoColor=white" alt="play Spooky Crime Scene" /></a>

- **Materialize**: type any object and an LLM compiles its physics. Ten chambers cover mass, buoyancy, momentum, insulation and friction, and every solution is verified by automated tests.
- **The Spooky Crime Scene**: a first-person murder mystery with three cases, red herrings, informants and procedurally synthesised horror audio.
- ⚙️ `Unity 6 URP` `C#` `LLM` `Blender Python` `WebGL`

## 🗂️ Everything I've Built or Contributed To

```text
FuadAhamed91 · projects I built or committed to
│
├── 🛡️ Security
│   ├── cloud-soc-lab                → SOC detection-engineering lab · ATT&CK
│   ├── phishing-detector-extension  → link safety score on hover · MV3
│   └── PluginFence                  → runtime firewall for IntelliJ plugins
│
├── 🏆 Wins
│   ├── UnderGrid                    → 🥇 AI Everything Hackathon
│   └── PRE//FLIGHT                  → 🥇 Oriane × Replit (1st of 48)
│
├── 🤖 AI & Agents
│   ├── agentsentinel                → API sold to AI agents (x402)
│   └── CareLoop / -DischargeIQ      → WhatsApp patient follow-up · live
│
├── 🌐 Digital Twins & 3D
│   ├── FlexiPath                    → drone network-mobility twin · ATRC EDGE
│   └── Fadhal (LOCALDAYS)           → Sharjah traditions in 3D · live
│
├── 🎮 Games
│   ├── Materialize                  → LLM-compiled physics puzzles · playable
│   └── MysterySolver                → The Spooky Crime Scene · playable
│
└── 📱 Web & Mobile
    ├── elite-motors-workshop        → client site for an Abu Dhabi workshop · live
    └── fitness-app                  → Pulse · Flutter + Supabase
```

### 🧰 Dev Toolbox

<div align="center">

<img src="https://skillicons.dev/icons?i=ts,js,cs,java,kotlin,dart,html,css&theme=dark" alt="languages" />

<br/>

<img src="https://skillicons.dev/icons?i=react,nextjs,vite,tailwind,threejs,unity,blender,flutter&theme=dark" alt="frontend, 3D and games" />

<br/>

<img src="https://skillicons.dev/icons?i=nodejs,supabase,postgres,sqlite,vercel,git,github&theme=dark" alt="backend and data" />

<br/><br/>

<img src="https://img.shields.io/badge/Gemini%20API-4285F4?style=flat-square&logo=googlegemini&logoColor=white" alt="Gemini" />
<img src="https://img.shields.io/badge/Twilio%20WhatsApp-F22F46?style=flat-square" alt="Twilio" />
<img src="https://img.shields.io/badge/Replit-F26207?style=flat-square&logo=replit&logoColor=white" alt="Replit" />
<img src="https://img.shields.io/badge/XDC%20%C2%B7%20x402-0F172A?style=flat-square" alt="XDC" />
<img src="https://img.shields.io/badge/Chrome%20Extensions%20MV3-4285F4?style=flat-square&logo=googlechrome&logoColor=white" alt="Chrome extensions" />

</div>

<img src="assets/divider.svg" width="100%" alt="" />

## 📊 GitHub Signals

<div align="center">

<img src="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=FuadAhamed91&theme=tokyonight" height="170" alt="GitHub stats" />
<img src="https://streak-stats.demolab.com?user=FuadAhamed91&theme=tokyonight&hide_border=true&background=1A1B26&ring=A878FF&fire=FF4E5C&currStreakLabel=A878FF" height="170" alt="contribution streak" />

<br/><br/>

<img src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=FuadAhamed91&theme=tokyonight" height="170" alt="top languages by repo" />
<img src="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=FuadAhamed91&theme=tokyonight" height="170" alt="top languages by commit" />


</div>

<img src="assets/divider.svg" width="100%" alt="" />

## 🤝 Let's Talk

Open to **SOC and pentest roles**, **internships**, **hackathon teams**, and anyone who wants a security person who can also ship the product.

<div align="center">

<a href="mailto:fuadoow@gmail.com"><img src="https://img.shields.io/badge/Email%20Me-fuadoow%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="email" /></a>
<a href="https://github.com/FuadAhamed91"><img src="https://img.shields.io/badge/Follow-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>

<br/><br/>

<sub>Banner and avatar are rendered, not drawn: <a href="assets/render">assets/render</a> holds the particle renderer.</sub>

</div>
