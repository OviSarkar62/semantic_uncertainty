#!/bin/bash
MODEL=$1
cd ~/semantic_uncertainty_dev
for DS in trivia_qa squad bioasq nq svamp; do
  if [ -f cluster_stats/${MODEL}_${DS}.json ]; then
    echo "SKIP: $MODEL $DS already has results"; continue
  fi
  echo "RUNNING: $MODEL $DS"
  python semantic_uncertainty/generate_answers.py --model_name=$MODEL --dataset=$DS --num_generations=50 --no-get_training_set_generations --no-compute_p_ik --no-compute_p_true > run_dev_${MODEL}_${DS}.log 2>&1
  echo "EXIT $? : $DS"
done
