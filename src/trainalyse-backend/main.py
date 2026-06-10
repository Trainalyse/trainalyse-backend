from workers import WorkerEntrypoint  # cloudflare native libarary
import asgi  # for building asyncronous api
from fastapi import FastAPI, Depends
from auth import check_dev_token

app = FastAPI(
    dependencies=[Depends(check_dev_token)]
)  # only allow access to the api when token is valid


@app.get("/")
async def main():
    return {"status": "cum"}


class Default(WorkerEntrypoint):
    # fetch is trigger for http request
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)
