# in-class-10-01

starting point: <https://github.com/umn-5117-f18/in-class-10-01>

heroku setup:

```
heroku create
heroku addons:create heroku-postgresql:hobby-dev
# use `heroku pg:psql` and run `\i 'schema.sql'`
git push heroku master
heroku open
```

local setup:

```
# setup
pipenv install
# create .env with datastore connection params (see .env.example)

# run
pipenv shell
heroku local dev
```

heroku commands:

```
heroku logs --tail
heroku pg:psql
```
