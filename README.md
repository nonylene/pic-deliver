# pic-deliver
picture haishin tool

## dependencies

- python >= 3.2

### pip
- bottle
- peewee
- jinja2

## deploy and run
1. install above packages
2. set base url in `config.py`
3. `python3 app.py`

### gunicorn
`gunicorn app:app --bind <address>`
