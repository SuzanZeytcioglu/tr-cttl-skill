# CTTL writing rules

This file is the rule source for the rewriter and for `scripts/cttl-lint.py`.

The focal references are in `standards.md`. CTTL applies their public aims to Turkish technical text. Sentence caps, the semicolon check, and the closed lists below are local checks. They are not clauses of those standards.

## What the rewriter enforces

**Word choice**

- Use one preferred designation for one concept. Do not rotate names for the same actor or the same action.
- Keep a designation that the applicable Turkish standard already fixes.
- Prefer the plain verb. Do not hide the action in a noun.
- Define a domain term once if the reader may not know it.
- A definition names the broader concept and the traits that set this concept apart. A definition is not circular.
- Do not use a soft multi-word verb whose meaning is not the sum of its parts.

**Verb and actor**

- Name the actor in a procedure and in a tool description.
- Use the imperative for a procedure.
- Use active voice. Use a passive only when the actor is unknown.
- Use a direct tense for a known fact. Keep "-mIş" or "-mIştIr" when the source reports an inference.
- Keep "olabilir", "-ebilir", "belki", and "bazen". Those marks are content.

**Sentence shape**

- Put one command in one sentence.
- Keep one finite verb in a sentence.
- Use at most 20 words in a procedure. Use at most 25 words in a description.
- A word is a whitespace-separated token.
- Do not drop the actor, the object, or a limit in order to shorten the line.
- Keep a noun chain to at most three words.
- Do not use a semicolon. Use a new sentence.
- Put one topic in a paragraph. Use at most six sentences.
- Use a list for three or more steps or conditions.
- Put a warning before the hazardous step. Name the hazard, the harm, and how to avoid the harm.
- Name the target group when the wording depends on it. Define an expert term on first use in text for a general reader.
- In prose, use SI units. In prose, the decimal mark is a comma. Leave a number inside code, an identifier, or a protocol field as written.

**Current state**

- State the behavior the system has now.
- Do not narrate a change. Do not name a past edition as the way to explain the present.

**Meaning**

- Do not add a fact, a cause, or a rate.
- If a shorter line would drop a required fact, keep the longer line and say so.

## Closed lists the linter checks

The linter matches these surface forms. A form outside a list can still break a rule. The rewriter still fixes it. The script will not see it.

**Soft verbs (hard)**

- ele al
- göz önünde bulundur
- hayata geçir
- derinlemesine
- iletişime geç
- masaya yatır

**Marketing adjectives (hard)**

- kusursuz
- eşsiz
- benzersiz
- zahmetsiz
- devrimsel
- rakipsiz
- sorunsuz
- kullanıcı dostu
- son teknoloji
- çığır açan

**Nominalizations (hard)**

- gerçekleştir
- yerine getir
- analiz yap
- inceleme yap
- doğrulama yap
- değerlendirme yap
- yapılması
- edilmesi
- sağlanması
- gerçekleştirilmesi

**Change narrative (hard)**

- önceden
- eskiden
- geçmişte
- daha önce
- önceki sürüm
- kaldırıldı
- kaldırılmıştır
- güncellendi
- güncellenmiştir
- düzeltildi
- düzeltilmiştir

**Passive forms (advisory)**

The script flags these forms, plus an optional "-sa", "-se", "-lar", or "-ler":

- edilir, edilmez, edildi, edilmiştir, edilmelidir, edilecektir, edilmektedir
- yapılır, yapılmaz, yapıldı, yapılmıştır, yapılmalıdır, yapılmaktadır
- sağlanır, sağlandı, sağlanmıştır, sağlanmalıdır, sağlanmaktadır
- kullanılır, kullanıldı, kullanılmıştır, kullanılmaktadır
- tanımlanır, oluşturulur, silinir, gönderilir, beklenir, yazılır, okunur
- uygulanır, istenir, görülür, belirlenir, hesaplanır, kaydedilir
- başlatılır, durdurulur, çağrılır
- tarafından

**Evidential (advisory)**

The script flags a word that contains "-mIştIr", "-mIştİr", "-mUştUr", or "-mÜştÜr" with the matching vowels. "Olmuş olabilir" does not match. Do not delete a hedge to satisfy this check.

**One term (hard)**

The script flags a second label from the same group. It does not flag a repeated label.

| Group | Labels |
|---|---|
| 1 | doğrula, teyit |
| 2 | görüntüle, göster |
| 3 | sonlandır, durdur |
| 4 | yararlan, kullan |
| 5 | gönder, ilet |
| 6 | onar, düzelt |
| 7 | kullanıcı, müşteri, istemci |

"Kullan" does not match "kullanıcı". "Göster" does not match "gösterge".

**List conjunctions (hard)**

A list item must not end on "ve", "veya", "ile", or "ya da".

The check accepts "-", "*", "+", and a numeric marker that ends in "." or ")". The marker may have zero to three leading spaces, then ASCII spaces. A line with four or more leading spaces is not a list marker. The check ignores fenced code. It does not parse a list inside a blockquote.

**Length (hard)**

A sentence over 25 words is a finding. The procedure cap of 20 words is for the rewriter. The script cannot tell a procedure from a description, so it uses 25.

## What the linter does not check

- Noun-chain length.
- A missing actor.
- A hedge or a modal.
- Whether a rewrite kept the meaning.
- Whether two terms in group 7 are real synonyms in that text. "Kullanıcı" and "istemci" can be different roles. If they are, keep both and say why.
- Phrases outside the closed lists.

A clean run means these checks found nothing. It does not mean the text is good CTTL.

## Sources

See `standards.md`.
