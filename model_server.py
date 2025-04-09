import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Personal LLM API")

# Model configuration
MODEL_ID = os.getenv("MODEL_ID", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "512"))
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load model and tokenizer
@app.on_event("startup")
async def startup_event():
    global model, tokenizer
    print(f"Loading model {MODEL_ID} on {DEVICE}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, 
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
        low_cpu_mem_usage=True
    )
    model.to(DEVICE)
    print("Model loaded successfully!")

# Define request/response models
class GenerationRequest(BaseModel):
    prompt: str
    max_length: int = MAX_LENGTH
    temperature: float = 0.7
    top_p: float = 0.9

class GenerationResponse(BaseModel):
    text: str

# Endpoint for text generation
@app.post("/generate", response_model=GenerationResponse)
async def generate_text(request: GenerationRequest):
    try:
        inputs = tokenizer(request.prompt, return_tensors="pt").to(DEVICE)
        
        generation_args = {
            "max_length": request.max_length,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "do_sample": True
        }
        
        with torch.no_grad():
            outputs = model.generate(**inputs, **generation_args)
        
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return GenerationResponse(text=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run with: uvicorn model_server:app --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
