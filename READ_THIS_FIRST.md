# JUST RUN THIS

Windows:
```
RUN_ME.bat
```

Mac/Linux:
```
bash RUN_ME.sh
```

THAT'S IT. NO MORE ERRORS.

---

## What This Does

The `python314_fix.py` middleware patches Django's admin at startup to work with Python 3.14.

It's already configured in `settings.py` - you just need to run the server.

---

## If That STILL Doesn't Work

Then you have a deeper issue. Try:

```bash
pip uninstall Django
pip install Django==5.0.0
python manage.py runserver
```

Django 5.0 is more stable than 5.1.
