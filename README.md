# lean_agent

TODO blurb

https://github.com/leanprover-community/mathematics_in_lean/

## Installation

1. Install with [uv](https://github.com/astral-sh/uv) with `curl -LsSf https://astral.sh/uv/install.sh | sh`
1. The LLM agent runs in a Docker sandbox.
   To prepare the Docker image, run `./build_docker_image.bash`.
   This will take ~10 minutes and use up ~10 GB of disk space---it's
   downloading a cached version of [mathlib4](https://github.com/leanprover-community/mathlib4).
1. Then you can run the evaluation with `uv run inspect eval run_eval.py`. `uv` will handle the necessary Python dependencies.

## Viewing results

TODO

## Future work

- Some of the files from `mathematics_in_lean` should be filtered out, e.g. `MIL/C01_Introduction/S02_Overview.lean` contains Fermat's Last Theorem, which models are not currently able to prove
  - Although I saw Claude decide that this exercise was too hard, so Claude replaced it with an easier exercise
- There are no checks for cheating. The scorer should be upgraded to check that the models haven't modified the theorem statements, either using an LLM or parsing the code directly.
  - A sufficiently clever model might realize that there are solutions in the same folder. It would be interesting to measure this.
- The files from `mathematics_in_lean` often contain more than one exercise.
  LLMs sometimes struggle to fix all the exercises simultaneously and figure out which exercise is broken.
  Ideally I'd split the files so that there was one exercise per file. This could be done:
  - manually
  - using an LLM
  - writing some sort of hacky parser to look for `sorry`

## How to run on NixOS

uv doesn't work well on machines that don't follow the Filesystem Hierarchy Standard (e.g. NixOS).
The solution is to have a separate development docker container,
TODO
To run uv in this case, use the provided Dockerfile:

1. Build the image with `./build.sh` TODO
1. Enter the container with `./run.sh`. If you have GPUs, instead use `./run.sh --gpus all` TODO
1. To mount a results directory, use `./run.sh -v /absolute/host/path/to/results/:/results` TODO
1. Then inside the container you can run `uv run ...` as before

TODO Mount port and mount the docker socket
