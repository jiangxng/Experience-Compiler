# LLM Replacement and Inheritance

Changing a model is changing a reasoning processor, not replacing EC memory. New models receive Constitution, role, task, relevant context, Learning Strategy versions, past strategy evaluations, known failure modes, available EVO commands and Eidos capabilities.

Run shadow evaluation before migration: same frozen Context Packs -> old/new model -> structured comparison on correctness, citation faithfulness, policy compliance, latency, cost and decision outcomes. Roll out by risk class, then retire the old adapter.
