# Open Source License Compliance for Solo SaaS Founders

## Why Open Source Compliance Matters

Your SaaS almost certainly depends on dozens (if not hundreds) of open source libraries. Each comes with a license that imposes conditions on how you can use it. Ignoring these licenses creates legal risk that can:

- Force you to release your proprietary source code
- Expose you to copyright infringement lawsuits
- Block acquisitions (due diligence reveals non-compliance)
- Prevent you from raising funding

**The good news:** Most open source licenses are permissive and fine to use in a commercial SaaS product. The risk comes from a few specific license types and from not tracking what you use.

## Open Source License Types

### Permissive Licenses (Safe for Commercial Use)

These licenses allow you to use, modify, and distribute the code with minimal restrictions. You can use them in a proprietary SaaS product.

| License | Conditions | Notes |
|---------|-----------|-------|
| **MIT** | Include copyright notice | Most popular, very simple |
| **Apache 2.0** | Include notice, state changes | Includes patent grant |
| **BSD (2/3-Clause)** | Include copyright notice | Very permissive |
| **ISC** | Include copyright notice | Nearly identical to MIT |
| **Unlicense** | None | Public domain equivalent |
| **CC0** | None | Public domain |

**Compliance requirements for permissive licenses:**
- Include the license notice in your application's credits/about page
- Include it in your documentation
- OR include it in a NOTICE file distributed with your software
- For SaaS (no distribution): Many of these requirements don't trigger since you're not distributing the software

### Weak Copyleft Licenses (Use with Caution)

These require you to share modifications to the licensed library but don't "infect" your entire codebase.

| License | Conditions | Notes |
|---------|-----------|-------|
| **LGPL** | Share modifications to the LGPL library; dynamic linking is OK | Safe if you use as a library (dynamic linking) |
| **MPL 2.0** | Share modifications to MPL files; new files can be proprietary | File-level copyleft |
| **EPL** | Share modifications to EPL files | Similar to MPL |
| **CDDL** | Share modifications to CDDL files | Similar to MPL |

**Compliance for weak copyleft:**
- Distribute source code for modified versions of the library
- You can keep your own code proprietary
- LGPL with dynamic linking is generally safe for SaaS

### Strong Copyleft Licenses (Dangerous for SaaS)

These require ANY code that uses the licensed code to also be open source under the same license. This is the "viral" or "infectious" effect.

| License | Conditions | Danger Level |
|---------|-----------|-------------|
| **GPL 2.0/3.0** | If you distribute the software, you must release the entire source code | ⚠️ High (if distributed) |
| **AGPL 3.0** | Same as GPL, but also applies to SaaS (network use = distribution) | 🔴 VERY HIGH |
| **SSPL** | MongoDB's license — specifically targets SaaS providers | 🔴 VERY HIGH |

**The AGPL problem for SaaS:**

The AGPL closes the "SaaS loophole" in the GPL. With regular GPL, you can use the code in a SaaS without releasing your source code because you're not "distributing" the software. The AGPL defines "interaction over a network" as distribution, meaning your SaaS must release its source code if it uses AGPL code.

**What to do:**
- **Never use AGPL code in your core product** unless you intend to open source it
- **Be very careful with GPL code** — understand how you're using it
- **Check all dependencies for GPL/AGPL** regularly

### Other Licenses

| License | Risk | Notes |
|---------|------|-------|
| **Commons Clause** | Restricts commercial use | Not open source (OSI disapproves) |
| **Business Source (BSL)** | Changes to open source after time limit | Commercial use OK during grace period |
| **Creative Commons (CC)** | Not for software (except CC0) | Only for content, documentation |
| **WTFPL** | Minimal restrictions | Not legally rigorous |
| **JSON License** | "The software shall be used for Good, not Evil" | Not enforceable, but ambiguity |

## Open Source Compliance Process

### Step 1: Inventory Your Dependencies

Use tools to automatically generate a dependency list.

**JavaScript/Node.js:**

```bash
# List all dependencies with licenses
npx license-checker --json > licenses.json
npx license-checker --summary

# Alternative: npx license-report
npx license-report --output=csv > licenses.csv

# Alternative: npm-license-audit
npx npm-license-audit
```

**Python:**

```bash
# List all dependencies
pip-licenses --format=json
pip-licenses --summary

# Check for restricted licenses
pip-licenses --allow-only="MIT, Apache 2.0, BSD, ISC"
```

**Ruby:**

```bash
# Check licenses
gem install license_finder
license_finder
```

**Go:**

```bash
# List dependencies with licenses
go-licenses csv ./...
go-licenses check ./...
```

**Rust:**

```bash
# Cargo license check
cargo install cargo-license
cargo license

# Or use cargo-deny for comprehensive checking
cargo deny check
```

**Java/Maven:**

```bash
# Generate license report
mvn license:third-party-report
```

### Step 2: Create a Dependency/License Inventory

Maintain a file like `DEPENDENCIES.md` or `NOTICE.md` in your repository root:

```markdown
# Third-Party Dependencies

## Direct Dependencies

| Package | Version | License | Source |
|---------|---------|---------|--------|
| react | 18.2.0 | MIT | https://github.com/facebook/react |
| express | 4.18.2 | MIT | https://github.com/expressjs/express |
| stripe-node | 12.14.0 | MIT | https://github.com/stripe/stripe-node |
| axios | 1.4.0 | MIT | https://github.com/axios/axios |
| posthog-js | 1.56.0 | MIT | https://github.com/PostHog/posthog-js |

## Transitive Dependencies (selected)

| Package | Version | License | Notes |
|---------|---------|---------|-------|
| ... | ... | ... | ... |

## Licenses Requiring Attributed
The following packages require attribution. See NOTICE file for details.

[List packages with MIT, Apache 2.0, BSD licenses that require attribution]
```

### Step 3: Create a NOTICE File

For projects using Apache 2.0, LGPL, MPL, or other licenses requiring attribution, create a `NOTICE` file:

```markdown
[Product Name]
Copyright [Year] [Company Name]

This product includes software developed by:
[Include details as required by each license]

---

This product contains modified versions of:

[Library Name] - Copyright [Year] [Author]
Licensed under the [License Name]. Original available at [URL].
Modifications: [Description of changes]

---

This product includes:

Library Name (https://github.com/author/library)
Copyright [Year] [Author]
Licensed under MIT License (LICENSE-MIT or http://opensource.org/licenses/MIT)
```

### Step 4: Choose Your Own Licenses

**For your codebase:**
- **MIT** — Simple, permissive, encourages adoption
- **Apache 2.0** — MIT-like but includes patent grant (safer for contributors)
- **Proprietary** — All rights reserved, no open source

**For documentation:**
- **CC BY 4.0** — Let others share with attribution
- **CC BY-SA 4.0** — Share-alike for documentation

**For website content:**
- **All rights reserved** (default copyright)

**If you open source parts of your code:**
- **MIT for libraries/sdks** — Encourages adoption
- **Apache 2.0 for core components** — Patent protection
- **AGPL for anything-else** — Discourages competitors from using it in proprietary products (though you'd need to accept the AGPL terms too)

### Step 5: Automate Compliance Checking

**GitHub Actions for license compliance:**

```yaml
name: License Check
on: [pull_request, push]
jobs:
  license-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - name: Check licenses
        run: npx license-checker --failOn "AGPL;GPL;SSPL;BUSL"
```

**CI integration tools:**

| Tool | Language | Cost | Features |
|------|----------|------|----------|
| **FOSSA** | All | Free (for public repos) | Full license management, policy engine |
| **Snyk** | All | Free tier | Vulnerability + license scanning |
| **WhiteSource** | All | Free for small projects | Comprehensive |
| **ClearlyDefined** | All | Free | License data curation |
| **license-checker** | Node | Free | Simple CLI check |
| **cargo-deny** | Rust | Free | Comprehensive + policy |
| **pip-licenses** | Python | Free | Simple Python check |

**Recommended: Use FOSSA (free for public repos) or Snyk (free tier)**
- Runs automatically on PRs
- Alerts you to problematic licenses
- Tracks dependencies over time

## The "SaaS Loophole" and Distribution

**Key concept:** Most open source license requirements (including attribution) are triggered by **distribution** of the software. If you run the software on your own server and only allow users to interact with it over a network, you are generally NOT distributing it.

This is why:
- You can use GPL libraries in your SaaS WITHOUT releasing your source code
- You DON'T have to display MIT license notices to every user
- Most open source compliance for SaaS is internal, not customer-facing

**Exception:** AGPL specifically closes this loophole. AGPL code in your SaaS = your SaaS must be open source.

**Exception:** If you distribute your software (mobile app, desktop app, embedded device), all distribution-related license obligations apply.

## Common Scenarios and Solutions

### Scenario 1: "I found a GPL library in my dependencies"

```
Problem: One of your transitive dependencies uses GPL
Risk: If GPL code is linked into your code, your entire project may need to be GPL

Solutions:
  → Remove the dependency (find an alternative)
  → If it's a tool (not linked): No problem
  → If it's dynamically linked: May still be a problem
  → If it's GPL-only and critical: Consider open sourcing your project (drastic)

Prevention:
  → Use a license checker in CI
  → Add GPL to your fail-on list
```

### Scenario 2: "I need to comply with MIT license attribution"

```
Problem: You use 50 MIT-licensed packages and need to include notices
Solutions:
  → Create a NOTICE file and include all MIT/BSD/Apache notices
  → Most licenses require: "The above copyright notice and this permission
    notice shall be included in all copies or substantial portions of the Software"
  → Since you're not distributing (SaaS), this is less critical
  → Good practice: include in your application's "About" page or docs
```

### Scenario 3: "A contractor copied code from an open source project"

```
Problem: A contractor copied code from a GPL project into your proprietary code
Risk: Your entire codebase could be contaminated

Solutions:
  → Immediately identify and isolate the contaminated code
  → Rewrite the functionality from scratch (clean room)
  → If the code is small: remove it
  → If already deployed: consult a lawyer

Prevention:
  → Include in contractor agreements: "All code must be original or properly licensed"
  → Code review should flag suspicious code (copy-paste)
  → Run license checks on all contributions
```

### Scenario 4: "I want to open source part of my SaaS"

```
Problem: You want to release a library as open source but keep your backend proprietary

Solution:
  → Create a separate repository for the open source library
  → Ensure no proprietary code is in the library
  → Choose MIT or Apache 2.0 license
  - Include a CONTRIBUTING.md with CLA requirements
  → Maintain separate build and CI for open source vs proprietary

Note: Once you release something as open source, you cannot un-release it.
Be very deliberate about what you open source.
```

## Open Source Compliance Policy Template

```markdown
Open Source Compliance Policy

1. Purpose
   This policy ensures [Company] complies with all open source license
   obligations in our software.

2. Roles
   - Founder: Final authority on license compliance
   - Developers: Responsible for reporting and complying

3. Dependency Approval
   - Developers may use any permissively-licensed dependency (MIT, Apache,
     BSD, ISC, Unlicense)
   - Weak copyleft (LGPL, MPL, EPL) requires founder approval
   - Strong copyleft (GPL, AGPL, SSPL) is PROHIBITED in production code
   - Tools and build dependencies are generally OK regardless of license

4. Compliance Steps
   Before adding a new dependency:
   1. Check the license
   2. Verify it's in our approved list
   3. If not approved, submit for review with:
      - Package name and version
      - License
      - Purpose (why we need it)
   
   When we release/deploy:
   1. Run license checker (FOSSA or license-checker)
   2. Verify no prohibited licenses
   3. Update NOTICE file if needed

5. Attribution
   - We maintain a NOTICE file in our repository
   - All permissive licenses requiring attribution are listed
   - We include attribution in our application when practical

6. Violations
   - Accidental inclusion of prohibited license: Remove immediately, audit
     for contamination
   - Willful violation: Disciplinary action up to termination
   - Found in due diligence: Remediate before acquisition/investment
```

## Open Source Auditing Before an Exit

When preparing for acquisition or investment, expect a thorough open source audit:

**What auditors look for:**
- Complete dependency list
- License for every dependency
- No GPL/AGPL/SSPL in proprietary code
- Proper attribution (NOTICE file)
- CLAs for all contributors
- Clean code (no copy-pasted code without attribution)

**Acquisition horror stories:**
- **Acquisition blocked** because of GPL contamination affecting entire codebase
- **Acquisition price reduced** because remediation is expensive
- **Investment delayed** while compliance is sorted out

**How to prepare:**
1. Run a full license audit now (don't wait for due diligence)
2. Remediate any issues (replace, remove, or isolate problematic dependencies)
3. Document everything
4. Have a clean bill of health ready

## Resources

- [Choose a License](https://choosealicense.com/) — Great resource for choosing your own license
- [TLDRLegal](https://tldrlegal.com/) — Plain-English license summaries
- [FOSSA Blog](https://fossa.com/blog) — Open source compliance best practices
- [SPDX License List](https://spdx.org/licenses/) — Standard license identifiers
- [GitHub License API](https://docs.github.com/en/rest/licenses) — Programmatic license checking
- [Open Source Initiative (OSI)](https://opensource.org/licenses) — Approved license list
- [GNU License List](https://www.gnu.org/licenses/license-list.html) — GNU license explanations
- [FOSSA Free Plan](https://fossa.com/pricing) — Free for public repos
- [Snyk Free Tier](https://snyk.io/plans/) — Free vulnerability + license scanning
