# pic-deliver
picture haishin tool

## dependencies

- python >= 3.2
- pipenv

## Setup

```sh
$ pipenv install
```

## deploy and run
1. install above packages
2. set base url in `config.py`
3. `$ pipenv run python3 app.py`

### gunicorn
`$ pipenv run gunicorn app:app --bind <address>`
