import asyncio
from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.scorer import Score, accuracy, scorer
from inspect_ai.agent import react
from inspect_ai.tool import bash_session, text_editor
from inspect_ai.util import sandbox

# Define the MIL.lean files and the target files to be fixed
# TODO This should use the actual MIL files instead of making some up
SAMPLE1_MIL = """import MIL.C02_Basics.S01_Calculating"""




SAMPLE2_MIL = """import MIL.C02_Basics.S02_Proving_Identities_in_Algebraic_Structures"""

@scorer(metrics=[accuracy()])
def lean_proof_scorer():
    async def score(state, target):
        # Run lake build to check if proofs are valid
        build_result = await sandbox().exec(["lake", "build"])
        if not build_result.success:
            return Score(value=0, explanation=f"lake build failed: {build_result.stderr}")

        # Check for remaining sorries
        check_sorries = await sandbox().exec(["bash", "-c", "lake build | grep sorry"])
        has_sorries = "sorry" in check_sorries.stdout

        if has_sorries:
            return Score(value=0, explanation="The file still contains sorries")

        return Score(value=1, explanation="All proofs are valid")

    return score

@task
def evaluate_lean_fixing():
    dataset = MemoryDataset([
        Sample(
            input="Fix the Lean file by replacing all 'sorry' statements with valid proofs. Run 'lake build' to check your work. Repeat until there are no more sorries.",
            files={
                "MIL.lean": SAMPLE1_MIL,
            },
        ),
        Sample(
            input="Fix the Lean file by replacing all 'sorry' statements with valid proofs. Run 'lake build' to check your work. Repeat until there are no more sorries.",
            files={
                "MIL.lean": SAMPLE2_MIL,
            },
        )
    ])

    lean_agent = react(
        description="Expert Lean theorem prover",
        prompt="""
        You are an expert in the Lean theorem prover. Your task is to fix Lean files by replacing 'sorry' statements with valid proofs.

        Follow these steps:
        1. Run 'lake build' to see the current state of the project
        2. Examine the file that needs to be fixed
        3. Replace each 'sorry' with a complete proof
        4. Run 'lake build' again to verify your proofs
        5. If there are still errors or sorries, fix them and repeat

        Tips for writing proofs in Lean:
        - Use tactics like 'rw', 'induction', 'cases', 'simp', etc.
        - For simple arithmetic properties, try 'rw' with existing theorems
        - For inductive proofs, use 'induction' followed by appropriate tactics
        - When you're done, make sure 'lake build | grep sorry' returns nothing
        """,
        # TODO Should the timeout be larger?
        tools=[bash_session(), text_editor()],
        attempts=3,
    )

    return Task(
        dataset=dataset,
        solver=lean_agent,
        scorer=lean_proof_scorer(),
        sandbox=("docker", "docker/Dockerfile")
    )
