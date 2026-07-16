# Curation Rubric

Use this reference to classify extracted material, decide whether to update or create a page, and report evidence without turning source notes into a mirror.

## 1. Evidence Record

For each important claim, capture:

| Field | Meaning |
| --- | --- |
| Claim ID | Stable identifier within the analysis |
| Statement | Concise paraphrase |
| Provenance | External fact, author conclusion, user result, user judgment, or Agent inference |
| Source tier | Primary paper, official project/repository, secondary synthesis, user record, or Agent-generated material |
| Source location | File, page, section, table, figure, DOI, URL, or CiteKey |
| Version and date | Dataset/release version, document date, and source access date when changeable |
| Scope | Dataset version, task, environment, split, metric, or stated condition |
| Confidence | Confirmed, partially supported, conflicting, or `待验证` |
| Candidate object | Page or object that could consume this evidence |

Do not silently fill missing fields from general knowledge. If additional verification uses another source, record it separately.

## 2. Object Boundary Tests

| Object | Use when the page answers | Do not use as |
| --- | --- | --- |
| `concept` | What is this term or principle, and how is it distinguished? | A container for one paper's notes |
| `topic` | What research problem or task is being studied, with what boundaries and open questions? | A broad directory label without a research question |
| `method` | What does this approach do, what are its inputs, assumptions, steps, outputs, and limitations? | A list of unrelated algorithms |
| `dataset` | What data exists, under which version/license/split/coordinate/annotation conditions? | A generic list of dataset names |
| `metric` | What is measured, how is it calculated and aggregated, and when are values comparable? | A result table without definition |
| `paper` | What did one publication claim, test, report, and omit? | The final home of every concept from the paper |
| `survey` | What body of sources was selected, by which scope and synthesis method? | An unsourced narrative summary |
| `experiment` | What did the user actually run, under which versions/configuration, with what result? | A paper's reported experiment |
| `project` | What real effort has goals, scope, milestones, resources, experiments, and decisions? | A stable technical concept |
| `decision` | Which option was chosen for a real problem, and why? | General comparison without a decision |
| `guide` | Which verified steps can be repeated, with prerequisites and validation? | Unverified command history |
| `troubleshooting` | Which symptom was diagnosed and verified through a reproducible process? | A list of unrelated errors |
| `reference` | Which compact facts, commands, terms, or resources need quick lookup? | A full explanatory tutorial |
| `article` | Which ideas form a reader-oriented narrative output? | The canonical source of underlying knowledge |

The repository currently supports `topic`, `metric`, and `survey`. Recheck the current Schema, templates, and checker before every implementation rather than relying on this reference alone.

For data-related material, keep these concepts separate:

- **dataset or collection**: the underlying released data;
- **benchmark**: a task and comparison setting defined on data;
- **protocol**: train/validation/test splits, query/gallery roles, metrics, and evaluation rules;
- **derived subset or release**: a versioned selection or packaging of the data.

One resource may support several tasks, so a report's categories are often overlapping analytical views rather than a permanent ontology.

## 3. Update, Create, Retain, or Defer

### Update an existing page

Choose update when:

- the same object already exists under the same official name, alias, abbreviation, or translation;
- the new evidence extends the same definition and page purpose;
- differences can be expressed as versions, variants, scopes, or source disagreements inside one page.

### Create a new page

Recommend creation only when:

- the object has a stable name and responsibility;
- it has enough verified substance for multiple meaningful sections;
- it is likely to receive evidence or use beyond one transient note;
- no existing page can absorb it without mixing responsibilities;
- the current Schema and template support it, or the prerequisite migration is explicitly approved.

### Retain as evidence only

Use this outcome when the material supports another object but does not justify its own page, such as a single numeric result, a short implementation detail, or a report classification that requires external confirmation.

### Defer

Defer when the source is unreadable, provenance is unclear, names are ambiguous, licensing is unknown, claims conflict, or the object boundary is unstable.

## 4. Research Material Example

A UAV visual-localization dataset report may yield:

- one candidate research topic for UAV absolute visual localization;
- several candidate dataset objects, each requiring official-source verification;
- metric candidates that define localization, retrieval, pose, or geospatial error;
- method links for retrieval, local matching, geometric verification, and pose estimation;
- a report-level source record only if the report itself must remain traceable.

Do not accept a dataset count, scale, license, coordinate system, or split solely because it appears in a secondary report. Mark official verification needs explicitly.

For each dataset candidate, record independently when available:

- official name, aliases, paper, DOI, and maintained project URL;
- source tier, access date, release/version, dataset license, code license, publication copyright, and download mechanism as separate fields;
- task and protocol, including query/gallery or sequence organization;
- data nature, modalities, sensors, map products, coordinate systems, and ground truth;
- image/frame count, sequence/trajectory count, spatial coverage, duration, distance, location count, and sampling unit as separate fields;
- train/validation/test split and whether scenes, locations, or trajectories overlap;
- official limitations, known discrepancies, and values that remain `待验证`.

Never compare a training-image count with a whole-dataset count, a place count with a trajectory count, or a route length with spatial area without explicitly naming the unit and scope.

When an official page and a secondary report disagree, retain a discrepancy record such as “report value observed on date A; official project value observed on date B.” Do not silently overwrite either value until the release or counting definition is known.

A secondary report does not automatically need a formal `paper` page or a BibTeX entry. Preserve DOI, CiteKey, or BibTeX when a publication is itself a tracked evidence object; for a user report, file path, title, date, page location, and its cited primary sources are normally sufficient during analysis.

A public download link does not prove that reuse, redistribution, or publication is permitted. Likewise, an MIT or Apache license in a code repository normally covers code only unless the authors explicitly extend it to the dataset. Record an unknown dataset license as `待验证` rather than copying the code license.

## 5. Programming and Algorithm Material Example

Go syntax or algorithms and data structures use the same workflow but different objects:

- language rules and data-structure definitions usually become `concept` pages;
- a concrete algorithm with inputs, steps, complexity, correctness conditions, and limitations can be a `method` page;
- a verified Go implementation workflow can be a `guide`;
- benchmark results belong to an `experiment`;
- a compact syntax or standard-library lookup may be a `reference`.

Do not create one page for every code snippet or exercise. Extract reusable rules, common failure modes, complexity facts, and implementation tradeoffs.

## 6. Analysis Output Template

```text
## Source status
- Path, format, metadata, extraction method, limitations

## Material structure
- Sections, tables, figures, and scope

## Evidence-backed findings
- Claim ID, summary, provenance, source location, confidence

## Candidate knowledge objects
- Object, proposed outcome, existing page or proposed location, rationale

## Verification gaps
- Missing official source, conflicting number, unclear license/version/split

## Version and discrepancy log
- Conflicting value, source tier, observed version/date, and required resolution

## Decisions requiring the user
- Only decisions that cannot be resolved from repository or source evidence

## Skill gap review
- Issue, reusable?, severity, proposed home, change made or proposed
```

## 7. Skill Gap Review

Classify gaps before changing the Skill:

| Gap type | Default action |
| --- | --- |
| Safety, privacy, source corruption, or fact-boundary risk | Fix immediately when Skill improvement is authorized |
| Repeated workflow ambiguity | Add a concise rule to `SKILL.md` |
| Detailed domain decision or reusable example | Add to `references/` |
| Mechanical check repeated across tasks | Consider a small script only after the workflow stabilizes |
| Repository-wide governance | Propose or update `AGENTS.md` |
| Project architecture or roadmap | Propose or update the project overview |
| Quartz/Markdown presentation rule | Propose or update the content and layout guide |
| One-off wording or taste | Record but do not hard-code |

After any Skill change, validate structure and re-run the scenario that exposed the gap when practical.
