#!/bin/bash
cd ~/semantic_uncertainty_dev
for DS in squad bioasq nq svamp; do
  if [ -f cluster_stats/Llama-2-7b-chat_${DS}.json ]; then
    echo "SKIP: $DS already has results"; continue
  fi
  echo "RUNNING: $DS"
  python semantic_uncertainty/generate_answers.py --model_name=Llama-2-7b-chat --dataset=$DS --num_generations=50 --no-get_training_set_generations --no-compute_p_ik --no-compute_p_true > run_dev_${DS}.log 2>&1
  echo "EXIT $? : $DS"
done
