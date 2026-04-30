
---

# 🚀 Odoo 18 CLI Cheat Sheet (Fast & Practical)

> One-liners, dev tricks, and commands for daily Odoo 18 hacking.

---

## ⚡ 1. The One Command You'll Use 100×/day

```bash
./odoo/odoo-bin --addons-path=odoo/addons,custom_addons -d mydb --dev=all
```

✅ Auto-reloads Python + XML on save  
✅ Live view updates on browser refresh  
✅ Perfect for **list → form → code → repeat** cycle

---

## 📦 2. Module Install / Update (The Only Two You Need)

| Action | Command |
|--------|---------|
| **Install** new module first time | `-i my_module` |
| **Update** after code change | `-u my_module` |
| Multi-module | `-i web,my_module` |

🔁 **Example after changing a list view column:**
```bash
./odoo/odoo-bin --addons-path=odoo/addons,custom_addons -d mydb -u my_module
```

> *No restart needed if `--dev=all` is on — but if views get "stuck", run `-u` to clear cache.*

---

## 🧱 3. Scaffold a New Module (Instant Folder Structure)

```bash
./odoo/odoo-bin scaffold cool_module ./custom_addons
```

Generates:
```
cool_module/
├── __init__.py
├── __manifest__.py
├── models/
├── views/
├── security/
└── data/
```

---

## 🗄️ 4. Database Quick Ops

| Task | Command |
|------|---------|
| Create DB + install module | `./odoo/odoo-bin -d fresh_db -i my_module --stop-after-init` |
| Drop DB (from terminal) | `dropdb fresh_db` |
| Reset DB | `dropdb mydb && createdb mydb` |

---

## 🛠️ 5. Pro Dev Flags (Copy-paste ready)

```bash
# No timeout while debugging
--limit-time-real=0

# Different port (avoid conflicts)
-p 8080

# Super verbose logs (find crashes fast)
--log-level=debug

# Interactive Python shell inside Odoo
shell -d mydb
```

🧠 **Shell example:**
```bash
./odoo/odoo-bin shell -d mydb
>>> self.env['res.partner'].search_count([])
>>> self.env['my.model'].create({'name': 'test'})
```

---

## ⚠️ 6. Odoo 18 List View (No Old Syntax!)

| Old (v17) | ✅ Odoo 18 |
|-----------|------------|
| `<tree>` | `<list>` |
| `view_mode="tree,form"` | `view_mode="list,form"` |
| `string=` field attr | `label=` (in some contexts) |

> If your list view shows old columns → `-u your_module` + hard refresh browser.

---

## 🔧 7. Fix Common Crashes Fast

### Port 8069 already in use
```bash
sudo fuser -k 8069/tcp
```

### PostgreSQL connection refused
```bash
sudo systemctl restart postgresql
```

### Permission denied on custom_addons
```bash
chmod -R 755 custom_addons
```

---

## 📎 Pro-Tip to Sound Smart (to boss/client)

> *"With `--dev=all` and targeted `-u` updates, we reduce the dev loop from minutes to seconds — faster iterations, faster feature delivery."*

---

Want me to turn this into a:
- 📄 PDF cheat sheet
- 🖥️ Bash alias file (e.g., `odoo-dev`, `odoo-update`)
- 🧩 VS Code snippet file?

Just say the word.