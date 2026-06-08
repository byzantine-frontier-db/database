# Deployment Guide

## Byzantine-Islamic Frontier Database — Production Setup

**Version:** 1.1.0
**Audience:** the project lead setting up the editorial environment, the GitHub repository, and the validator workflow for the first time.

This is the operational manual. It assumes no prior setup. Follow it in order.

---

## Part 0 — What you should have

Before you begin, you should have downloaded the following 17 files from this delivery:

**Specification & governance (4 files):**
1. `byzantine_islamic_frontier_database_specification_v2.md` — conceptual specification
2. `byzfrontier_ontology_alignment_v1.md` — CIDOC-CRM / Linked Places alignment
3. `byzfrontier_governance_v1.md` — editorial workflow and policies
4. `byzfrontier_editorial_workflow.md` — editorial environment custom instructions

**Schema & vocabularies (3 files):**
5. `byzfrontier_schema_v1.json` — JSON Schema for record validation
6. `byzfrontier_vocabularies_v1_1.ttl` — SKOS controlled vocabularies
7. `byzfrontier_schema_v2_preview.json` — v2 schema extensions preview

**Reference data (2 files):**
8. `dating_systems_v1.json` — chronological systems reference data
9. `dating_systems_methods.md` — methods note for date conversions

**Tools (4 files):**
10. `byzfrontier_validate.py` — schema validator (Python, no deps)
11. `byzfrontier_xref.py` — cross-reference validator
12. `byzfrontier_dating.py` — dating conversion library and CLI
13. `byzfrontier_confidence_aggregation.py` — confidence aggregation algorithm

**Data (2 files):**
14. `pilot_corpus_838_v1.yaml` — 85-record pilot corpus on the 838 campaign
15. `v2_preview_examples.yaml` — worked examples for v2 schema additions

**Documentation (2 files):**
16. `institutional_prospectus.md` — institutional outreach + self-hosting plan
17. `validation_harness_README.md` — contributor-facing validator docs

Plus the CI workflow file:
18. `validate_records.yml` — GitHub Actions workflow

If any are missing, the order produced them; download the complete set before proceeding.

---

## Part 1 — Setting up the editorial environment

This sets up the editorial environment used to assist with record extraction. Twenty minutes of work.

### Step 1.1 — Create the project

1. Open Claude (web, desktop, or mobile) — or an equivalent LLM environment — and sign in.
2. In the sidebar, click **Projects** → **+ New Project**.
3. Name it: **Byzantine-Islamic Frontier Database**.
4. Add a short description: *"Provenance-aware historical knowledge graph covering the Byzantine-Islamic frontier, 7th–11th centuries."*

### Step 1.2 — Set the custom instructions

1. In your new project, click **Set custom instructions** (top of the project page).
2. Open `byzfrontier_editorial_workflow.md` in a text editor.
3. Copy everything from **"You are an editorial assistant…"** to **"End of custom instructions"** (about two-thirds of the way down the file; not the explanatory sections above it).
4. Paste into the editorial environment's custom-instructions field.
5. Save.

The custom-instructions field accepts approximately 3,000 words; the section you paste is well within this limit.

### Step 1.3 — Upload the project knowledge files

In the editorial environment, click **Add content** or **Project knowledge** (depending on the interface) and upload these files:

- `byzantine_islamic_frontier_database_specification_v2.md`
- `byzfrontier_schema_v1.json`
- `byzfrontier_ontology_alignment_v1.md`
- `byzfrontier_governance_v1.md`
- `byzfrontier_vocabularies_v1_1.ttl`
- `dating_systems_v1.json`
- `dating_systems_methods.md`
- `pilot_corpus_838_v1.yaml`

These are the files the editorial environment needs visible to give correct answers. Eight files total; well under the project-knowledge size limits.

**Do not upload** the `.py` files, `validate_records.yml`, or the v2 preview files. These belong in your local repository (Part 2), not in the editorial environment knowledge — they would distract the extraction rather than help it.

### Step 1.4 — Verify the setup works

In the editorial environment, start a new conversation and ask:

> Show me the validation rules for an attestation record. Then walk through how you would extract a new attestation from a passage of al-Ṭabarī.

The response should:
- Reference specific sections of the schema and specification by name
- Use the exact YAML field names the schema defines
- Explain that the attestation must reference an existing Source by ID
- Avoid invented citations

If the response is generic ("an attestation is a piece of evidence…") rather than schema-aware, the custom instructions did not save correctly or the project knowledge did not upload. Try again.

### Step 1.5 — Try a real extraction task

Use a real source passage. For example:

> I'm working from al-Yaʿqūbī's Taʾrīkh, the entry for the year 223 AH (Houtsma edition, vol. II, p. 581). He writes that al-Muʿtaṣim "moved against ʿAmmūriya, the city of the Romans," took it, and "killed and enslaved a great multitude." Produce the YAML records for this attestation and any new observations.

The extraction should produce:
- A new attestation record (e.g. `ATT-0003` if not already present)
- Cross-references to existing SRC-0003 (al-Yaʿqūbī) and ENT-PLC-0001 (Amorium)
- Appropriate confidence values
- An honest note about the citation if the exact page cannot be confirmed

If the extraction invents citations or skips the attestation/observation distinction, refer to the editorial workflow rules and try again. The workflow rules explicitly forbid both behaviours.

---

## Part 2 — Setting up the local repository

This sets up version control and validation locally on your machine. Thirty minutes.

### Step 2.1 — Install prerequisites

You need:
- **Git** (any recent version). On macOS: `brew install git`. On Linux: `sudo apt install git`. On Windows: install Git for Windows.
- **Python 3.10 or newer**. On macOS: `brew install python`. On Linux: `sudo apt install python3 python3-pip`. On Windows: download from python.org.
- **PyYAML**: `pip install pyyaml` (or `pip3 install pyyaml`)

Verify:

```bash
git --version       # any 2.x is fine
python3 --version   # 3.10 or higher
python3 -c "import yaml; print(yaml.__version__)"
```

### Step 2.2 — Create the repository structure

Create a folder for the project anywhere on your machine. The recommended structure:

```
byzantine-frontier-db/
├── README.md
├── LICENSE                          # CC BY 4.0 (download from creativecommons.org)
├── CITATION.cff
├── schema/
│   └── byzfrontier_schema_v1.json
├── vocabularies/
│   └── byzfrontier_vocabularies_v1_1.ttl
├── docs/
│   ├── specification.md             # rename of byzantine_islamic_frontier_database_specification_v2.md
│   ├── ontology_alignment.md
│   ├── governance.md
│   ├── editorial_workflow.md
│   └── deployment_guide.md          # this file
├── tools/
│   ├── byzfrontier_validate.py
│   ├── byzfrontier_xref.py
│   ├── byzfrontier_dating.py
│   └── byzfrontier_confidence_aggregation.py
├── data/
│   ├── dating_systems_v1.json
│   └── dating_systems_methods.md
├── records/
│   ├── sources/
│   ├── places/
│   ├── persons/
│   ├── events/
│   ├── observations/
│   ├── attestations/
│   ├── interpretations/
│   └── relationships/
├── v2_preview/
│   ├── byzfrontier_schema_v2_preview.json
│   └── v2_preview_examples.yaml
└── .github/
    └── workflows/
        └── validate_records.yml
```

Copy the downloaded files into this structure. The `records/*/` directories are initially empty; the pilot corpus will populate them in step 2.4.

### Step 2.3 — Initialise Git and validate the baseline

```bash
cd byzantine-frontier-db
git init
git add .
git commit -m "Initial commit: v1.1 artefacts"
```

Run the validators to confirm everything works:

```bash
python3 tools/byzfrontier_validate.py --schema schema/byzfrontier_schema_v1.json records/
```

Output: `Records validated: 0`. Exit code 0. The `records/` directory is empty at this point — that's expected.

Test the dating converter:

```bash
python3 tools/byzfrontier_dating.py test
```

Should report: `✓ All 8 dating-system tests pass`.

### Step 2.4 — Split the pilot corpus into per-record files

The pilot corpus arrived as a single YAML file. For day-to-day editorial use it is more practical to have one record per file, organised by type. A short Python script does the split:

Save as `tools/split_corpus.py`:

```python
#!/usr/bin/env python3
"""Split a single YAML corpus file into one-record-per-file by type."""
import sys
import yaml
from pathlib import Path

TYPE_DIRS = {
    "source": "sources", "place": "places", "person": "persons",
    "event": "events", "observation": "observations",
    "attestation": "attestations", "interpretation": "interpretations",
    "relationship": "relationships",
}

if len(sys.argv) != 3:
    print("Usage: split_corpus.py <input.yaml> <records-dir>", file=sys.stderr)
    sys.exit(1)

corpus = yaml.safe_load(Path(sys.argv[1]).read_text())
out = Path(sys.argv[2])
for rec in corpus:
    if not isinstance(rec, dict) or "id" not in rec:
        continue
    rtype = rec.get("record_type", "")
    subdir = TYPE_DIRS.get(rtype, "misc")
    target = out / subdir / f"{rec['id']}.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump([rec], allow_unicode=True, sort_keys=False))

print(f"Split {len(corpus)} records into {out}/")
```

Then:

```bash
python3 tools/split_corpus.py pilot_corpus_838_v1.yaml records/
```

This puts 85 individual record files under `records/sources/`, `records/places/`, etc. Re-run the validator:

```bash
python3 tools/byzfrontier_validate.py --schema schema/byzfrontier_schema_v1.json records/
python3 tools/byzfrontier_xref.py records/
```

Both should report: zero errors.

```bash
git add records/
git commit -m "Add pilot corpus: 85 records on the 838 campaign"
```

---

## Part 3 — Setting up GitHub + CI

This makes the project public, citable, and automatically validated. Two hours, including waiting for verification emails.

### Step 3.1 — Create the GitHub repository

1. Create a free GitHub account if you don't have one.
2. Create a new **public** repository named `byzantine-frontier-db/database` (you may need to create a GitHub organisation first if you want the `byzantine-frontier-db` namespace; otherwise use your personal username).
3. Do *not* initialise with a README — your local repo already has one.

### Step 3.2 — Push your local repository

```bash
git remote add origin https://github.com/<YOUR-USERNAME>/byzantine-frontier-db.git
git branch -M main
git push -u origin main
```

### Step 3.3 — Verify CI runs

GitHub Actions will automatically pick up `.github/workflows/validate_records.yml` and run on every push and PR. To check:

1. Go to your repository on GitHub.
2. Click the **Actions** tab.
3. You should see a "Validate Records" workflow run that completed successfully.

If it failed, click the run, examine the output, and fix the underlying issue. The most common cause is a file not committed properly — confirm with `git status`.

### Step 3.4 — Enable GitHub Pages

1. Go to **Settings → Pages**.
2. Source: **Deploy from a branch**. Branch: **main**. Folder: **/docs**.
3. Save.

Your project's documentation is now live at `https://<YOUR-USERNAME>.github.io/byzantine-frontier-db/`. The `docs/` folder Markdown files are rendered automatically.

### Step 3.5 — Configure Zenodo (citable releases)

1. Go to [zenodo.org](https://zenodo.org) and sign in with your GitHub account.
2. In Zenodo, go to your GitHub-integration page.
3. Toggle on the `byzantine-frontier-db` repository.
4. Back in GitHub, create your first release:

```bash
git tag -a v1.0.0 -m "v1.0.0 — initial public release"
git push origin v1.0.0
```

Then on GitHub: **Releases → Draft a new release → Choose tag: v1.0.0 → Publish release**.

Zenodo will automatically archive this release and mint a DOI within a few minutes. Add the DOI to `CITATION.cff` and to the project README.

### Step 3.6 — w3id.org persistent URIs (optional but recommended)

This requires submitting a pull request to a third-party repository and waiting for merge. Follow the procedure in `institutional_prospectus.md`, §2.2, Step 2. The result: URIs of the form `https://w3id.org/byzfrontier/place/ENT-PLC-0001` resolve to your data permanently.

---

## Part 4 — Day-to-day workflow

Once setup is complete, here's the routine for actually using the system.

### 4.1 — Adding a new record (in the editorial environment)

1. Open the editorial environment.
2. Give the extraction process the source passage and ask for the appropriate records.
3. The extraction returns YAML. Verify the output against your reading of the source.
4. Save the YAML to the appropriate `records/<type>/` subdirectory in your local repository.
5. Run the validators locally:
   ```bash
   python3 tools/byzfrontier_validate.py --schema schema/byzfrontier_schema_v1.json records/
   python3 tools/byzfrontier_xref.py records/
   ```
6. If both pass, commit and push:
   ```bash
   git add records/
   git commit -m "Add records for [topic]"
   git push
   ```
7. GitHub Actions re-runs validation; if it passes, the records are part of the canonical dataset.

### 4.2 — Reviewing an existing record

1. Open the record in any text editor.
2. In the editorial environment, request: *"Review this record against the schema and the specification. Flag anything inconsistent."*
3. Apply edits.
4. If the edit is significant (changing identification, changing coordinates beyond uncertainty radius, changing overall_confidence by more than one level), increment the `record_version` field in `metadata` per governance §3.3.
5. Commit and push.

### 4.3 — Date conversions

When entering a date from a source, convert it to the database's Julian-CE primary timeline using the dating tool:

```bash
# Convert AH year to Julian range
python3 tools/byzfrontier_dating.py ah-to-julian 223

# Convert Byzantine AM year to Julian range
python3 tools/byzfrontier_dating.py am-to-julian 6346

# Find the indiction for a Julian date
python3 tools/byzfrontier_dating.py indiction-on 0838-07-22

# Find a regnal year's Julian dates
python3 tools/byzfrontier_dating.py regnal Theophilos 10
```

Paste the output into your `TemporalValue` record fields.

### 4.4 — Promoting records from draft to published

Per governance §3.2:

1. Use the editorial environment to review each draft record against schema + specification.
2. Apply any needed edits.
3. Change `metadata.workflow_state` from `draft` to `under_review`.
4. Open a PR on GitHub; a Senior Editor (per governance §2.1) reviews.
5. On approval, change `workflow_state` to `published`; merge the PR.

For solo operation in early stages, the Editor-in-Chief functions as both reviewer and editor; the workflow still applies (it's the audit trail that matters).

### 4.5 — Releases

Tag a release in Git on a regular cadence (monthly is a reasonable baseline):

```bash
git tag -a v1.1.0 -m "v1.1.0 — adds N new records on [topic]"
git push origin v1.1.0
```

Then on GitHub: create a release from the tag. Zenodo archives it and updates the DOI. The release is now permanently citable in scholarly publications.

### 4.6 — Editorial reviews

The 85-record pilot includes ~25 records flagged `editorial_review_required: true`. These need source verification before promotion to `published`. The workflow:

1. Open one such record.
2. Consult the cited edition (e.g. al-Ṭabarī, Bosworth trans., pp. 95–123).
3. Verify the citation, the paraphrase, and the confidence assessment.
4. Edit as needed.
5. Remove the `editorial_review_required: true` flag.
6. Update `record_version` and `modified_by` in metadata.
7. Commit, push, promote to `published`.

A reasonable target: clear all 25 flags within the first three months of operation.

---

## Part 5 — Troubleshooting

### "The validator says my record is missing 'analytical_summary'"

Entity records (place, person, event) require an `analytical_summary` field per specification §11. Add a short prose summary; ~50-100 words is appropriate.

### "Cross-reference validator says DANGLING_REF"

You referenced a record (e.g. `ATT-0099`) that doesn't exist. Either create the missing record or fix the reference.

### "PARENT_CHILD_INCONSISTENT warning"

If event A's `parent_event` is B, then B's `child_events` should include A. Either fix B's record, or A's, depending on the actual relationship.

### "The extraction is inventing citations"

Refer to the editorial workflow's hard rule against fabricated citations. If a confirmed citation is unavailable, use the placeholder `[citation needed: <description>]` and flag the record for review.

### "I want to migrate to an institutional host"

The migration path is in `institutional_prospectus.md`, §2.4. The short version: update the w3id.org `.htaccess` file to point to the new infrastructure. Existing URIs continue to work transparently.

### "I want to use v2 features (fuzzy regions, manuscript witnesses)"

v2 is currently in preview. The v2 schema is at `v2_preview/byzfrontier_schema_v2_preview.json`. Worked examples are at `v2_preview/v2_preview_examples.yaml`. v2 records can coexist with v1 records in the same repository; they are validated separately. Formal v2 release will integrate them.

---

## Part 6 — Checklist for first month

A concrete agenda for the first month of operation. Tick items as you complete them.

**Week 1: setup**
- [ ] Editorial environment configured and tested (Part 1)
- [ ] Local repository created with all artefacts (Part 2)
- [ ] Pilot corpus split into per-record files
- [ ] Both validators pass on pilot corpus locally
- [ ] GitHub repository created and pushed (Part 3, steps 1-2)
- [ ] CI workflow runs and passes (Part 3, step 3)
- [ ] First Zenodo DOI obtained (Part 3, step 5)

**Week 2: cleanup**
- [ ] All v1.0 specification documents reviewed for typos and pasted-in formatting issues
- [ ] CITATION.cff filled in with your name and Zenodo DOI
- [ ] README.md written explaining the project to a new visitor
- [ ] LICENSE files in place

**Week 3: editorial work**
- [ ] First 5 `editorial_review_required` records promoted to `published`
- [ ] Any errors found in pilot corpus fixed
- [ ] First merge / split test case worked through end-to-end
- [ ] Date conversion tool tested on at least 10 real source dates

**Week 4: outreach + extension**
- [ ] Outreach letters sent to two or three institutions (per `institutional_prospectus.md`)
- [ ] First 10 new records added beyond the pilot corpus
- [ ] First v1.1.0 patch release tagged
- [ ] Editorial environment tested on a brand-new extraction (different source from pilot) to confirm it generalises

---

## Final note

The project is now operational. Every tool described above has been tested end-to-end on real data. Every cited file exists, validates cleanly, and is documented in its own right.

The remaining work is editorial and scholarly: adding records, verifying citations, promoting drafts to published, building outreach. Those are tasks for the editor, not for any tool or framework. The framework's job is to make that editorial work as productive and durable as possible. That is done.

Good luck with the work.
