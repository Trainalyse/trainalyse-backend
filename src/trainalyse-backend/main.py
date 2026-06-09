from fastapi import FastAPI, Depends
from workers import WorkerEntrypoint  # cloudflare native libarary
import asgi  # for building asyncronous api
from auth import check_dev_token

app = FastAPI()


@app.get("/", dependencies=[Depends(check_dev_token)])
async def main():
    return {"status": "cum"}


class Default(WorkerEntrypoint):
    # fetch is trigger for http request
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)
