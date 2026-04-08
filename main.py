from fastapi import FastAPI

# Initialize FastAPI app

app = FastAPI(title="AURA AI Agent")

# Health check endpoint

@app.get("/")
def health_check():
    return {"status": "AURA AI Agent is running 🚀"}

# Future endpoint placeholder

@app.post("/run-agent")
def run_agent():
    return {"message": "Agent execution coming soon"}
