from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def utama():
    return {"status": "HAYDEN API HIDUP"}
