# orkestra

![orkestra tanıtım](docs/demo.gif)

herdr içinde yan yana çalışan kodlama ajanlarını tek bir koordinatörün yönetmesi için bir ajan
skill'i. Claude Code şef olur, Codex ve Antigravity (agy) işçi. Claude odada kimin olduğunu
kendiliğinden bilir, görevi net bir tanımla dağıtır, sonuçları dosyadan toplar, iddiaları
doğrular ve sana tek bir cevap verir.

> English: [README.en.md](README.en.md)

## Ne yapar?

- **Odayı kendiliğinden tanır.** Küçük bir oturum başlangıç kancası, aynı herdr workspace'indeki
  diğer ajanları (pane, durum) Claude'a söyler. "Yanında Codex ve agy var" diye anlatman gerekmez.
  herdr dışında hiçbir şey yazmaz, hata verse bile oturumu bozmaz.
- **Görevi kime vereceğini bilir.** Derin araştırma, kök neden analizi ve kod incelemesi Codex'e;
  hızlı keşif, kaynak bulma ve alternatif fikirler agy'ye; bölme, doğrulama ve sentez Claude'da
  kalır. Varsayılan tek işçidir, ikincisi yalnız gerçekten bağımsız iş ya da bilinçli ikinci görüş
  için eklenir.
- **Her görev kendi kendine yeten bir tanımla gider.** İşçi senin bağlamını bilmez, o yüzden her
  görevde kimlik, tek cümlelik hedef, salt okunur kuralı, doğrulanmış girdi yolları, sonuç dosyası
  ve bitiş işareti (`DONE <id>`) vardır.
- **Sonuç ekrandan değil dosyadan gelir.** İşçi cevabını bir dosyaya yazar ve son satıra
  `DONE <id>` koyar. Ajanın "boşta" görünmesi işin bittiği anlamına gelmez.
- **İddiaları doğrular.** "Testler geçiyor" bir iddiadır, sonuç değil. Kararı değiştirecek her
  bulgu açılıp kontrol edilir: dosya:satır, URL, komut. Kanıtsız, eski sürüme dair ya da kapsam
  dışı bulgular elenir.
- **Tek cevapta birleştirir.** Sana şu sırayla döner: her ajan ne buldu → neyi kabul etti, neyi
  reddetti ve neden → karar. Gerçek anlaşmazlıkları ortalamaya gömmez, gösterir.
- **Odayı sağlıklı tutar.** İzin, güncelleme ya da güven diyaloğu çıkarsa senin yerine seçim
  yapmaz, sana sorar. İzin atlama bayraklarını yalnız sen istediysen kullanır
  (`~/.orkestra/launch.json`).

## Kurulum

Koordinatör Claude Code'dur. Codex ve agy işçi olduğu için onlara bir şey kurman gerekmez.

### Claude Code eklentisi

```
/plugin marketplace add zekierman/orkestra
/plugin install orkestra@orkestra
```

Eklenti skill'i ve oda kancasını birlikte kurar. Kanca `python3` ile, o yoksa `python` ile çalışır.

### Elle kurulum

```bash
git clone https://github.com/zekierman/orkestra
cp -r orkestra/skills/orkestra ~/.claude/skills/
cp orkestra/hooks/orkestra-roster.py ~/.claude/hooks/
```

`~/.claude/settings.json` içinde `hooks.SessionStart` listesine ekle:

```json
{"hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/orkestra-roster.py", "timeout": 10}]}
```

Windows'ta python yolunu tam yaz. İkisini birden kurma: eklentiyi kurduysan elle eklediğin kancayı
kaldır, yoksa oda iki kez bildirilir.

### İzin bayrakları (isteğe bağlı)

Bir ajanı hep belli bayraklarla başlatmak istiyorsan `~/.orkestra/launch.json` yaz:

```json
{"agy": ["--dangerously-skip-permissions"]}
```

orkestra o ajanı başlatırken ya da yeniden başlatırken bu bayrakları ekler. Dosya yoksa izin atlama
bayrağını asla kendiliğinden eklemez.

## Nasıl kullanılır

herdr'da bir workspace aç: bir panede Claude Code, yan panelerde Codex ve agy. Claude'a doğal dille
söyle:

- "codex'e de sor"
- "agy'ye kaynakları baktır"
- "diğer ajanlara da incelet"
- "bunu paralel araştır"
- "ikinci görüş al"

Claude hangi panenin hangi görevi aldığını tek satırla söyler, bekler, doğrular ve sonucu verir.

## Bir görev nasıl görünür

```
TASK T3-review-kavra
Goal: kavra'nın SKILL.md dosyasındaki tutarsızlıkları bul
Mode: READ-ONLY except the result file. Do not edit, move, or create other files.
Inputs: <klon>/skills/kavra/SKILL.md  (commit 9c2d27f)
Deliver: write your answer to <temp>/T3.md, then end it with a final line "DONE T3-review-kavra".
Format: max 10 findings, one line each: file:line — problem — fix; cite file/URL for every claim
Limits: 15 min; if blocked, write "BLOCKED T3-review-kavra: <why>" to the result file.
```

Sonuç dosyaları her zaman repo ve kasa dışında, geçici bir klasörde durur. Böylece hafıza sistemleri
ve git işçilerin karalamalarını görmez.

## Sınırlar

- herdr gerekir. herdr dışında skill ve kanca devreye girmez.
- Koordinatör yalnız Claude Code. Codex ve agy'ye kanca yok, işçi olarak çalışırlar.
- İşçiler kota harcar. orkestra varsayılan olarak tek işçi kullanır ve pane altbilgisindeki kota
  uyarılarını sana söyler.
- Erken sürüm. Gerçek oturumlarda yaşanan hatalar ve çözümleri
  [`references/pitfalls.md`](skills/orkestra/references/pitfalls.md) içinde. Hata görürsen issue aç.

## Neden böyle?

Kuralların çoğu gerçek oturumlarda yaşanan bir hatadan çıktı:

- **Dosya, ekrandan güvenilirdir.** Alternatif ekran kullanan ajanların çıktısı ekran okumasında
  kaçabiliyor. `DONE <id>` satırı işin gerçekten bittiğini gösteriyor.
- **Uzun girdi dosyaya yazılır, istem ona işaret eder.** Büyük yapıştırmalar istemi takabiliyor
  (`agent_prompt_stalled`).
- **Sürüm sabitlenir.** Commit ya da dosya zamanı verilmezse işçi eski bir kopyayı inceleyebiliyor.
- **İkinci görüş kör olmalı.** Delegasyonun asıl değeri bağımsızlık; kendi sonucunu önce
  gösterirsen o bağımsızlığı kaybedersin.
- **İşçinin "bitti"si bir iddiadır.** Kaynaksız "araştırmalar gösteriyor ki…" cümleleri atılır,
  kararı değiştirecek bulgular yerinde kontrol edilir.

## Lisans

MIT
