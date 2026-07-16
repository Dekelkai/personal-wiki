---
name: personal-wiki-curator
description: Analyze user-specified papers, PDFs, reports, notes, experiments, programming-study materials, or blog sources and turn them into evidence-backed proposals or approved updates for this personal Wiki. Use when extracting knowledge from external materials, deciding between updating and creating pages, classifying concept/method/dataset/paper/experiment/guide objects, preserving source boundaries, or reviewing and improving this curation workflow after a real task.
---

# Personal Wiki Curator

Use this workflow to separate raw material from formal knowledge, preserve evidence, and keep Obsidian, Git, and Quartz constraints aligned. Default to analysis without repository writes.

## Load Project Rules

Before analyzing content, read these files in order:

1. `AGENTS.md`.
2. `docs/项目总览与路线图.md`.
3. `docs/内容与排版规范.md`.
4. `schemas/frontmatter.schema.json`.
5. The relevant file in `content/_templates/` when proposing or applying a page.
6. Existing pages with the same title, aliases, near-synonyms, object, or research area.
7. `quartz.config.yaml` only when public rendering, links, titles, or publication are relevant.

Treat the Schema and current repository state as executable truth. Report conflicts between the target model and current implementation instead of bypassing validation.

Read `references/curation-rubric.md` when classifying objects, deciding update versus create, structuring analysis output, or conducting the final Skill gap review.

## Select the Mode

Use **analysis mode** unless the user explicitly authorizes Wiki changes.

Analysis mode may:

- read only the source paths explicitly supplied by the user;
- extract text, tables, figures, metadata, claims, and source locations;
- search the repository for related pages;
- propose candidate objects and page changes;
- identify missing evidence and questions for human review.

Analysis mode must not:

- modify the source material or formal Wiki;
- create placeholder pages;
- change `publish`;
- copy full source documents, long excerpts, or screenshots into the repository.

Use **apply mode** only after the user approves specific pages or edits. Apply mode must follow backup, validation, build, and Git rules from `AGENTS.md`.

## Inspect the Source

1. Confirm the path and source role. Convert Windows paths to WSL mount paths when needed.
2. Confirm the file is readable and record filename, format, size, document date, analysis date, and other useful metadata.
3. Use a format-specific reader. For PDFs, extract text and render representative pages when layout, tables, figures, formulas, or OCR quality matter. Visually reconstruct tables that continue across pages instead of trusting flattened text order.
4. When the user supplies equivalent formats of the same material, assign each format a verification role instead of assuming byte-level identity. Use the editable format for headings and tables, the rendered format for pagination and layout, and compare section names, named objects, key values, omissions, and revisions before treating them as the same source version.
5. Check internal consistency before extracting summary facts. Reconcile cover totals, abstract claims, table-row counts, duplicate objects, units, and detailed sections. Preserve unexplained differences as source conflicts rather than selecting the most prominent number.
6. Preserve page, section, table, figure, heading, DOI, URL, CiteKey, or other source locations.
7. Classify each source as primary, official project, secondary synthesis, user record, or Agent-generated material. Record the observed version and access date for changeable project pages and datasets.
8. Record extraction limitations. Mark unreadable, conflicting, incomplete, version-dependent, or unsupported content as `待验证`.
9. Do not scan neighboring private directories unless the user supplied that scope or the task cannot be completed without it.

## Separate Statements by Provenance

Classify each material statement as one of:

- external fact;
- source author conclusion;
- user experiment result;
- user judgment;
- Agent inference.

Never transform an inference into a fact. Never describe a source-reported result as user-reproduced. Preserve uncertainty, scope, units, dataset versions, evaluation settings, and comparison limits.

Treat secondary reports as discovery and synthesis sources. Before applying stable dataset facts such as scale, license, availability, splits, coordinate systems, or ground truth, verify them against the paper, official project page, or maintained dataset repository. When sources disagree, preserve both values with their dates and scopes rather than selecting one silently.

Treat code licensing, dataset licensing, download availability, and publication copyright as separate facts. Never infer a dataset license from the license badge or `LICENSE` file of an accompanying code repository unless the official source explicitly states that it covers the data.

## Identify Knowledge Objects

Decompose the source into candidate objects such as `concept`, `topic`, `method`, `dataset`, `metric`, `paper`, `survey`, `experiment`, `project`, `decision`, `guide`, `troubleshooting`, `reference`, or `article`.

For data resources, distinguish the underlying dataset or collection from its benchmark task, evaluation protocol, derived subset, and current download release. A report's task taxonomy is an analytical view and may overlap; do not turn it into a permanent mutually exclusive hierarchy without evidence from repeated use.

Use the repository Schema before proposing implementation. Do not assume that a type described in project documentation is already supported; when a candidate type is absent, label it as a target-model candidate and identify the required Schema/template/checker alignment.

Do not create one formal page per source by default. A paper or report can support multiple knowledge objects, while a method or dataset page should accumulate evidence from multiple sources.

## Search Before Proposing

Search filenames, Frontmatter titles, aliases, headings, Wiki Links, abbreviations, English names, and Chinese translations.

For each candidate object, choose one outcome:

- update an existing page;
- create a substantive new page;
- retain as source evidence only;
- defer because evidence or object boundaries are insufficient.

Do not use a Wiki Link for a page that does not exist. Do not create an empty page to satisfy a link.

## Report Analysis

In analysis mode, provide:

1. source and extraction status;
2. material scope and document structure;
3. evidence-backed findings with source locations;
4. primary-source verification status and any cross-format, version, total, unit, or count conflicts;
5. candidate knowledge objects;
6. existing pages that could be updated;
7. justified new-page candidates;
8. items retained only as evidence or marked `待验证`;
9. decisions requiring the user;
10. Skill gap review.

Avoid long verbatim reproduction. Summarize and quote only short fragments necessary to distinguish terms or verify a claim.

## Apply Approved Changes

After explicit approval:

1. Recheck Git status and stop for unknown changes.
2. Back up every existing file to `.backup/<timestamp>/` with its relative path.
3. Use the closest current template and valid Schema values.
4. Preserve Frontmatter title without Emoji and exactly one body H1 with optional Emoji.
5. Keep new pages `status: draft` and `publish: false` unless the user explicitly decides otherwise.
6. Add source locations and provenance labels.
7. Update only necessary existing pages and indexes; do not perform broad moves or public-language restructuring incidentally.
8. Run `python3 scripts/check_kb.py`.
9. Run the Quartz build for content, template, Schema, or rendering changes and inspect generated HTML when title or layout behavior is involved.
10. Show the exact Git diff and commit only when authorized. Never push unless explicitly requested.

## Improve This Skill Deliberately

End every use with a Skill gap review, even when no change is needed.

For each issue, state:

- what happened;
- whether it is reusable or task-specific;
- whether it affects safety/correctness, workflow reliability, deterministic validation, or style;
- where a durable fix belongs.

Place reusable workflow rules in `SKILL.md`, detailed decisions and examples in `references/`, deterministic repeated checks in `scripts/`, repository governance in `AGENTS.md`, architecture in the project overview, and Quartz content rules in the layout guide.

When the current task explicitly includes Skill improvement, immediately fix generalizable safety or correctness gaps and validate the Skill. For other improvements, propose the change before editing. Do not hard-code one-off wording preferences, one document's headings, or a single research report's taxonomy as universal rules.
