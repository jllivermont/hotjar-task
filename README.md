# Quickstart
Here is an example of how a survey response can be created, queried, updated and completed using command line curl:

```bash
$ curl -X POST https://hotjar-task.herokuapp.com/survey -d '{"name": "Vladimir Putin", "email": "vlad@russia.ru"}' -H 'Content-Type: application/json'
{"id": 5}
$ curl -X GET https://hotjar-task.herokuapp.com/survey/5
{"about_me": null, "id": 5, "address": null, "finished": false, "name": "Vladimir Putin", "email": "vlad@russia.ru", "age": null, "favorite_colors": null, "favorite_book": null, "gender": null} 
$ curl -X PUT https://hotjar-task.herokuapp.com/survey/5 -d '{"favorite_book": "Inferno"}' -H 'Content-Type: application/json'
$ curl -X PUT https://hotjar-task.herokuapp.com/survey/5 -d '{"age": "28", "about_me": "I love chicken wings"}' -H 'Content-Type: application/json'
$ curl -X PUT https://hotjar-task.herokuapp.com/survey/5 -d '{"finished": "true"}' -H 'Content-Type: application/json'
$ curl -X GET https://hotjar-task.herokuapp.com/survey/5
{"about_me": "I love chicken wings", "id": 5, "address": null, "finished": true, "name": "Vladimir Putin", "email": "vlad@russia.ru", "age": 28, "favorite_colors": null, "favorite_book": "Inferno", "gender": null}
```

# API Documentation
## POST /survey (CREATE)
* Required request headers: `application/json`
* Required request body parameters: `name` and `email`
* Example request payload: `{"name": "Jon Snow", "email": "jon@got.com"}`
* Response format: `application/json`
* Response body parameters: `id`
* Example response payload: `{"id": 293292}` 
* HTTP response codes: `201`, `400`, `409`, `500`

## PUT /survey/{id} (UPDATE)
* Required request headers: `application/json`
* Allowed request body parameters: `name`, `age`, `about_me`, `address`, `gender`, `favorite_book` and `favorite_colors`
* Example request payload: `{"name": "Jon Snow", "address": "The Wall, The North, Westeros", "favorite_colors": "black,red,purple"}`
* Response format: None
* Response body parameters: None
* Example response payload: None
* HTTP response codes: `200`, `400`, `500`

## GET /survey/{id} (READ)
* Required request headers: None
* Allowed request body parameters: None
* Example request payload: None
* Response format: `application/json`
* Response body parameters: `id`, `name`, `email`, `age`, `about_me`, `address`, `gender`, `favorite_book`. `favorite_colors` and `finished`
* Example response payload: `{"email": "test@google.com", "about_me": "I love chicken wings", "finished": true, "id": 4, "age": 28, "name": "Nancy Reagan", "address": null, "gender": "female", "favorite_colors": "brown,yellow", "favorite_book": "Bridge to Terabithia"}`
* HTTP response codes: `200`, `400`, `500`

## GET /surveys (BULK READ)
* Required request headers: None
* Allowed request body parameters: None
* Example request payload: None
* Response format: `application/json`
* Response body parameters: `id`, `name`, `email`, `age`, `about_me`, `address`, `gender`, `favorite_book`. `favorite_colors` and `finished`
* Example response payload: `[{"email": "test@google.com", "about_me": "I love chicken wings", "finished": true, "id": 4, "age": 28, "name": "Nancy Reagan", "address": null, "gender": "female", "favorite_colors": "brown,yellow", "favorite_book": "Bridge to Terabithia"}]`
* HTTP response codes: `200`, `400`, `500`

# Technology Stack
## Back-end
- [python] - Lots of awesomeness!
- [postgresql] - RDBMS
- [peewee] - ORM
- [falcon] - WSGI-compatible web framework
- [gunicorn] - HTTP Server

## Front-end
- [angular] - Declarative web app framework
- [jquery] - JS pocket knife (Go MacGyver!)
- [twitter-bootstrap-wizard] - Tab-based form wizard

## Managed Services
- [heroku] - Cloud hosting
- [github] - Source control
- [circleci] - Continuous integration
- [pusher] - Real-time messaging

[angular]: <https://angularjs.org/>
[circleci]: <https://circleci.com/gh/jllivermont/hotjar-task>
[falcon]: <https://falcon.readthedocs.io/en/stable/>
[github]: <https://github.com/jllivermont/hotjar-task>
[gunicorn]: <http://gunicorn.org/>
[heroku]: <https://hotjar-task.herokuapp.com>
[jquery]: <https://jquery.com/>
[peewee]: <http://docs.peewee-orm.com/en/latest/>
[postgresql]: <https://www.postgresql.org/>
[pusher]: <https://pusher.com/>
[python]: <https://docs.python.org/3/>
[twitter-bootstrap-wizard]: <https://github.com/VinceG/twitter-bootstrap-wizard>
