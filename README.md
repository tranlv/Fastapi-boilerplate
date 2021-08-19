# hoovada-fastapi

### How to run

- Create python virtual environment
- Install dependencies
```
$ pip install -r app/requirements.txt
```
- Edit `.env` and set the equivalent variable
- Activate environment variables
```
$ source .env
```

- Init the database (do this only for the first time)
```
$ make prestart-db-init
```
- Run the app:
```
$ make run
```

- Open browser at: `http://localhost:8000/docs`
- Authentication
	+ Login at `api/v1/login/access-token` with username, pass predefined in `.env`
	+ Add header `Authorization`: `Bearer {{access_token}}` for any request
