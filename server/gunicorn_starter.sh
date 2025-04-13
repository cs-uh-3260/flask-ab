# note that i'm using --reload  here so changes are reflected right
# away during development without having to stop and start the containers
# this is not a setting you should have in production
gunicorn --reload --bind 0.0.0.0:6969 app:app