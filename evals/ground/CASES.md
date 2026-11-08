# Ground cases

These cases test whether `ground` leaves the user with a project map they can understand and a specification they
can trust without reading every line. Each task is a short conversation. The first message names the skill file
(the skill requires explicit invocation) and gives a brief; later messages are fixed replies. Baseline jobs send
the same messages with the skill file absent. Replies accept the agent's recommendations because a plain yes takes
the recommendation, so the checks apply to what the agent writes, not to how well it interviews.

Success for a trial means every step scores 1: each step's offline checks pass and, on the final step, every judge
criterion passes. Compare each task and agent across the baseline, the previous skill version and the current
skill. Treat a step that fails to run (timeout or infrastructure error) as invalid and rerun it.

## Expected shape

The skill is expected to produce `ground/product.md` and `ground/design.md` from the first turn. Each opens with a
map of the project: a short summary, the main pieces and how they connect, using a diagram or table where the
relationships need one. Sections give the detail below that. A piece that cannot be understood from its section
alone moves into `ground/areas/<name>/` with its own pair of files, and its parent keeps a summary and a link.
Content the user has not confirmed carries a `(proposed)` marker. The files hold current understanding only: no
decision ids and no account of how a decision was reached.

## verification-cli

[Task](tasks/verification-cli)

**Origin: observed failure, 2026-11-07.** In an interactive run of the previous `ground` skill, this brief
produced one specification file of about 500 lines before the work was close to done. It contained no diagram. The
user could not read all of it and could not tell whether the agent had written only what was agreed. The output
files were not created until the user asked for them after several rounds.

Expected: the files exist after the first turn; the top-level files carry a visual and can be understood on their
own; product content stays free of technical design; no decision ids or process history appear.

## invention

[Task](tasks/invention)

**Origin: observed concern, 2026-11-07.** The user could not be sure the agent was not writing things nobody had
agreed. The same brief runs, and one reply says how screenshots and videos are stored is undecided.

Expected: that decision does not appear as settled anywhere in `ground/`. An open question or a `(proposed)` option
is acceptable. Other settled claims must trace to the brief, the replies or what the agent proposed and the user
accepted.

## monolith

[Task](tasks/monolith)

**Origin: expected behavior for the new design; no observed failure yet.** A large brief with many parts that share
identity and must work offline. The top-level map should show a few large pieces and how they connect, not every
feature. No `areas/` folder may exist after the first turn, because the user has approved no promotion yet. Any
folder created later needs its own `product.md` and a link from its parent.

## small-stays-flat

[Task](tasks/small-stays-flat)

**Origin: expected behavior for the new design; no observed failure yet.** A one-tool brief. The result should be one
pair of files with no `areas/` folder and no padding. A diagram is not required.

## Grading limits

Offline checks run in the Reward Kit verifier and cover: the pair of files exists and has content; the retired
`spec.md` and `slices.md` are absent; no decision ids or process phrases appear (phrases such as "spike result", "confirmed by a spike", "round 2", "the user confirmed"; a forward-looking "needs a spike" is allowed); a visual (fenced diagram, table
or image) is present in the top-level files when the task requires one; no `areas/` before approval or in the small
case; every promoted area has a product file and a link from its parent. The process-language check is a list of
phrases, so it can miss paraphrases and can reject a legitimate use of a listed word.

A blinded Codex judge (`gpt-6.1-terra`) assesses the semantic criteria. It sees neither the condition name nor the
skill. All criteria must pass. Which criteria apply varies by task:

- `explain_back`: the two top-level files alone support the four answers (what, why as far as the brief gives a
  reason, pieces, connections).
- `invention`: every settled claim traces to the brief, the replies, an accepted recommendation, or the repository.
- `diagram`: a visual in the top-level files shows real relationships and agrees with the prose.
- `separation`: product content says what and why with acceptance checks (a piece that is only a name or one-line
  summary on the map needs none) and holds no implementation choice; design content does not contradict it, and no
  design detail is written for a piece whose own product section still lists open questions.
- `undecided_storage`: the user's undecided question is not settled in the files.
- `map_scale`: the top level shows a small set of large pieces, not a flat feature list.

The process-language check was tested directly on eight sentences, valid and invalid. Judge criteria were challenged with a valid reference, a valid alternative (ASCII diagram and different wording),
an option marked `(proposed)`, and near misses: an unmarked invented decision, process history, a decision id, the
retired layout, technical design in a product file, a diagram that contradicts the prose, a missing visual, an
unlinked area, a promotion before approval, and a map pushed out of the top-level files. All were classified as
intended.

What the suite does not establish: whether the interview itself is good (the replies are fixed), whether a map
helps a real person understand a project (the judge's explain-back is a proxy), or behavior on briefs and projects
unlike these four. The `invention` judge can only verify claims against the recorded conversation; it cannot
detect a true statement the agent learned elsewhere. Only the final step is judged, so a problem that appears and
is fixed in earlier steps is not caught.
