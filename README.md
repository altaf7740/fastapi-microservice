# Sample App

## Follow this to run app
- create `.env` file from `.env.example` and adjust it.
- build app `make app-build`
- run app `make app-run`

Now connect to container using `docker exec -it <container name> bash`
- generate migrations `make generate-migrations`
- migrate it `make migrate`