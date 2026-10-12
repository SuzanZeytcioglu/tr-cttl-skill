---
name: tr-cttl
description: "Use when Turkish technical text must be clear for a reader who cannot ask the author. Covers product instructions, software information for users, terminology, warnings, tool descriptions, error messages, and specifications. Triggers: anlamı netleştir, CTTL, kontrollü teknik Türkçe, TSE, kullanım bilgisi, terim, sadeleştir. Not for creative or marketing copy."
version: 0.2.0
---

# Controlled Turkish Technical Language (CTTL)

CTTL is controlled Turkish for a reader who cannot ask the author a question.

The focal references are TSE terminology standards and the ISO, IEC, and IEEE standards for information for use. Read `references/standards.md` for the map. Read `references/writing-rules.md` for the rewrite rules and the closed lists.

This skill applies the public aims of those standards. It does not copy their text. It does not issue a conformity claim.

## When to use this skill

Use this skill in these cases:

- A tool description, an error message, an instruction, or a status line is dense or ambiguous.
- A specification must state current behavior in Turkish.
- The caller asks for a before and after table.

Do not use this skill for creative copy or for text whose tone is the point.

## Two modes

Pick a mode before you rewrite. Infer the mode from the text type. Keep the choice internal unless the caller asks for the rule table.

**Strict.** Procedures, error messages, tool descriptions, and safety text. Apply every rule in `references/writing-rules.md`.

**CTTL-flavored.** Explanatory prose. Apply the structural rules. Treat the one-term rule as advisory.

## Core rules

Apply these rules on every rewrite. The closed word lists are in `references/writing-rules.md`.

| Rule | Write this | Do not write this |
|---|---|---|
| Named actor | "Araç dosyayı siler." | A finite verb with no actor in a tool description |
| One command | "Dosyayı açın. Üçüncü satırı okuyun." | Two commands in one sentence |
| Length | At most 20 words in a procedure. At most 25 words in a description. | A longer sentence |
| Punctuation | Separate sentences | A semicolon |
| Noun chain | At most three words in one noun chain | A longer stack of nouns |
| Modality | Keep "olabilir" and "-ebilir" | A hedge rewritten as a fact |
| Current state | State what the system does now | A story of a change |
| Paragraph | One topic. At most six sentences. | Two topics in one paragraph |
| Steps | A list when there are three or more steps | A sequence inside one sentence |
| Verb | "Günlüğü inceleyin." | A noun that hides the action |
| Target group | Define an expert term on first use in text for a general reader. | An undefined expert term |
| Safety | A warning, then the step. Name the hazard, the harm, and the avoidance. | A hazard buried inside the step |
| Definition | The broader concept, then the traits that set this concept apart. | A circular definition |

A word is a whitespace-separated token. Suffixes stay inside the word.

Turkish often drops the subject. In a procedure or a tool description, name the actor in the sentence.

Keep one finite verb in each sentence. Split a chain of relative clauses.

For a procedure, use the imperative. In a description, do not turn a statement into a command.

Keep every fact, number, condition, and limit. If a shorter sentence would drop one, keep the longer sentence.

Never add a cause, a rate, or a mechanism that the source does not state.

When a hedge and a shorter tense conflict, keep the hedge. "Başarısız olmuş olabilir" must not become "başarısız oldu".

Keep a designation that the applicable Turkish standard already fixes. Do not coin a second name for that concept.

Use the same designation for the same concept in the whole text. Define a domain term once when the reader may not know it.

In prose, use SI units. In prose, the decimal mark is a comma. Leave a number inside code, an identifier, or a protocol field as written.

## Process

1. Classify the text with `references/standards.md`. Name the class only when the caller asks for the rule table.
2. Pick the mode. Strict covers a procedure, a warning, a term entry, an error, and a tool description. CTTL-flavored covers explanatory prose.
3. Read the source until you can restate every fact.
4. Read `references/writing-rules.md`.
5. Mark each violation. For a first pass, run `scripts/cttl-lint.py` on the file or on stdin. Use `--json` for structured output. The script never flags a hedge. `--baseline N` allows N hard findings. `--disable rule1,rule2` silences named rules.
6. Rewrite each marked sentence. Keep the meaning. Keep the strength of each hedge.
7. If the source already complies, say so. Do not change compliant text.
8. Use the output format below.

The script checks a closed set of surface patterns. It does not check noun-chain length. It does not check a missing actor. It does not prove that a rewrite kept the meaning. A clean run means the configured checks found nothing.

## Output format

**Default.** Print only the rewritten text. Do not add a preamble, a mode line, a count, or a summary.

If you kept a longer sentence on purpose, add one line after the text:

`Kept as-is:` name the phrase and the fact that a shorter sentence would drop.

Omit that line when you kept nothing.

**On request.** When the caller asks for the diff or the rules, print this table:

```markdown
| Rule violated | Original | Simplified |
|---|---|---|
| Named actor | "Dosya silinir." | "Araç dosyayı siler." |
| Length | A 40-word sentence | Two sentences under the cap |

Mode: Strict. 2 violations found.
```

After the table, add one line for anything you did not simplify, and say why.

## Boundaries

This skill will:

- Rewrite dense Turkish into short active sentences with one meaning each.
- Return the rewritten text alone, unless the caller asks for the rules.
- Keep every fact, condition, and limit.
- Keep the strength of every hedge.
- Suggest one glossary line for a domain term that must stay.

This skill will not:

- Claim conformity to a TSE, ISO, IEC, or IEEE standard.
- Copy the text of a standard.
- Rewrite creative copy.
- Drop a safety condition in order to shorten a sentence.
- Turn "olabilir" into a fact.
- Invent a missing cause.
- Make empty content useful. Say that the source has no claim.
- Cut past the point where the sentence is clear.
