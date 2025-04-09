# Personal LLM Hosting

This project allows you to host your own Large Language Model (LLM) and access it through a REST API.

## Setup

### Using Conda (Recommended)

1. Create and activate the conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate llm-server
   ```

2. Verify the installation:
   ```bash
   python -c "import torch; print(f'PyTorch version: {torch.__version__}, CUDA available: {torch.cuda.is_available()}')"
   ```

### Alternative: Using Pip

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the model:
   - Edit the `.env` file to change the model ID or parameters
   - Default model is TinyLlama-1.1B-Chat, but you can use any model from Hugging Face

## Running the Server

Start the server with:
```bash
python model_server.py
```
or
```bash
uvicorn model_server:app --host 0.0.0.0 --port 8000
```

## Using the API

Use the included client script:
```bash
python client.py --prompt "Tell me about artificial intelligence"
```

Or make a direct API call:
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me about artificial intelligence", "max_length": 512, "temperature": 0.7}'
```

## Deployment Options

### On a Cloud VM (e.g., AWS EC2, Google Cloud, Azure)

1. Set up a VM with Miniconda/Anaconda and required dependencies
2. Clone this repository to the VM
3. Follow the conda setup steps above
4. Configure your VM's security group/firewall to allow traffic on port 8000
5. Run the server with the host set to `0.0.0.0`
6. Access your API using your VM's public IP address

### Using Docker

A Dockerfile is included for containerized deployment. Build and run with:
```bash
docker build -t personal-llm .
docker run -p 8000:8000 personal-llm
```
