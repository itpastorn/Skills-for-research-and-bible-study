---
name: prophetic-comparative-report
description: Produce a comparative report between 2-5 works (books, articles, theses, interviews, Lars Gunther's own drafts) on the prophetic and discernment. Use this skill whenever Lars asks for a comparative report, jämförande rapport, synthesis, or översikt involving prophecy, profetia, urskillning, discernment, hearing God's voice, att höra Guds röst, the prophetic gift, profetians gåva, or testing/evaluation of prophecy. Trigger on phrases like "jämför dessa verk om profetian", "skriv en jämförande rapport", "gör en översikt av det profetiska", "compare these works on prophecy", or any mention of Christine Westhoff, Jack Deere, Mike Bickle, Graham Cooke, John Paul Jackson, Kris Vallotton, R. Loren Sandford, Sam Storms, Wayne Grudem's prophecy book, or similar prophecy/discernment authors when a comparison or synthesis is requested. Also use when Lars points at 2-5 files in the profetia-urskillning-uppsatser-bocker project and asks for analysis across them.
---

# Prophetic Comparative Report

A repeatable workflow for producing a structured comparative report between 2-5 works on the prophetic and discernment. The output is a polished Word document (.docx) in IBM Plex Sans, at Level 2, 3, or 4 in Lars Gunther's register system, in Swedish or English, saved to the project folder `profetia-urskillning-uppsatser-bocker`.

The skill exists because this is recurring work for Lars's book project on testing the prophetic, and the same 11 questions and the same structural skeleton should be applied consistently across cases so that the resulting reports can be cross-compared later.

## Scope

- **Subject**: prophecy and discernment only. Other topics (healing, deliverance, spiritual formation) are out of scope for this skill.
- **Sources**: 2-5 works per report. Sources may be books, articles, theses, sermons, interview transcripts, or Lars's own draft manuscripts. There is no fixed anchor work — the set can be entirely from other authors, or Lars's own draft can be one of the voices.
- **Output**: one .docx per run, saved to the mounted `profetia-urskillning-uppsatser-bocker` folder (typically at `/sessions/<current-session>/mnt/profetia-urskillning-uppsatser-bocker/` — resolve the actual path at runtime by listing `/sessions/` or asking Lars), plus a quality flag printed in chat and at the end of the document.

## Workflow

1. **Intake** — identify the source files. Check the project folder and any files Lars has pointed to or uploaded. List them back to Lars so he can confirm.
2. **Clarifying questions** — use the AskUserQuestion tool (see `## Clarifying questions`). Do this before any research.
3. **Research pass** — read or summarise each source. Use parallel subagents when any single source exceeds ~30k words or when the combined corpus would overflow context. For smaller sources, read directly. Extract for each source: main thesis, methodology, stance on each of the 11 canonical questions, key vocabulary, unusual claims, notable strengths and weaknesses.
4. **Drafting** — write the report in markdown following `references/report-structure.md`. Organise each Q&A as Agreement / Complementarity / Tension.
5. **Verification pass** — only for Level 4. Re-check citations against the sources, confirm that chapter/subheading references are accurate, and that translated quotes preserve meaning.
6. **Production** — convert markdown to .docx using `scripts/build_docx.py`, which runs pandoc and then applies IBM Plex Sans to all runs, styles, and document defaults.
7. **Delivery** — present the file with a computer:// link, print the quality flag in chat, and stop. Do not add lengthy postambles about what's in the document.

## Clarifying questions

Ask these with AskUserQuestion before starting research. Group related questions in one call when possible.

1. **Level** — Level 2 (folkbildande/pastoral), Level 3 (default for this work; itpastorn.nu / deep article / book manuscript), or Level 4 (academic, SBL 2, full verification pass). If unclear, default to Level 3.
2. **Language** — Swedish or English. This affects translation rules, filename convention, and Bible translation defaults.
3. **Supplementary sources** — are there secondary sources, previous comparison documents in the folder, or specific articles Lars wants factored in beyond the 2-5 primary works? Rare but possible.
4. **Web search** — should the skill do any web searches (for author bios, reception history, reviews)? Default: no.
5. **Additional / custom questions** — the 11 canonical questions (see `references/questions.md`) are always included. Ask Lars if there is anything additional he wants the report to address this particular time. This is also where ad hoc learning-curve or applicability questions can go.
6. **Previous comparison docs** — is there an earlier comparison in the project folder that should be treated as context or updated rather than written fresh?

## Rules

### Filename convention

- Characters: `[a-z]`, `[0-9]`, hyphens, period. Swedish å→a, ä→a, ö→o; German ü→u. No underscores.
- Up to two author last names, then "-med-flera-" (Swedish report) or "-et-al-" (English report) if there are more than two.
- End with `-jamforande-rapport.docx` (Swedish) or `-comparative-report.docx` (English).
- Examples:
  - `westhoff-gunther-comparative-report.docx` (2 authors, English)
  - `westhoff-gunther-et-al-comparative-report.docx` (3+ authors, English)
  - `deere-storms-jamforande-rapport.docx` (2 authors, Swedish)
  - `deere-storms-med-flera-jamforande-rapport.docx` (3+ authors, Swedish)

### Translation policy

- **English report**: translate Swedish quotes into English inline. Keep original Swedish in a footnote only if Level 4 and the phrasing matters.
- **Swedish report**: keep English quotes in English. Do not translate them.
- **Greek / Hebrew**: follow Lars's standard rules — original script, popular transliteration (Levels 1-3) or simplified academic (Level 4), English/Swedish translation.
- **German, French, Latin**: original + translation.
- **Other languages**: translation only unless Lars specifies otherwise.

### Citations

- SBL 2 style.
- Use **chapter + subheading** as the pointer, not page numbers, unless the source genuinely has stable pagination (e.g. a peer-reviewed PDF) and the level demands it.
- Level 4: full verification pass against the source text. Quotes must be verbatim.
- Levels 2-3: paraphrase is acceptable when exact quotes can't be confirmed; flag any paraphrased passages as such.

### Bibliography

- Primary sources only — the 2-5 works being compared.
- Note influences on each author (mentors, theological traditions, prior works) in flowing text inside the "Authors in context" section, not as separate bibliography entries.

### Subagents

- Use judgment. If any single source exceeds ~30k words or the combined corpus would not fit comfortably in context, spawn parallel subagents — one per source — to produce structured summaries organised around the 11 canonical questions.
- For smaller sources, read directly; the round-trip via subagent is overhead.

### Quality flag

Every report ends with a short quality flag section. This is honest diagnostics for Lars, not marketing. Cover:

- What was reconstructed vs. quoted verbatim
- Any chapter/subheading references that are approximate
- Under-developed areas in the sources that affected the answers
- Known gaps in the research (e.g. sources Lars might have wanted included)

Print the same quality flag in the chat response when delivering the file, so Lars sees it without opening the document.

## Report structure

See `references/report-structure.md` for the full template. The high-level skeleton:

1. Title
2. Description of the assignment (one paragraph: what Lars asked for, which sources, which level, which language)
3. Authors in context (one paragraph per author: background, traditions, influences, relevant biases)
4. Abstract + key takeaways (bullet list, 5-10 items — this is the one place bullets are allowed at Level 3+)
5. Methodology (one paragraph; if Lars's own draft is among the sources and its approach differs markedly from the others, note this once, briefly, without repetition later)
6. Q&A — 11 canonical questions, plus any additional ones Lars requested. Each organised as **Agreement / Complementarity / Tension**.
7. Longer summary (flowing prose, no bullets)
8. Suggested further study (list of topics that emerged but weren't developed)
9. Bibliography (primary sources, SBL 2)
10. Quality flag (honest diagnostics, as above)

## Canonical questions

The 11 questions are in `references/questions.md`. They are always included. Q12 from the original Westhoff case ("learning curve") is dropped — the open clarifying question about additional/custom questions covers that territory more flexibly.

## Production

Use `scripts/build_docx.py`. It:

1. Takes a markdown input path and an output .docx path.
2. Runs pandoc to produce a raw .docx.
3. Opens the docx with python-docx and sets IBM Plex Sans on all runs, all style rPr elements, and docDefaults.
4. Saves the final file.

Invoke it like:

```bash
python <skill-path>/scripts/build_docx.py \
  --input /sessions/<current-session>/report-draft.md \
  --output /sessions/<current-session>/mnt/profetia-urskillning-uppsatser-bocker/<filename>.docx
```

Dependencies: `pandoc` (system), `python-docx`, `lxml`. Install with `pip install python-docx lxml --break-system-packages` if missing.

## Delivery

- Save the .docx to the mounted `profetia-urskillning-uppsatser-bocker` folder. Resolve the path at runtime: list `/sessions/` to find the current session name, then use `/sessions/<current-session>/mnt/profetia-urskillning-uppsatser-bocker/`.
- Present a `computer://` link to the file.
- Print the quality flag in chat.
- Stop. No lengthy summary of what's in the report — Lars can open it.
