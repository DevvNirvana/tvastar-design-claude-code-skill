# Contributing to Tvastar

Thank you for improving the world's best frontend design skill.

## What makes a good contribution

The bar is: does this make Tvastar produce **better, more varied output** than it did before?  
Not: does this add more code.

---

## Types of contributions

### 🏆 High Impact
- **New library** — Adds a library that fills a gap (new interaction type, new use case)
- **New style profile** — Adds an aesthetic that produces genuinely different output
- **Bug fix** — Makes the skill produce correct code instead of broken code
- **New lint rule** — Catches a real bug that ships undetected

### ✅ Good
- **Reference file updates** — Keeps a library's section current
- **New page pattern** — Adds a layout blueprint for a real page type
- **Test improvement** — Better coverage for edge cases

### 🟡 Minor
- **Typo fixes** — Still welcome
- **Documentation** — Always useful

---

## Adding a new library

1. **Add to `LIBRARY_CATALOG`** in `scripts/core.py`:
   ```python
   "your-library": {
       "name": "Your Library",
       "url": "https://your-library.com",
       "install_method": "npm install your-library",
       "requires": ["tailwindcss"],
       "best_for": ["specific-use-case"],
       "style_fit": ["Dark Aurora Premium", "Gaming Cyber"],
       "components": {
           "category": [
               {"name":"ComponentName","desc":"What it does","wow_factor":8},
           ]
       }
   }
   ```

2. **Add slot logic** in `select_components()`:
   ```python
   # In the relevant slot (background, hero_text, feature_cards, etc.)
   elif is_your_context:
       slot = {"lib":"your-library","component":"ComponentName",
               "reason":"Why this is right here"}
   ```

3. **Add lint rules** if the library has gotchas (in `framework_lint.py`):
   ```python
   "your-library": [
       {"id":"YL001","severity":"High","rule":"Rule name",
        "pattern":r"regex_pattern","message":"Human-readable explanation"},
   ]
   ```

4. **Add reference section** in `references/component-library-catalog.md`

5. **Add search strategy** in `references/resources-blogs.md`

6. **Run tests** — all 164 must pass:
   ```bash
   python3 scripts/test_all.py
   ```

---

## Adding a new style profile

In `scripts/core.py`, add to the `STYLES` list:
```python
{"name":"Your Style Name",
 "vibe":"keyword1 keyword2 keyword3 ...",
 "bg_approach":"How to describe the background approach",
 "effects":"comma, separated, effects, to, use",
 "anti_patterns":"what, to, avoid",
 "react_bits":["ComponentA","ComponentB"],
 "aceternity":["ComponentC"],
 "magicui":["ComponentD","ComponentE"],
 "shadcn":["Card","Button"],
 "primary_lib":"magicui"},  # or react_bits, aceternity, shadcn
```

The `primary_lib` controls which library gets priority when select_components() resolves conflicts.

---

## Running tests

```bash
# Full suite
python3 scripts/test_all.py

# Single module
python3 scripts/test_all.py --module core
python3 scripts/test_all.py --module lint_2026

# Syntax check
for f in scripts/*.py; do python3 -m py_compile "$f"; done
```

164 tests must pass. No exceptions.

---

## PR checklist

- [ ] `python3 scripts/test_all.py` passes (164/164)
- [ ] All scripts syntax-check clean
- [ ] SKILL.md updated if commands or READ triggers changed
- [ ] Reference files updated if new libraries added
- [ ] Tests added for new functionality

---

## Questions?

Open an issue. We're friendly.
