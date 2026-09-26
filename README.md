# orkestra

herdr içinde yan yana çalışan kodlama ajanlarını (Claude Code, Codex, Antigravity…) tek bir
koordinatörün yönetmesi için bir skill ve küçük bir oturum başlangıç kancası.

- **Kanca:** Claude herdr içinde açıldığında aynı workspace'teki diğer ajanları (pane, durum)
  kendiliğinden öğrenir. Anlatmana gerek kalmaz. herdr dışında hiçbir şey yazmaz, hata verse bile
  oturumu bozmaz.
- **Skill:** Görevi kime vereceğini, görevi nasıl tanımlayacağını (kimlik, salt okunur, sonuç
  dosyası, `DONE <id>`), nasıl bekleyeceğini, iddiaları nasıl doğrulayacağını ve sonuçları nasıl
  birleştireceğini anlatır. Gerçek oturumlarda yaşanan hatalar ve çözümleri `references/pitfalls.md`
  içinde.

## Kurulum (Claude Code, koordinatör)

```bash
cp -r skills/orkestra ~/.claude/skills/
cp hooks/orkestra-roster.py ~/.claude/hooks/
```

`~/.claude/settings.json` içinde `hooks.SessionStart` listesine ekle:

```json
{"hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/orkestra-roster.py", "timeout": 10}]}
```

(Windows'ta python yolunu tam yaz.) Codex ve agy işçi olduğu için onlara kanca gerekmez.

## Lisans

MIT
