#!/bin/bash
#SBATCH -p GPU              # partition (queue)
#SBATCH -N 1                # number of nodes
#SBATCH -t 0-36:00          # time (D-HH:MM)
#SBATCH -o slurm.%N.%j.out  # STDOUT
#SBATCH -e slurm.%N.%j.err  # STDERR
#SBATCH --gres=gpu:1        # request one GPU

# Initialize and activate Conda environment
if [ -f "/usr/local/anaconda3/etc/profile.d/conda.sh" ]; then
    . "/usr/local/anaconda3/etc/profile.d/conda.sh"
    conda activate test_env
else
    export PATH="/usr/local/anaconda3/bin:$PATH"
    conda activate test_env
fi


python  -u form2text_usage.py

