---
name: ground
description: Work out what to build before building it by interviewing the user, ending in ground/product.md and ground/design.md: a project map the user can hold in their head plus the details downstream work needs. Use when the user invokes ground, wants to plan a new project or large idea up front, doesn't yet know the depth of what they're building, or wants unknowns surfaced before implementation starts.
---

# Ground

The goal is for the user to understand what is being built, why, what its main pieces are, and how they connect, with enough detail under each piece that an agent or engineer can start from it. The user is the decider: a decision enters the files only after they confirm it. Ground works above change-level specs: stop short of scenario-level behavior (GIVEN/WHEN/THEN), which downstream work writes per change. Acceptance checks are one-line observable outcomes. Do not create tickets or code.

**Done** means every piece has been settled (below) and the user can explain the project back, which you check by asking them to and comparing their account with the map. A gap is either an unclear map or a misunderstanding; say which and fix it. Then stop.

## Files

Read any existing `ground/` (or the folder the user names) and the repository first. Treat them as evidence, not decisions. Before research or the first question, create `ground/product.md` and `ground/design.md` if they are missing; saving needs no approval. Seed `product.md` with the user's intent and open questions, and `design.md` with a line saying design follows each piece's product section.

Each file opens with the **map**: a short summary, then the main pieces and how they connect. The two top-level files must answer what, why, which pieces, and how they connect without the reader opening anything else. Use a diagram or table wherever it shows something better than prose (Mermaid for flow and structure, ASCII or a mockup for layout); label unconfirmed items in it `(proposed)` too. The map must show how the pieces connect (what each shares with or needs from the others), not only list them. Show the project as a few large pieces: group features that share data or change together, and fold small ones into the piece they belong to. If your list of pieces mirrors the user's list of features, regroup. Detail follows in one section per piece.

- **Product section:** what the piece does for its users and why. Every product section has all four parts; write "None" only for open questions:

  ```
  ## <Piece>
  <what it does and why>
  **Decisions:** <each choice with its reason>
  **Acceptance checks:** <at least one observable outcome; mark it (proposed) if unconfirmed>
  **Open questions:** <questions about the piece itself, or None>
  ```

  Product holds only what a user can observe without knowing how it is built. Anything named after an implementation goes in design instead: stack, libraries, data model, file layout, config or wire formats, command syntax and flags, hashes, merge or conflict algorithms, git operations. "Reads one Markdown table and writes CSV" is product; "uses Python's standard library" and "last-writer-wins" are design. A piece whose product section would need such a term to be specific stays less specific, or the term goes to design.
- **Design section:** write nothing for a piece until its product section says "Open questions: None". Then write only what a builder could not infer from that product section and the conventions of the stack: flows, structure or mockups. Design adds no behavior a user could observe; if one is needed, put it in product first. Before saving a design section, reread the brief's constraints and the piece's product section (a runtime dependency, flag, or format they rule out stays out), and mark every design choice the user has not confirmed `(proposed)`. Do not describe the product section ("leaves no choice open"); write only the design. Stack choices, shared contracts and other cross-cutting technical decisions go in the top-level `design.md`; they belong to no piece, so they are not gated.

**Promotion.** When a piece cannot be understood from its section alone, or has pieces of its own worth mapping, propose moving it to `ground/areas/<name>/` with its own `product.md` and `design.md`, each opening with its own map. After the user agrees, move the detail there; the parent keeps the piece's summary, its place on the map, and a link to `areas/<name>`. Promoted areas can nest the same way. Propose new pieces and promotions among a round's questions and wait. Until the user agrees, create no `areas/` folder.

## What the files hold

The files describe the project as currently understood; they outlive this session. Edit in place; git is the history. Never write decision ids, round numbers, or who confirmed what, and never mention spikes or how something was learned: write "Hashing the files git lists gives the same value on every checkout, so evidence is tied to that hash", not "Spike result: hashing ... is stable". A resolved question becomes a plain statement with its reason. Open questions sit in the section they concern, state the question itself (never "see round 2"), and are deleted when resolved.

Anything you wrote that the user has not confirmed carries `(proposed)` until they confirm it. Unmarked prose must come from the user, the repository, or a recommendation they accepted: before saving, check each new unmarked sentence against that, and mark or cut every detail you added yourself, including plausible specifics and consequences you inferred. Never settle something the user said is undecided, and do not substitute an interim answer; list it as an open question.

## Each round

Each round: ask, wait, then update the files with the answers and save before you summarize. Interview with the `grilling` skill: ask everything you can ask now, each with a recommendation. Ask about the project; do not ask the user how the process should run. Stack and feasibility questions come first. Then work one piece at a time, product before design: a design question is not askable until that piece's product questions are answered, so keep it out of any round that still has product ones. If design shows a product section is wrong, reopen it. End each round by naming the sections you changed.

**Risk.** An unknown is risky if it is new to you or the user, depends on an unproven external system, is expensive to undo, or has other pieces depending on it. Say why; the user can overrule. Go deep on risk and skim the rest.

**Evidence.** A risky decision counts as made only with evidence such as a spike. Propose the spike, naming the question and what result would change the decision, and wait for a yes. Run it in a throwaway directory outside the repo. State what you learned in the files as a plain fact (evidence needs no marker); the decision it implies stays `(proposed)` until the user confirms it. If the user declines the spike, or decides a risky point without one, state the assumption plainly as a known risk.

## Settling a piece

A piece is settled when it has no open questions, passes both checks below, and the user has read it and said it is right. Before asking them to read it, run two checks with fresh-context subagents before asking the user to read it:

- **Readiness:** give it only that piece's files and the top-level map, never the conversation. It lists every question it would need answered and every assumption it would have to make, where the answer would change what gets built. Both lists must be empty: fix what you can, take the rest to the user, then run it again.
- **Invention audit:** give it the files and the conversation. It lists every settled claim with no basis in what the user said or accepted, or in the repository. Fix or mark each, then rerun readiness if the fix changed what gets built.

Then tell the user which file to read and wait for their go-ahead.
