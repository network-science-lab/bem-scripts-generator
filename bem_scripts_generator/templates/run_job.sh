#!/bin/bash

#SBATCH -N1
#SBATCH -c1
#SBATCH --mem={{ memory }}
#SBATCH --time={{ time }}

#SBATCH -o slurm_output/slurm-%j.out
#SBATCH -e slurm_output/slurm-%j.out

#SBATCH --mail-user=pirog.adam@gmail.com
#SBATCH --mail-type=ALL

#SBATCH --job-name={{job_name}}

{{ python_path }} -m influence_simulator \
    {{ dataset_path }} \
    {{ config_path }} \
    -o {{ output_path }} \
    --n-jobs 1
