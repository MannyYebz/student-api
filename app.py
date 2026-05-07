from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/v1/ghana/items/{item_id}")
def read_item(item_id: int, q: str):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    # uvicorn.run(app, host="localhost", port=27017)
    uvicorn.run("app:app", host="0.0.0.0", port=5001, reload=True)