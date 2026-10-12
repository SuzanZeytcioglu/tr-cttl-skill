#!/usr/bin/env python3
"""Deterministic linter for the structural CTTL rules in SKILL.md.

Checks only rules verifiable without a dictionary. Never flags hedges or
modality (olabilir, -ebilir, belki, bazen). Confidence is content.

Usage:
    cttl-lint.py FILE [FILE ...]
    echo "text" | cttl-lint.py [--json]
    cttl-lint.py --baseline 5 FILE
    cttl-lint.py --disable passive-voice,evidential FILE
    cttl-lint.py --selftest

Exit 1 when hard violations exceed the baseline (default 0).
Advisory findings (passive voice, evidential -mIştIr) never fail the run.
"""
import json
import re
import sys

# Regex heuristics, not a parser. No noun-chain rule: that needs part-of-speech
# tags. No missing-actor rule: Turkish drops subjects, and a regex cannot tell
# a legal drop from an illegal one.

# Closed lists match references/writing-rules.md.
SOFT_VERBS = (
    r"ele al\w{0,12}"
    r"|göz önünde bulundur\w{0,12}"
    r"|hayata geçir\w{0,12}"
    r"|derinlemesine"
    r"|iletişime geç\w{0,8}"
    r"|masaya yatır\w{0,12}"
)
MARKETING = (
    r"kusursuz|eşsiz|benzersiz|zahmetsiz|devrimsel|rakipsiz|sorunsuz"
    r"|kullanıcı dostu|son teknoloji|çığır açan"
)
NOMINAL = (
    r"gerçekleştir\w*"
    r"|yerine getir\w*"
    r"|(?:analiz|inceleme|doğrulama|değerlendirme)\s+(?:yap|gerçekleştir)\w*"
    r"|yapılması|edilmesi|sağlanması|gerçekleştirilmesi"
)
PASSIVE = (
    r"edilir|edilmez|edildi|edilmiştir|edilmelidir|edilecektir|edilmektedir"
    r"|yapılır|yapılmaz|yapıldı|yapılmıştır|yapılmalıdır|yapılmaktadır"
    r"|sağlanır|sağlandı|sağlanmıştır|sağlanmalıdır|sağlanmaktadır"
    r"|kullanılır|kullanıldı|kullanılmıştır|kullanılmaktadır"
    r"|tanımlanır|oluşturulur|silinir|gönderilir|beklenir|yazılır|okunur"
    r"|uygulanır|istenir|görülür|belirlenir|hesaplanır|kaydedilir"
    r"|başlatılır|durdurulur|çağrılır|tarafından"
)
HISTORY = (
    r"önceden|eskiden|geçmişte|daha önce|önceki sürüm\w*"
    r"|kaldırıldı|kaldırılmıştır|güncellendi|güncellenmiştir"
    r"|düzeltildi|düzeltilmiştir"
)

RULES = [
    ("semicolon", "advisory-free",
     re.compile(r";"),
     "CTTL bans the semicolon. Split the text into separate sentences."),
    ("soft-verb", "advisory-free",
     re.compile(r"\b(?:" + SOFT_VERBS + r")\b"),
     "Soft multi-word verb. Use one plain verb."),
    ("marketing-adjective", "advisory-free",
     re.compile(r"\b(?:" + MARKETING + r")\b"),
     "Marketing adjective. Delete it, or replace it with a measurement."),
    ("nominalization", "advisory-free",
     re.compile(r"\b(?:" + NOMINAL + r")\b"),
     "Action hidden in a noun. Use the verb."),
    ("passive-voice", "advisory",
     re.compile(r"\b(?:" + PASSIVE + r")(?:sa|se|lar|ler)?\b"),
     "Possible passive. Name the actor and use an active verb, unless the actor is unknown."),
    ("evidential", "advisory",
     re.compile(r"\b\w*(?:mış|miş|muş|müş)(?:tır|tir|tur|tür)\b"),
     "Evidential -mIştIr. Use a direct tense unless the inference itself is the point."),
    ("history-frame", "advisory-free",
     re.compile(r"\b(?:" + HISTORY + r")\b"),
     "Change narrative. State the current behavior."),
]

# One term, one meaning. Each item is (label, stems).
# Suffixes are a closed set so "kullan" does not match "kullanıcı".
_SUFFIXES = (
    "maktadır", "mektedir", "malıdır", "melidir",
    "makta", "mekte",
    "ıyor", "iyor", "uyor", "üyor",
    "mış", "miş", "muş", "müş",
    "yınız", "yiniz", "ınız", "iniz", "unuz", "ünüz", "nız", "niz",
    "ların", "lerin",
    "dı", "di", "du", "dü", "tı", "ti", "tu", "tü",
    "mak", "mek", "maz", "mez", "malı", "meli",
    "lar", "ler", "dan", "den", "tan", "ten",
    "nın", "nin", "nun", "nün",
    "yın", "yin", "yun", "yün",
    "yla", "yle", "arak", "erek",
    "ya", "ye", "yı", "yi", "yu", "yü",
    "ır", "ir", "ur", "ür",
    "ın", "in", "un", "ün",
    "da", "de", "ta", "te",
    "ma", "me", "n",
)
_SUFFIX_ALT = "|".join(sorted(_SUFFIXES, key=len, reverse=True))

SYNONYM_GROUPS = [
    (("doğrula", ("doğrula", "doğrul")), ("teyit", ("teyit",))),
    (("görüntüle", ("görüntüle", "görüntül")), ("göster", ("göster",))),
    (("sonlandır", ("sonlandır",)), ("durdur", ("durdur",))),
    (("yararlan", ("yararlan",)), ("kullan", ("kullan",))),
    (("gönder", ("gönder",)), ("ilet", ("ilet",))),
    (("onar", ("onar",)), ("düzelt", ("düzelt",))),
    (("kullanıcı", ("kullanıcı",)), ("müşteri", ("müşteri",)), ("istemci", ("istemci",))),
]


def _stem_re(stem):
    return re.compile(r"\b" + re.escape(stem) + r"(?:(?:" + _SUFFIX_ALT + r"))?\b")


_STEM_RE = {}
for _group in SYNONYM_GROUPS:
    for _label, _stems in _group:
        for _stem in _stems:
            _STEM_RE[_stem] = _stem_re(_stem)

MAX_WORDS = 25

CODE_FENCE = re.compile(r"^(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
LIST_ITEM_START = re.compile(
    r"^(?P<indent> {0,3})(?P<marker>[-*+]|[0-9]+[.)])(?P<gap> +)(?P<body>.*)$"
)
CONJUNCTION_END = re.compile(r"\b(?:ve|veya|ile|ya da)\s*$")
TABLE_SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")


def _tr_fold(text):
    """Length-preserving lowercase. Maps Turkish I/İ to ı/i."""
    return text.replace("İ", "i").replace("I", "ı").lower()


def _leading_spaces(line):
    return len(line) - len(line.lstrip(" "))


def _is_list_continuation(line, content_indent):
    if not line.strip():
        return True
    if LIST_ITEM_START.match(line):
        return False
    return _leading_spaces(line) >= content_indent


def _split_table_row(line):
    """Return trimmed table cells and their zero-based source columns."""
    left = len(line) - len(line.lstrip())
    right = len(line.rstrip())
    content = line[left:right]
    if "|" not in content:
        return None
    if content.startswith("|"):
        content = content[1:]
        left += 1
    if content.endswith("|"):
        content = content[:-1]
    raw_cells = re.split(r"(?<!\\)\|", content)
    if len(raw_cells) < 2:
        return None

    cells = []
    column = left
    for raw_cell in raw_cells:
        leading = len(raw_cell) - len(raw_cell.lstrip())
        cells.append((raw_cell.strip(), column + leading))
        column += len(raw_cell) + 1
    return cells


def _markdown_table_cells(lines):
    """Map ordinary Markdown table rows to their prose cells."""
    table_cells = {}
    index = 1
    while index < len(lines):
        separator = _split_table_row(lines[index])
        header = _split_table_row(lines[index - 1])
        if (not separator or not header or len(separator) != len(header)
                or not all(TABLE_SEPARATOR_CELL.fullmatch(cell)
                           for cell, _ in separator)):
            index += 1
            continue

        table_cells[index - 1] = header
        table_cells[index] = []
        index += 1
        while index < len(lines):
            row = _split_table_row(lines[index])
            if not row or len(row) != len(separator):
                break
            table_cells[index] = row
            index += 1
    return table_cells


def _dangling_conjunction_findings(text, filename):
    lines = text.splitlines()
    findings = []
    in_fence = False
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if CODE_FENCE.match(stripped):
            in_fence = not in_fence
            index += 1
            continue
        if in_fence:
            index += 1
            continue
        start = LIST_ITEM_START.match(line)
        if not start:
            index += 1
            continue

        content_indent = (len(start.group("indent"))
                          + len(start.group("marker"))
                          + len(start.group("gap")))
        item_lines = [(index, start.group("body"))]
        next_index = index + 1
        item_fence = False
        while next_index < len(lines):
            candidate = lines[next_index]
            candidate_stripped = candidate.strip()
            if CODE_FENCE.match(candidate_stripped):
                item_fence = not item_fence
                next_index += 1
                continue
            if item_fence:
                next_index += 1
                continue
            if not _is_list_continuation(candidate, content_indent):
                break
            item_lines.append((next_index, candidate))
            next_index += 1

        meaningful = []
        for line_index, item_line in item_lines:
            cleaned = INLINE_CODE.sub(" CODE ", item_line).strip()
            if cleaned:
                meaningful.append((line_index, cleaned))
        if meaningful:
            end_line_index, end_line = meaningful[-1]
            conjunction = CONJUNCTION_END.search(_tr_fold(end_line))
        else:
            end_line_index, end_line, conjunction = None, None, None
        if conjunction:
            if end_line_index == index:
                finding_line = index + 1
                finding_col = start.start("marker") + 1
            else:
                raw_end_line = next(
                    raw for line_index, raw in item_lines
                    if line_index == end_line_index
                )
                masked_end_line = INLINE_CODE.sub(
                    lambda match: " " * len(match.group(0)), raw_end_line
                )
                raw_conjunction = CONJUNCTION_END.search(_tr_fold(masked_end_line))
                finding_line = end_line_index + 1
                finding_col = raw_conjunction.start() + 1 if raw_conjunction else 1
            findings.append({
                "file": filename,
                "line": finding_line,
                "col": finding_col,
                "rule": "dangling-conjunction",
                "level": "advisory-free",
                "match": end_line,
                "message": "List item ends with a coordinating conjunction. Complete the item or join it with the next item.",
            })
        index = next_index
    return findings


def lint(text, filename="<stdin>"):
    findings = []
    words_total = 0
    in_fence = False
    lines = text.splitlines()
    table_cells = _markdown_table_cells(lines)
    seen_synonyms = {}
    for lineno, raw_line in enumerate(lines, 1):
        if CODE_FENCE.match(raw_line.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        segments = table_cells.get(lineno - 1, [(raw_line, 0)])
        for segment, source_column in segments:
            original = INLINE_CODE.sub("", segment)
            line = _tr_fold(original)
            words_total += len(line.split())
            for rule_id, level, pattern, msg in RULES:
                for match in pattern.finditer(line):
                    findings.append({
                        "file": filename,
                        "line": lineno,
                        "col": source_column + match.start() + 1,
                        "rule": rule_id,
                        "level": level,
                        "match": match.group(0),
                        "message": msg,
                    })
            for gi, group in enumerate(SYNONYM_GROUPS):
                for label, stems in group:
                    if (gi, label) in seen_synonyms:
                        continue
                    for stem in stems:
                        match = _STEM_RE[stem].search(line)
                        if match:
                            seen_synonyms[(gi, label)] = (
                                lineno, source_column + match.start() + 1, match.group(0)
                            )
                            break
            for sent in re.split(r"(?<=[.!?])\s+", line):
                n = len(sent.split())
                if n > MAX_WORDS:
                    findings.append({
                        "file": filename,
                        "line": lineno,
                        "col": source_column + 1,
                        "rule": "long-sentence",
                        "level": "advisory-free",
                        "match": f"{n} words",
                        "message": f"Sentence has {n} words (cap {MAX_WORDS}). Split it.",
                    })
    for gi, group in enumerate(SYNONYM_GROUPS):
        present = [(seen_synonyms[(gi, label)], label) for label, _stems in group if (gi, label) in seen_synonyms]
        if len(present) > 1:
            present.sort()
            first_label = present[0][1]
            for (lineno, col, match), label in present[1:]:
                findings.append({
                    "file": filename,
                    "line": lineno,
                    "col": col,
                    "rule": "synonym-rotation",
                    "level": "advisory-free",
                    "match": match,
                    "message": f"'{label}' and '{first_label}' name the same thing. Pick one and use it every time.",
                })
    findings.extend(_dangling_conjunction_findings(text, filename))
    findings.sort(key=lambda item: (item["line"], item["col"]))
    return findings, words_total


def report(findings, words_total, as_json, hard_count, baseline):
    rate = round(len(findings) * 100 / words_total, 1) if words_total else 0.0
    if as_json:
        print(json.dumps({
            "violations": findings,
            "count": len(findings),
            "hard_count": hard_count,
            "baseline": baseline,
            "words": words_total,
            "per_100_words": rate,
        }, indent=2, ensure_ascii=False))
        return
    for item in findings:
        print(f"{item['file']}:{item['line']}:{item['col']} {item['rule']}: {item['message']} [{item['match']}]")
    print(f"\n{len(findings)} violations ({hard_count} hard, baseline {baseline}), "
          f"{words_total} words, {rate} per 100 words")
    print("Hedges (olabilir, -ebilir, belki, bazen) are never flagged: confidence is content.")


def selftest():
    bad = (
        "Pano silinir; işi ele alın. "
        "Sorunsuz günlük üzerinde analiz gerçekleştirin. "
        "İş tamamlanmıştır. Sistem önceden böyle çalışırdı."
    )
    findings, _ = lint(bad)
    rules = {item["rule"] for item in findings}
    for expected in (
        "semicolon", "soft-verb", "nominalization", "marketing-adjective",
        "passive-voice", "evidential", "history-frame",
    ):
        assert expected in rules, (expected, findings)

    findings, _ = lint(
        "İstek başarısız olmuş olabilir. Bu bir zaman aşımı olabilir. "
        "Disk dolmuş olabilir."
    )
    assert findings == [], findings

    findings, _ = lint("İstek başarısız olmuştur.")
    assert [item["rule"] for item in findings] == ["evidential"], findings
    assert findings[0]["level"] == "advisory"

    findings, _ = lint("```\nx = a; y = b\n```")
    assert findings == []

    findings, _ = lint(
        "- Hedefi onayla ve\n"
        "* Sonucu kaydet VEYA  \n"
        "+ Panoyu kapat\n"
        "1. İşi başlat ve\n"
        "2) İşi durdur VEYA"
    )
    dangling = [item for item in findings if item["rule"] == "dangling-conjunction"]
    assert len(dangling) == 4, dangling
    assert [item["line"] for item in dangling] == [1, 2, 4, 5], dangling
    assert [item["col"] for item in dangling] == [1, 1, 1, 1], dangling
    assert all(item["level"] == "advisory-free" for item in dangling), dangling

    findings, _ = lint("  - Hedefi onayla ve\n    sonucu kaydet.")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)
    findings, _ = lint("- Hedefi onayla\n  ve")
    dangling = [item for item in findings if item["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1 and dangling[0]["line"] == 2, dangling
    assert dangling[0]["col"] == 3, dangling
    findings, _ = lint("    - kod ve")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)
    findings, _ = lint("> - Hedefi onayla ve\n> - Sonucu kaydet veya")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)
    findings, _ = lint("- Bunu yap ve\n~~~\nkod ve\n~~~")
    dangling = [item for item in findings if item["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1 and dangling[0]["line"] == 1, dangling
    findings, _ = lint("```text\n- kod ve\n```")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)

    findings, _ = lint(" - İşi başlat ve\n   sonucu kaydet.")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)
    findings, _ = lint("-  İşi başlat ve\n   sonucu kaydet.")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)
    findings, _ = lint("-\tİşi başlat ve")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)
    findings, _ = lint("   - İşi başlat ve", filename="fixture.md")
    dangling = [item for item in findings if item["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1 and dangling[0]["col"] == 4, dangling
    assert dangling[0]["file"] == "fixture.md"
    assert dangling[0]["match"].endswith("ve")
    assert "Complete the item" in dangling[0]["message"]
    findings, _ = lint("100. İşi başlat ve\n  ilgisiz metin")
    dangling = [item for item in findings if item["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1, dangling
    findings, _ = lint("- İşi başlat ve.\n- İşi durdur veya,")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)
    findings, _ = lint("- İşi başlat ve\n\n  sonucu kaydet.")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)
    findings, _ = lint("- Üst madde ve\n  - İç madde veya")
    dangling = [item for item in findings if item["rule"] == "dangling-conjunction"]
    assert [item["line"] for item in dangling] == [1, 2], dangling

    findings, _ = lint("Süreç adımlar ve içerebilir")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)
    findings, _ = lint("- `ve` etiketini kullan")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)
    findings, _ = lint("- `sol` ve `sağ` değerini birleştir")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings), findings
    findings, _ = lint("~~~\n- kod ve\n~~~")
    assert not any(item["rule"] == "dangling-conjunction" for item in findings)
    findings, _ = lint(("kelime " * 30).strip() + ".")
    assert any(item["rule"] == "long-sentence" for item in findings)

    short_cell = " ".join(f"terim{number}" for number in range(1, 25)) + "."
    for table in (
            "| Etiket | Ayrıntı |\n"
            "| --- | --- |\n"
            f"| Açık | {short_cell} |",
            "Etiket | Ayrıntı\n"
            "--- | ---\n"
            f"Açık | {short_cell}"):
        findings, words_total = lint(table)
        assert not any(item["rule"] == "long-sentence" for item in findings), findings
        assert words_total == 27, words_total
    long_cell = " ".join(f"terim{number}" for number in range(1, 27)) + "."
    findings, _ = lint(
        "| Etiket | Ayrıntı |\n"
        "| --- | --- |\n"
        f"| Açık | {long_cell} |"
    )
    long_sentences = [item for item in findings if item["rule"] == "long-sentence"]
    assert len(long_sentences) == 1, long_sentences
    assert long_sentences[0]["match"] == "26 words", long_sentences

    findings, _ = lint("Dosyayı doğrula. Sonra çıktıyı teyit et. Teyit iki kez.")
    rotation = [item for item in findings if item["rule"] == "synonym-rotation"]
    assert len(rotation) == 1 and "'teyit' and 'doğrula'" in rotation[0]["message"], rotation
    findings, _ = lint("Dosyayı doğrula. Çıktıyı doğrula.")
    assert not any(item["rule"] == "synonym-rotation" for item in findings)
    findings, _ = lint("Kullanıcı aracı kullanır. Gösterge değerini okuyun.")
    assert not any(item["rule"] == "synonym-rotation" for item in findings), findings
    findings, _ = lint("Kullanıcı kaydı müşteri kaydından ayrıdır.")
    rotation = [item for item in findings if item["rule"] == "synonym-rotation"]
    assert len(rotation) == 1 and "müşteri" in rotation[0]["message"], rotation
    findings, _ = lint("Değeri görüntüleyin. Sonra değeri gösterin.")
    rotation = [item for item in findings if item["rule"] == "synonym-rotation"]
    assert len(rotation) == 1, rotation
    findings, _ = lint("Dosyayı doğruluyor. Raporu teyit eder.")
    rotation = [item for item in findings if item["rule"] == "synonym-rotation"]
    assert len(rotation) == 1, rotation

    findings, _ = lint("a; b", filename="x.md")
    assert findings[0]["file"] == "x.md"
    print("selftest OK")


def main(argv):
    if "--selftest" in argv:
        selftest()
        return 0
    as_json = "--json" in argv
    baseline = 0
    disabled = set()
    paths = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--baseline":
            i += 1
            baseline = int(argv[i])
        elif arg == "--disable":
            i += 1
            disabled = set(argv[i].split(","))
        elif not arg.startswith("--"):
            paths.append(arg)
        i += 1

    findings, words_total = [], 0
    if paths:
        for path in paths:
            file_findings, file_words = lint(open(path, encoding="utf-8").read(), filename=path)
            findings.extend(file_findings)
            words_total += file_words
    else:
        findings, words_total = lint(sys.stdin.read())

    findings = [item for item in findings if item["rule"] not in disabled]
    hard_count = sum(1 for item in findings if item["level"] == "advisory-free")
    report(findings, words_total, as_json, hard_count, baseline)
    return 1 if hard_count > baseline else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
