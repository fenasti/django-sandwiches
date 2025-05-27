source venv/bin/activate

(venv) felipenastloyola@Mac django-sandwiches % heroku addons:attach desla::DATABASE_URL -a django-sandwiches
Attaching postgresql-defined-55192 to django-sandwiches... done
Setting DATABASE config vars and restarting django-sandwiches... done, v3

(venv) felipenastloyola@Mac django-sandwiches % heroku config:set GOOGLE_CREDS_JSON="$(< creds.json)" --app django-sandwiches