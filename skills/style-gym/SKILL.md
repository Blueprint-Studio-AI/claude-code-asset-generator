---
name: style-gym
description: Develop and evaluate reusable Blueprint Studio generation Styles against real briefs and visual references. Use when experimenting with Style prompts or building a new brand Style library.
---

# Style gym

An optional experiment loop using the existing Style and generation tools, not a separate model-training system. Adapt it to the task.

1. Read the current brand guide and nearby Styles. Inspect the actual reference assets. Define the visual traits to keep and what must vary between generations.
2. Choose a small set of different briefs before optimizing: one close to the reference and at least one new subject or composition. Keep model, quality, dimensions, and reference order fixed for comparisons.
3. Draft a compact reusable Style prompt. Put scene-specific instructions in the generation prompt. Keep official logos in versioned brand inputs rather than describing a substitute.
4. If authorized to create Styles in the workspace, create a distinctly named candidate with `create_style`; record its ID and assign the existing sidebar category when appropriate. Otherwise keep the candidate local. Do not overwrite a shared Style just to run an experiment.
5. Generate, download, and visually inspect outputs. Compare fidelity, response to the brief, diversity, logo/text accuracy, and practical usability. Record failures as well as successes; one matching output is not proof of a broadly useful Style.
6. Change one meaningful variable, rerun the same briefs, and keep the stronger version. Use `get_generation_details` and receipt IDs as evidence of settings. Provider results can vary even with identical settings.
7. Present the selected examples and limitations. Keep experiment notes with the project: brief, source links, candidate Style IDs, asset/receipt IDs, actual settings, observations, and next test. This lets another agent continue without the original chat.

Existing MCP `create_style` authors text-based Styles. Reference-set editing and formal Style-fork lineage are not exposed by that tool yet. Do not silently claim a text-only candidate has saved image references or ancestry. The tools can be composed directly without following this loop.
