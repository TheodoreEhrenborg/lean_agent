# lean_agent

This repository uses [inspect](https://inspect.aisi.org.uk) to see how many
of the problems from
[mathematics_in_lean](https://github.com/leanprover-community/mathematics_in_lean/)
can be solved by an LLM.

## Quickstart

This will allow you to see the results of a sample evaluation, but it won't
install the larger dependencies that are necessary to run the evaluation.

1. Install [uv](https://github.com/astral-sh/uv) with `curl -LsSf https://astral.sh/uv/install.sh | sh`
1. Run `uv run inspect view --log-dir sample_logs`

## Full installation

1. Install [uv](https://github.com/astral-sh/uv) with `curl -LsSf https://astral.sh/uv/install.sh | sh`
1. The LLM agent runs in a Docker sandbox.
   To prepare the Docker image, run `./build_docker_image.bash`.
   This will take ~10 minutes and use up ~10 GB of disk space---it's
   downloading a cached version of [mathlib4](https://github.com/leanprover-community/mathlib4).
1. `uv sync` will handle the necessary Python dependencies.

## Configuration

Put this in `.env`:

```sh
ANTHROPIC_API_KEY=<secret key here>
INSPECT_EVAL_MODEL=anthropic/claude-3-5-sonnet-latest
```

(i.e. `.env` should match `.env.example`, but with values filled in)

If you want to use a different provider, adjust the environment variables
as described [here](https://inspect.aisi.org.uk/#getting-started),
and hence update the Python dependencies (e.g. `uv add openai`).

## Running the eval

`uv run inspect eval run_eval.py`

You can restrict to only a few samples using `--limit`
(see [here](https://inspect.aisi.org.uk/options.html) for the full list of options).

## Viewing results

`uv run inspect view`

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
- Does `lake build` have an option to produce more structured output (e.g. when talking to an IDE)?

## How to run on NixOS

uv doesn't work well on machines that don't follow the Filesystem Hierarchy Standard (e.g. NixOS).
The solution is to run commands in a separate development docker container:

1. Run `./build_docker_image.bash` as before
1. Run `./build_dev_image.bash`
1. Enter the container with `./run_dev_container.bash -v /var/run/docker.sock:/var/run/docker.sock -p 7575:7575`. The port is necessary for viewing results. The socket allows this development container to spin up sandboxes for the LLM agent.
1. Inside this container, uv will work as described above. Then inside the container you can run `uv run ...` as before. When viewing results, use `uv run inspect view --host 0.0.0.0`.
