from fastapi import FastAPI
from techhub.fastapi_routes import app as fastapi_app  # Import the FastAPI app

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to TechHub!"}

# Mount the FastAPI app under a subpath
app.mount("/api", fastapi_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)