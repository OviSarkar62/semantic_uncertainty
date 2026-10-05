#!/bin/bash

MODELS=("Llama-2-7b-chat" "Llama-2-13b-chat" "Llama-2-70b-chat" "falcon-7b-instruct" "falcon-40b-instruct" "Mistral-7B-Instruct-v0.1")
DATASETS=("trivia_qa" "squad" "bioasq" "nq" "svamp")

LOGDIR=~/semantic_uncertainty/run_logs
mkdir -p "$LOGDIR"

for MODEL in "${MODELS[@]}"; do
  for DATASET in "${DATASETS[@]}"; do
    LOGFILE="$LOGDIR/${MODEL}_${DATASET}.log"

    if [ -f "$LOGDIR/${MODEL}_${DATASET}.done" ]; then
      echo "SKIP: $MODEL / $DATASET already completed"
      continue
    fi

    echo "=================================================="
    echo "RUNNING: $MODEL on $DATASET"
    echo "=================================================="

    python semantic_uncertainty/generate_answers.py --model_name="$MODEL" --dataset="$DATASET" > "$LOGFILE" 2>&1
    STATUS=$?

    if [ "$STATUS" -eq 0 ]; then
      touch "$LOGDIR/${MODEL}_${DATASET}.done"
      echo "DONE: $MODEL / $DATASET"
    else
      echo "FAILED: $MODEL / $DATASET (exit $STATUS) -- see $LOGFILE"
    fi
  done
done

echo "All combinations attempted. Check $LOGDIR for logs."
