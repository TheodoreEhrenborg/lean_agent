# lean_agent

TODO blurb

https://github.com/leanprover-community/mathematics_in_lean/

## Installation

### With uv

This repo uses [uv](https://github.com/astral-sh/uv) for packaging,

1. Install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
1. Run scripts using `uv run`. TODO
   The first time you call uv, it will download all the necessary dependencies.

### With docker

uv doesn't work well on machines that don't follow the Filesystem Hierarchy Standard (e.g. NixOS).
To run uv in this case, use the provided Dockerfile:

1. Build the image with `./build.sh` TODO
1. Enter the container with `./run.sh`. If you have GPUs, instead use `./run.sh --gpus all` TODO
1. To mount a results directory, use `./run.sh -v /absolute/host/path/to/results/:/results` TODO
1. Then inside the container you can run `uv run ...` as before

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
