# CTTL skill

Türkçe: [README.md](README.md).

A skill that rewrites dense Turkish into Controlled Turkish Technical Language (CTTL).

CTTL applies the public aims of the TSE terminology standards. It also applies the public aims of the ISO, IEC, and IEEE standards for information for use. The map is [`references/standards.md`](references/standards.md). The skill does not copy those texts. The skill does not issue a conformity claim.

The reader is a person or a program that cannot ask the author what a sentence means. Typical inputs are a tool description, an error message, an instruction, a status line, and a specification.

## Why a controlled Turkish

Information for use supports a safe and effective task. Terminology work gives one concept one preferred designation. A definition states the broader concept and the traits that set the concept apart. A misread maintenance step is expensive, and the reader often cannot call the author.

The same failure mode exists in Turkish technical text. The passive hides the actor. A long noun chain hides the head noun. A dropped subject is legal in Turkish and ambiguous in a tool description. A change narrative hides the current behavior.

## Before and after

| Before | After |
|---|---|
| "Bu araç, yapılandırılmış arka uçlar arasında durumu eşitlemeye çalışacak ve bir çakışma çıkarsa bunu otomatik olarak çözebilir ya da çakışmayı elle inceleme için gösterecektir." | "Araç, yapılandırılmış arka uçlar arasında durumu eşitlemeye çalışır. Araç bir çakışma bulursa yapılandırılmış stratejiyi okur. Strateji otomatik çözüme izin verirse araç çakışmayı çözebilir. Araç çakışmayı çözmezse çakışmayı elle inceleme için bildirir." |
| "İsteğiniz, beklenen veri biçimindeki olası bir uyuşmazlık nedeniyle başarısız olmuş olabilir." | "İsteğiniz başarısız olmuş olabilir. Neden, veri biçiminin sunucunun beklediği biçimle uyuşmaması olabilir. İstemci sürümünü kontrol edin." |

More examples are in [`examples/before-after.md`](examples/before-after.md).

## What the skill does

1. It picks a mode. **Strict** covers a procedure, an error message, and a tool description. **CTTL-flavored** covers explanatory prose. Flavored mode keeps the sentence rules and treats the one-term rule as advisory.
2. It reads the Turkish for meaning.
3. It marks each violation. The structural rules and the closed lists are in [`references/writing-rules.md`](references/writing-rules.md).
4. It rewrites each marked sentence. It does not drop a fact, a condition, or a limit. It does not turn "olabilir" into a fact.
5. It prints the rewritten text alone. It adds one `Kept as-is:` line only when it kept a longer sentence on purpose.

Ask for the diff when you want the rule table.

`scripts/cttl-lint.py` checks surface patterns only. It does not compare a source with a rewrite. It does not prove that the meaning stayed the same. A clean run means the configured checks found nothing.

The script checks the semicolon, a short list of soft verbs, and nominalizations. It also checks marketing adjectives, a change narrative, and sentence length. It also checks term rotation and a dangling conjunction in a supported list item. Passive forms and the evidential copula are advisory. They do not fail the run. The script never flags a hedge. It does not check noun-chain length. It does not know a soft verb outside its list.

Run these checks from the repo root:

```
python scripts/cttl-lint.py --selftest
python scripts/cttl-lint.py SKILL.md README.md README.tr.md
python scripts/cttl-lint.py examples/linter-edge-cases.md
```

`SKILL.md`, `README.md`, and `README.tr.md` pass with baseline 0. `examples/linter-edge-cases.md` is an invalid fixture. The script reports two dangling-conjunction findings there. `references/writing-rules.md` quotes the closed lists, so a lint of that file reports those lists.

The dangling-conjunction rule accepts "-", "*", "+", and a numeric marker that ends in "." or ")". The marker has zero to three leading spaces. A line with four or more leading spaces is not a marker. Fenced code is ignored. A list inside a blockquote is not parsed.

## Install

From the project root:

```
npx skills add adilumer/tr-cttl-skill
```

Or clone the repo and point your skill loader at this directory.

## Use

Ask to simplify or to disambiguate a Turkish text:

```
Bu araç tanımının anlamını netleştir
Bu hata metnini yanlış okunamayacak şekilde yaz
Bu yönergeye CTTL uygula
```

You receive the rewritten text and nothing else. Add "farkı göster" when you want the rule table.

## Scope

Use CTTL for a tool description, an error message, an instruction, a status line, and a specification.

Do not use CTTL for creative writing or for marketing copy.

The skill fixes the form of a text. It does not add missing facts. A vague paragraph stays empty after the rewrite, and the skill should say so.

## Sources

The standard map is [`references/standards.md`](references/standards.md). Confirm the current TS record in the [TSE catalog](https://intweb.tse.org.tr/).

- [IEC/IEEE 82079-1:2019](https://webstore.iec.ch/en/publication/29075)
- [ISO/IEC/IEEE 26514:2022](https://www.iso.org/standard/77451.html)
- [ISO 704:2022](https://www.iso.org/standard/79077.html)

## License

MIT. See [LICENSE](LICENSE).
