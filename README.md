# CTTL becerisi

English: [README.en.md](README.en.md).

Bu beceri yoğun Türkçeyi Kontrollü Teknik Türkçeye (CTTL) dönüştürür.

CTTL, TSE terim standartları ile ISO, IEC ve IEEE kullanım bilgisi standartlarının açık amaçlarını Türkçeye uygular. Harita [`references/standards.md`](references/standards.md) dosyasındadır. Bu beceri standart metnini kopyalamaz. Bu beceri uygunluk belgesi vermez.

Okur, cümlenin anlamını yazara soramayan bir kişi ya da bir programdır. Tipik girdi bir araç tanımı, bir hata metni, bir yönerge, bir durum satırı ya da bir belirtimdir.

## Neden kontrollü Türkçe

Kullanım bilgisi, güvenli ve etkili bir iş için gerekir. Terim çalışması bir kavrama bir yeğlenen ad verir. Tanım, üst kavramı ve ayırt edici özellikleri söyler. Yanlış okunan bir bakım adımının bedeli yüksektir. Okur yazara çoğu zaman ulaşamaz.

Aynı risk teknik Türkçede vardır. Edilgen çatı eyleyeni gizler. Uzun bir ad zinciri baş adı gizler. Türkçede özne düşebilir. Bir araç tanımında düşen özne anlamı belirsiz kılar. Bir değişim anlatısı güncel davranışı gizler.

## Önce ve sonra

| Önce | Sonra |
|---|---|
| "Bu araç, yapılandırılmış arka uçlar arasında durumu eşitlemeye çalışacak ve bir çakışma çıkarsa bunu otomatik olarak çözebilir ya da çakışmayı elle inceleme için gösterecektir." | "Araç, yapılandırılmış arka uçlar arasında durumu eşitlemeye çalışır. Araç bir çakışma bulursa yapılandırılmış stratejiyi okur. Strateji otomatik çözüme izin verirse araç çakışmayı çözebilir. Araç çakışmayı çözmezse çakışmayı elle inceleme için bildirir." |
| "İsteğiniz, beklenen veri biçimindeki olası bir uyuşmazlık nedeniyle başarısız olmuş olabilir." | "İsteğiniz başarısız olmuş olabilir. Neden, veri biçiminin sunucunun beklediği biçimle uyuşmaması olabilir. İstemci sürümünü kontrol edin." |

Daha fazla örnek [`examples/before-after.md`](examples/before-after.md) dosyasındadır.

## Beceri ne yapar

1. Beceri bir kip seçer. **Katı** kip bir yönergeyi, bir hata metnini ve bir araç tanımını kapsar. **CTTL tadında** kip açıklayıcı düzyazıyı kapsar. Bu kip cümle kurallarını tutar. Tek terim kuralı bu kipte uyarıdır.
2. Beceri Türkçe metni anlam için okur.
3. Beceri her ihlali işaretler. Yapı kuralları ve kapalı listeler [`references/writing-rules.md`](references/writing-rules.md) dosyasındadır.
4. Beceri işaretli her cümleyi yeniden yazar. Beceri bir olguyu, bir koşulu ya da bir sınırı düşürmez. Beceri "olabilir" sözünü bir olguya çevirmez.
5. Beceri yalnızca yeni metni basar. Beceri uzun bir cümleyi bilerek tutarsa metnin sonuna bir `Kept as-is:` satırı ekler.

Kural tablosu için farkı isteyin.

`scripts/cttl-lint.py` yalnızca yüzey örüntülerini denetler. Betik kaynağı yeni metinle karşılaştırmaz. Betik anlamın aynı kaldığını kanıtlamaz. Temiz bir sonuç, açık denetimlerin sorun bulmadığı anlamına gelir.

Betik noktalı virgülü, kısa bir gevşek eylem listesini ve adlaştırmaları denetler. Betik pazarlama sıfatlarını, değişim anlatısını ve cümle uzunluğunu denetler. Betik terim dönüşünü ve desteklenen bir liste maddesindeki askıda bağlacı denetler. Edilgen biçimler ve dolaylı bildirme uyarıdır. Bu bulgular çalıştırmayı başarısız etmez. Betik bir olasılık ifadesini işaretlemez. Betik ad zincirinin uzunluğunu denetlemez. Betik, listesinin dışındaki gevşek eylemi tanımaz.

Depo kökünde şu denetimleri çalıştırın:

```
python scripts/cttl-lint.py --selftest
python scripts/cttl-lint.py SKILL.md README.md README.tr.md
python scripts/cttl-lint.py examples/linter-edge-cases.md
```

`SKILL.md`, `README.md` ve `README.tr.md` taban 0 ile temiz çıkar. `examples/linter-edge-cases.md` geçersiz bir sınama dosyasıdır. Betik bu dosyada iki askıda bağlaç bulgusu verir. `references/writing-rules.md` kapalı listeleri aynen yazar. O dosyanın denetimi bu listeleri bulgu olarak gösterir.

Askıda bağlaç kuralı "-", "*", "+" ve sayı imlerini kabul eder. Sayı imi "." ya da ")" ile biter. İmin önünde en çok üç boşluk vardır. Dört ya da daha fazla boşlukla başlayan satır liste imi sayılmaz. Çit içindeki kodu betik yok sayar. Bir alıntı içindeki listeyi betik ayrıştırmaz.

## Kurulum

Proje kökünde şunu çalıştırın:

```
npx skills add adilumer/tr-cttl-skill
```

Depoyu klonlayın. Beceri yükleyicinizi bu dizine yöneltin.

## Kullanım

Bir Türkçe metni sadeleştirmek ya da anlamını netleştirmek için şunu yazın:

```
Bu araç tanımının anlamını netleştir
Bu hata metnini yanlış okunamayacak şekilde yaz
Bu yönergeye CTTL uygula
```

Yalnızca yeni metni alırsınız. Kural tablosu için "farkı göster" ifadesini ekleyin.

## Kapsam

Şu metinlerde CTTL seçin: araç tanımı, hata metni, yönerge, durum satırı, belirtim.

Yaratıcı yazıda CTTL seçmeyin. Pazarlama metninde CTTL seçmeyin.

Beceri metnin biçimini düzeltir. Beceri eksik olgu eklemez. Belirsiz bir paragraf yeni metinde de boş kalır. Beceri bu durumu bildirir.

## Kaynaklar

Standart haritası [`references/standards.md`](references/standards.md) dosyasındadır. Yürürlükteki TS kaydını [TSE kataloğundan](https://intweb.tse.org.tr/) doğrulayın.

- [IEC/IEEE 82079-1:2019](https://webstore.iec.ch/en/publication/29075)
- [ISO/IEC/IEEE 26514:2022](https://www.iso.org/standard/77451.html)
- [ISO 704:2022](https://www.iso.org/standard/79077.html)

## Lisans

MIT. Metin [LICENSE](LICENSE) dosyasındadır.
