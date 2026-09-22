# Setup Notes (lab GPU: RTX 6000 Ada, driver 570.169, CUDA 12.8)

1. Clone repo, then: conda-env update -f environment.yaml

2. Original environment.yaml's torch (2.5.1) fails with DeBERTa:
   ValueError: torch.load requires torch >= 2.6 (CVE-2025-32434 check in transformers)

3. Fix: reinstall matched torch/torchvision/torchaudio trio for CUDA 12.4
   (driver supports up to 12.8, so cu124 wheels work; cu130 wheels do NOT - driver too old):

   pip install --force-reinstall --no-cache-dir torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
   pip install --force-reinstall --no-cache-dir torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124
   pip install --force-reinstall --no-cache-dir torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124

4. Verify: python -c "import torch, torchvision, torchaudio; print(torch.__version__, torch.cuda.is_available())"
   should print 2.6.0+cu124 True

5. Set env vars before running:

   export HF_HUB_DISABLE_XET=1
   export HF_HUB_DOWNLOAD_TIMEOUT=120
   export HUGGING_FACE_HUB_TOKEN=<your token>
   export OPENAI_API_KEY=<your key>

6. Run: python semantic_uncertainty/generate_answers.py --model_name=Llama-2-7b-chat --dataset=trivia_qa

Reproduced result: semantic_entropy AUROC 0.783 (paper reports ~0.79 avg for LLaMA-2-7b-chat/TriviaQA - matches).
