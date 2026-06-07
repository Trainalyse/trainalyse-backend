from fastapi import FastAPI
from workers import WorkerEntrypoint  # cloudflare native libarary
import asgi  # for building asyncronous api

app = FastAPI()


@app.get("/")
async def main():
    return {"status": "cum"}


class Default(WorkerEntrypoint):
    # This specific naming structure maps directly to Cloudflare's W3C FetchEvent
    # fetch is trigger for http request
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)
