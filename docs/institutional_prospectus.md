# Institutional Hosting Prospectus and Self-Hosting Fallback

## Byzantine-Islamic Frontier Database

This document supports two parallel tracks:

1. **Institutional outreach** — for identifying and approaching a university, digital-humanities centre, or learned society to host the database long-term.
2. **Self-hosting fallback** — for operating the database immediately without an institutional host, using free public infrastructure that provides persistent URIs, version control, citable releases, and basic web presence.

Both tracks can run in parallel. The self-hosting fallback gets the project working tomorrow; the institutional track addresses the long-term sustainability concerns the governance charter assumes.

---

## Part 1 — Institutional Hosting Prospectus

### 1.1 What "hosting" actually requires

The governance charter and ontology alignment document together assume:

- **Persistent URIs** under a stable domain (`byzantine-frontier-db.org` or equivalent)
- **Version-controlled record storage** (a Git repository with backup)
- **A read-only HTTP API** exposing records by URI
- **A SPARQL endpoint** (target v1.1)
- **Bulk-export availability** (data dumps per release)
- **Editorial continuity** beyond any single contributor
- **Long-term archival commitment** (decades, not years)

None of these individually is expensive. The institutional component is the **commitment to maintain them** across staff transitions, funding cycles, and infrastructure changes.

### 1.2 Target institutions

The institutions most plausibly equipped and motivated to host:

**Digital-humanities centres with relevant programmes:**

- **King's College London — Department of Digital Humanities and the Centre for Hellenic Studies.** Home of the Prosopography of the Byzantine World (PBW). Existing relationships with Byzantine-studies infrastructure projects.
- **Berlin-Brandenburgische Akademie der Wissenschaften (BBAW).** Hosts the Prosopographie der mittelbyzantinischen Zeit (PMBZ). Direct prosopographical alignment.
- **Institute for the Study of the Ancient World (ISAW), New York University.** Hosts Pleiades, the foundational gazetteer of the ancient world. Existing Linked Pasts infrastructure.
- **Pisa Digital Humanities (e.g. through the Scuola Normale Superiore).** Active in computational classical and medieval studies.
- **University of Vienna — Institute for Medieval Research (IMAFO).** Hosts Tabula Imperii Byzantini and related Byzantine-geography projects.
- **The British Library Digital Scholarship.** Hosts comparable cultural-heritage data projects with persistent infrastructure.

**Learned societies:**

- **Society for the Promotion of Byzantine Studies (UK).**
- **Association internationale des études byzantines.**
- **Middle East Medievalists.**

**Research consortia:**

- **The Linked Pasts community** (informally associated with Pelagios/WHG).
- **DARIAH-EU** (Digital Research Infrastructure for the Arts and Humanities).

### 1.3 Outreach package

When approaching a candidate host, present:

1. **This document** (the prospectus + fallback).
2. **The four v1.0 artefacts**: specification, schema, ontology alignment, governance charter.
3. **The pilot corpus** demonstrating the system working end-to-end on a substantial test case.
4. **An ask sized to the institution**: hosting commitment may be as light as a sub-domain and a GitHub mirror with periodic snapshots, or as substantial as full editorial board representation. Tailor the ask.

### 1.4 Draft outreach letter

> Dear [Director / Programme Lead],
>
> I am writing to seek your institution's interest in hosting the Byzantine-Islamic Frontier Database, a provenance-aware historical knowledge graph covering the Byzantine-Islamic frontier between the seventh and eleventh centuries.
>
> The project has reached v1.0 in terms of specification, schema, vocabulary publication, and governance, with a working pilot corpus of approximately 85 records on the Abbasid campaign of 838. The full v1.0 documentation set is attached. The system is CIDOC-CRM aligned, validates cleanly against a published JSON Schema, exports to Linked Places format, and integrates with Pleiades, PMBZ, and VIAF for external identifiers.
>
> What the project needs now is institutional hosting: a stable URI domain, version-controlled storage with backup, and editorial continuity. The technical infrastructure requirements are modest; the substantive commitment is editorial sustainability across staff transitions.
>
> [Institution] would be a natural fit because [specific reason: existing programme on Byzantine prosopography / hosting of comparable infrastructure / regional scholarship]. I would welcome a conversation about whether and how this could be developed.
>
> The project's intellectual model and editorial governance are documented in the attached charter; the technical artefacts are released under CC BY 4.0 (data), CC0 (schemas/vocabularies), and Apache 2.0 (code) so that hosting does not create rights complications.
>
> Yours sincerely,
> [Name]

### 1.5 What to ask for, in order of preference

1. **Full hosting + editorial integration.** Domain, infrastructure, editorial board seat, long-term commitment.
2. **Hosting + mirror.** Domain and infrastructure; editorial board remains independent.
3. **Mirror only.** Periodic snapshots of the database hosted by the institution as a preservation backup; primary URIs remain elsewhere.
4. **Endorsement.** Public scholarly endorsement without infrastructure commitment, useful for raising the project's standing and attracting other contributors.

A no-response or polite decline is the most common outcome of cold outreach; the self-hosting fallback (Part 2) means the project continues regardless.

---

## Part 2 — Self-Hosting Fallback

This setup gets the project fully operational, with persistent URIs and citable releases, using only free public infrastructure. No institutional host required.

### 2.1 Stack overview

| Need | Tool | Cost | Persistence |
|---|---|---|---|
| Version-controlled record storage | **GitHub** (public repository) | Free | Indefinite |
| Persistent URIs (Cool URIs) | **w3id.org** (W3C permanent ID community service) | Free | Long-term |
| Citable releases with DOIs | **Zenodo** (CERN-hosted research data archive) | Free | Long-term (CERN commitment) |
| Web presence + simple API | **GitHub Pages** (static site, served from repo) | Free | Indefinite |
| Continuous integration | **GitHub Actions** | Free for public repos | Indefinite |
| Long-term preservation backup | **Software Heritage** (auto-archives public GitHub repos) | Free | Long-term |
| Linked Places mirror | Optionally submit place data to **World-Historical Gazetteer** | Free | Long-term |

This combination gives the project everything required by the governance charter's "interoperability commitments" (§8) without any institutional hosting.

### 2.2 Setting it up step-by-step

#### Step 1: Create the GitHub repository

Create a public GitHub organisation (e.g. `byzantine-frontier-db`) and a single primary repository within it (e.g. `byzantine-frontier-db/database`).

Repository structure:

```
byzantine-frontier-db/
├── README.md
├── LICENSE                            # CC BY 4.0
├── LICENSE-CODE                       # Apache 2.0 (for scripts)
├── LICENSE-VOCAB                      # CC0 (for vocabularies)
├── CITATION.cff                       # standard citation file
├── schema/
│   └── byzfrontier_schema_v1.json
├── vocabularies/
│   └── byzfrontier_vocabularies_v1_1.ttl
├── records/
│   ├── sources/
│   ├── places/
│   ├── persons/
│   ├── events/
│   ├── observations/
│   ├── attestations/
│   ├── interpretations/
│   └── relationships/
├── docs/
│   ├── specification.md
│   ├── ontology_alignment.md
│   ├── governance.md
│   └── deployment_guide.md
├── tools/
│   ├── byzfrontier_validate.py
│   ├── byzfrontier_xref.py
│   ├── byzfrontier_dating.py
│   └── byzfrontier_confidence_aggregation.py
├── data/
│   ├── dating_systems_v1.json
│   └── dating_systems_methods.md
├── .github/workflows/
│   ├── validate_records.yml
│   └── publish_release.yml
└── exports/                           # auto-generated on release
    ├── full_dump.json
    ├── places.lpf.json                # Linked Places Format
    └── records.ttl                    # CIDOC-CRM RDF
```

#### Step 2: Configure w3id.org for persistent URIs

[w3id.org](https://w3id.org) is a free W3C Permanent Identifier Community Group service that provides redirect-based persistent URIs. To set up:

1. Fork the [perma-id/w3id.org](https://github.com/perma-id/w3id.org) GitHub repository.
2. Add a directory `byzfrontier/` containing an `.htaccess` file that redirects URI paths to the actual content location.

Example `.htaccess` content:

```apache
Options +FollowSymLinks
RewriteEngine On

# Schema
RewriteRule ^schema/v1\.0\.0/?$ https://byzantine-frontier-db.github.io/database/schema/byzfrontier_schema_v1.json [R=302,L]

# Vocabularies
RewriteRule ^vocab/v1\.1\.0/?$ https://byzantine-frontier-db.github.io/database/vocabularies/byzfrontier_vocabularies_v1_1.ttl [R=302,L]

# Place records
RewriteRule ^place/(.+)$ https://byzantine-frontier-db.github.io/database/records/places/$1.yaml [R=302,L]

# Person records
RewriteRule ^person/(.+)$ https://byzantine-frontier-db.github.io/database/records/persons/$1.yaml [R=302,L]

# Source records
RewriteRule ^source/(.+)$ https://byzantine-frontier-db.github.io/database/records/sources/$1.yaml [R=302,L]

# Event records  
RewriteRule ^event/(.+)$ https://byzantine-frontier-db.github.io/database/records/events/$1.yaml [R=302,L]
```

3. Submit a pull request to perma-id/w3id.org for review.

Once merged, URIs of the form `https://w3id.org/byzfrontier/place/ENT-PLC-0001` will resolve persistently. If the project later migrates to an institutional host, only the `.htaccess` file changes; existing URIs continue to work.

#### Step 3: Set up GitHub Pages

Enable GitHub Pages on the repository (Settings → Pages → source: `main` branch, `/docs` folder, or use the GitHub Actions Pages workflow).

Place a `index.md` in `docs/` with the project overview. The site will be available at `https://byzantine-frontier-db.github.io/database/` and acts as the project's public web presence and read-only access layer.

#### Step 4: Configure Zenodo integration for citable releases

1. Sign in to [Zenodo](https://zenodo.org) with your GitHub account.
2. In the Zenodo GitHub integration page, enable the project repository.
3. Create a v1.0 release on GitHub (`git tag v1.0.0; git push --tags`); GitHub publishes; Zenodo archives the release and mints a DOI.
4. The DOI is then citable as a persistent reference to that exact version of the database.

CITATION.cff:

```yaml
cff-version: 1.2.0
title: "Byzantine-Islamic Frontier Database"
type: dataset
authors:
  - given-names: "[Lead editor]"
    family-names: "[Family name]"
license: CC-BY-4.0
repository-code: "https://github.com/byzantine-frontier-db/database"
url: "https://w3id.org/byzfrontier/"
keywords:
  - Byzantine studies
  - Islamic history
  - historical GIS
  - prosopography
  - linked open data
identifiers:
  - type: doi
    value: "[assigned by Zenodo on first release]"
```

#### Step 5: Set up CI validation

Place the validator workflow at `.github/workflows/validate_records.yml` (already produced in v1.0). On every pull request that touches records, schema, or validator, the workflow runs both the schema validator and the cross-reference validator. Failed validation blocks merge.

#### Step 6: Set up release-export pipeline

A second workflow auto-generates exports on every release:

```yaml
name: Publish release exports
on:
  release:
    types: [created]
jobs:
  export:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install pyyaml
      - name: Generate full JSON dump
        run: python tools/export_full.py records/ > exports/full_dump.json
      - name: Generate Linked Places Format export
        run: python tools/export_lpf.py records/places/ > exports/places.lpf.json
      - name: Generate CIDOC-CRM Turtle export
        run: python tools/export_crm.py records/ > exports/records.ttl
      - uses: actions/upload-release-asset@v1
        # (attaches the export files to the GitHub release)
```

#### Step 7: Submit place data to World-Historical Gazetteer

For places: convert place records to Linked Places Format (per ontology alignment §4.2) and submit to [World-Historical Gazetteer](https://whgazetteer.org/) for ingestion. WHG provides additional discoverability and a second persistent home for the place layer.

#### Step 8: Register with Software Heritage

Software Heritage automatically archives public GitHub repositories. To accelerate inclusion, you can manually request a save: visit `https://archive.softwareheritage.org/save/` and submit the repository URL. Once archived, each commit gets a SWHID (Software Heritage IDentifier) that persists independently of GitHub.

### 2.3 Costs

For a project of v1.0 size and pilot-corpus volume, the entire self-hosting stack costs **zero**.

If volume grows substantially (tens of thousands of records, sustained API traffic), upgrading to a paid tier of one of the following may become necessary, but each step is incremental:

- GitHub paid plan for larger storage / private collaborators (~$4/user/month).
- A dedicated domain (`byzfrontier.org`) instead of `w3id.org` paths (~$15/year).
- A cheap VPS for a SPARQL endpoint (~$5/month).

### 2.4 The migration path

When an institutional host is identified later, migration is one operation: update the w3id.org `.htaccess` file to point to the new institutional URIs. Every existing record reference continues to resolve transparently. The project never has a broken-URI period.

---

## Part 3 — Timeline

A reasonable timeline for getting from v1.1 (current state) to a fully operational public release:

| Week | Track | Action |
|---|---|---|
| 1 | Self-hosting | Create GitHub org and repository, populate with v1.1 artefacts. |
| 1 | Self-hosting | Submit w3id.org `.htaccess` PR. |
| 1 | Self-hosting | Enable GitHub Pages and Zenodo integration. |
| 2 | Self-hosting | Validate that all v1.1 records pass both validators in CI. Tag v1.0.0 release; obtain Zenodo DOI. |
| 2 | Outreach | Send the outreach letter to two or three best-fit institutions. |
| 3-4 | Self-hosting | Build the release-export pipeline for LPF and CIDOC-CRM RDF. |
| 3-4 | Outreach | Follow up with institutions that responded; prepare brief presentations on request. |
| 5-8 | Pilot publication | Promote the pilot corpus + v1.0 release in relevant scholarly venues (mailing lists, Byzantine-studies bulletins, digital-humanities forums). |
| 5-12 | Editorial work | Move pilot records through editorial review toward `published` state. |
| 8-26 | Institutional | Continue host conversations; aim for at least preliminary institutional commitment within six months. |

If no institutional host is secured within twelve months, the self-hosting setup continues indefinitely; the project remains fully operational on free infrastructure.

---

## Part 4 — Risk register

| Risk | Mitigation |
|---|---|
| No institutional host materialises | Self-hosting fallback (Part 2) covers all operational needs. |
| GitHub or w3id.org policy changes break the URI scheme | Software Heritage archiving + Zenodo DOIs provide independent persistence anchors. |
| Lead editor becomes unavailable | Governance charter §2 documents the succession procedure. The Editorial Board, even if minimal, can continue independently. |
| Contributor base does not grow | The project remains a working framework with a publishable pilot. Even as a single-editor project it is citable infrastructure. |
| Substantive scholarly errors in the pilot corpus | The `editorial_review_required` flag and the published validation are exactly the tools that allow such errors to be corrected publicly and transparently. |
| Schema changes break existing records | Governance §4.6 (versioning + migration paths) addresses this; SemVer commitments ensure breaking changes are signalled. |
