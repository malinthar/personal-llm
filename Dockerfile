FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install miniconda
RUN apt-get update && apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Add conda to path
ENV PATH /opt/conda/bin:$PATH

WORKDIR /app

# Install system dependencies for GPU support
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY environment.yml .

# Create conda environment
RUN conda env create -f environment.yml

# Make RUN commands use the conda environment
SHELL ["conda", "run", "-n", "llm-server", "/bin/bash", "-c"]

# Install additional GPU utilities in conda environment if not in environment.yml
RUN pip install nvidia-ml-py3

COPY . .

EXPOSE 8000

# Set environment variables for GPU
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# Run using the conda environment
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "llm-server", "uvicorn", "model_server:app", "--host", "0.0.0.0", "--port", "8000"]

# Label to indicate GPU support
LABEL com.nvidia.volumes.needed="nvidia_driver"
