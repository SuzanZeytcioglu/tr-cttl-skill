# Before and after

These examples are original. They show how to rewrite Turkish for a reader who cannot ask a question. The standards behind the aims are in `references/standards.md`.

Word counts are whitespace-separated tokens.

## Example A, tool description

**Before:**

> Bu araç, yapılandırılmış olan çeşitli arka uçlar arasında durumu eşitlemeye çalışacak ve bir çakışma tespit edilirse ayarlanmış stratejiye bağlı olarak bunu otomatik olarak çözebilir ya da çakışmayı elle inceleme için gösterecektir.

**What is wrong:**

- One sentence holds two jobs.
- The actor of "tespit edilirse" is missing.
- The sentence is longer than 25 words.

"Çözebilir" stays. The tool is not promised to succeed.

**After:**

> Araç, yapılandırılmış arka uçlar arasında durumu eşitlemeye çalışır. Araç bir çakışma bulursa yapılandırılmış stratejiyi okur. Strateji otomatik çözüme izin verirse araç çakışmayı bir kişi olmadan çözebilir. Araç çakışmayı çözmezse çakışmayı elle inceleme için bildirir.

The last sentence follows the case where the tool does not resolve the conflict. That is what the source meant by the other branch.

## Example B, error message

**Before:**

> İsteğiniz sunucu tarafında işlenirken, sunucunun beklediği veri biçimindeki olası bir uyuşmazlık nedeniyle bir hata oluşmuş olabilir ve buna güncel olmayan bir istemci sürümü neden olmuş olabilir.

**What is wrong:**

- One sentence holds three claims.
- The sentence is longer than 25 words.

"Olmuş olabilir" stays. The system does not know that the request failed.

**After:**

> İsteğiniz başarısız olmuş olabilir. Neden, veri biçiminin sunucunun beklediği biçimle uyuşmaması olabilir. Güncel olmayan bir istemci bu uyuşmazlığı oluşturabilir. İstemci sürümünü kontrol edin.

Do not write "İstek başarısız oldu". That sentence deletes the hedge. Do not write "en sık neden". The source states no rate.

## Example C, instruction

**Before:**

> Yukarı akış işi tamamlandıktan ve hata oluşmadığı varsayıldığında aşağı akış tarafı çıktı yapıtını okumalı, ancak zaman aşımında kısmi yapıt üretilebildiği de göz önünde bulundurulmalıdır.

**What is wrong:**

- "Göz önünde bulundurulmalıdır" is a soft verb plus a passive.
- One sentence holds three facts.
- The next action is buried in a subordinate clause.

**After:**

> Yukarı akış işinin hatasız bitmesini bekleyin. Sonra çıktı yapıtını okuyun. Uyarı: zaman aşımı kısmi bir yapıt üretebilir. Yapıtı kullanmadan önce yapıtın tam olduğunu kontrol edin.

The last sentence is new. The source warned about a partial artifact and did not say what to do. If that silence was deliberate, drop the last sentence.

## Example D, explanatory prose

Mode: CTTL-flavored.

**Before:**

> Önbellek katmanımız mevcut yığına sorunsuz oturur ve satıcı kilidi yoktur; anlamsal benzerlikten faydalanarak ıskaları büyük ölçüde azaltır.

**What is wrong:**

- "Sorunsuz" is a marketing adjective.
- The semicolon joins two claims.
- "Faydalanarak" is a soft verb outside the closed list. The script does not flag it. Write the comparison in a direct verb.
- The sentence states no measurement.

**After:**

> Normal bir önbellek istekleri birebir metinle eşler. İfade küçük değişirse önbellek ıska verir. Bu önbellek yeni bir istemin anlamını, tuttuğu istemlerle karşılaştırır. Önbellek mevcut yığınla birlikte çalışır. Önbellek, veriyi yığının dışında saklamaz.

Flavored mode still cuts the marketing word and the semicolon.

## Example E, current state

**Before:**

> Önceden sistem dosyayı diske yazardı. Bu davranış güncellendi. API yanıtı artık yalnızca bellekte tutulur.

**What is wrong:**

- "Önceden" and "güncellendi" narrate a change.
- "Tutulur" hides the actor.

**After:**

> API yanıtı bellekte durur. API yanıtı diske yazılmaz.

The rewrite states the current behavior. It does not name the old behavior.

## Example F, warning

**Before:**

> Cihazı çalıştırmadan önce kapağın kapalı olduğundan emin olun, aksi halde sıcak yüzey yanığa yol açabilir ve bu risk göz önünde bulundurulmalıdır.

**What is wrong:**

- The hazard sits inside the step.
- "Göz önünde bulundurulmalıdır" hides the avoidance action.

**After:**

> Uyarı: Kapak açıkken yüzey sıcaktır. Sıcak yüzey yanığa yol açabilir. Kapağı kapatın. Sonra cihazı çalıştırın.

The warning names the hazard, the harm, and the avoidance. The start command comes after that warning.

## Example G, term

**Before:**

> Denetim, sistemin denetlenmesidir. Sonucu teyit edin ve sonra doğrulayın.

**What is wrong:**

- The definition repeats the term and adds no trait.
- "Teyit" and "doğrula" name one action with two verbs.

**After:**

> Denetim, bir sonucun yazılı şarta uyup uymadığının bakılmasıdır. Sonucu denetleyin.

The definition names the broader act and the trait that sets it apart. The step uses that same designation.
