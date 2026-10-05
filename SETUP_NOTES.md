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

## Updates from the K = 10 to 50 cluster study

Dataset fixes in semantic_uncertainty/uncertainty/data/data_utils.py:
- squad uses rajpurkar/squad_v2 (the bare squad_v2 id breaks newer huggingface_hub)
- nq uses google-research-datasets/nq_open
- the --dataset argument is nq, not nq_open

BioASQ needs a manual download:
- get training11b.json from https://zenodo.org/records/7655130
- put it in ~/semantic_uncertainty_dev/data/bioasq/
- export SCRATCH_DIR=/home/lab before running

Model names: Llama-2-7b-chat, Llama-2-13b-chat, Mistral-7B-Instruct-v0.1, falcon-7b-instruct.
Llama-2-70b-chat and falcon-40b-instruct do not fit in 49 GB in fp16 and were not run.

Study pipeline (50 samples per question, K = 10 to 50 are the first K samples):
1. ./run_dev_model.sh MODEL_NAME     (generation, saves cluster_stats/MODEL_dataset.json)
2. python build_count_index.py MODEL_NAME   (count index tables, descending K ... 1)
3. python build_excel.py MODEL_NAME         (one workbook per model)

Set HUGGING_FACE_HUB_TOKEN and OPENAI_API_KEY in the shell before running. Never put them in files.
