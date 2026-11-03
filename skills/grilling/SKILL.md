---
name: grilling
description: Stress-test a plan, decision, or idea through a probing interview. Use when the user says "grill me", asks to be grilled, or wants their thinking challenged before proceeding.
---

# Grilling

Your goal is to understand what the user means and wants as well as they do. Keep questioning until you get there; don't settle for agreement. The topic may be a firm plan or a half-formed problem. Either way, understand it before proposing anything.

Lay the topic out as a **design tree**: each decision, and the decisions that hang on its answer.

Question in **rounds**. The **frontier** holds the decisions you can put to the user now, because everything they depend on is settled. Each round asks the whole **frontier** at once, then stops for answers. Hold back any question whose wording or recommendation would change with an answer you're still waiting on.

Lay out each round like this:

```
**1. <short title>**
<the question, in concrete terms; list the options when there are several>

**Recommended:** <your answer and why, in a sentence>
```

Phrase each question so a plain "yes" takes your recommendation.

Look up facts yourself; leave judgments to the user. Check code, documents, or tools only when a **frontier** question depends on what they say, using a fresh-context sub-agent if you can. Ask whatever doesn't depend on the lookup while it runs.

Once answers arrive, update the **design tree** and work out the new **frontier**. Reopen earlier decisions a new answer undermines. Test vague answers against a concrete case.

Stop when the **frontier** is empty and no branch rests on an assumption the user hasn't confirmed. List what was decided and ask whether it matches their understanding. Wait for that confirmation before acting.
