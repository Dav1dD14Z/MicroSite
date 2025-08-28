from fastapi import FastAPI, HTTPException, status

app = FastAPI()

@app.get("/")
def start():
    return {"message": "Hi class"}