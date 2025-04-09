FROM continuumio/miniconda3:latest

WORKDIR /app

COPY environment.yml .

# Create conda environment
RUN conda env create -f environment.yml

# Make RUN commands use the conda environment
SHELL ["conda", "run", "-n", "llm-server", "/bin/bash", "-c"]

COPY . .

EXPOSE 8000

# Run using the conda environment
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "llm-server", "uvicorn", "model_server:app", "--host", "0.0.0.0", "--port", "8000"]
