# Paired novelty second-opinion protocol

Use this optional step for a contentious or high-stakes idea. Once enabled, run Codex and Hermes together. Do not ask only one provider and do not turn two opinions into a vote.

## 1. When to run it

Run the paired opinion when:

- per-claim deltas sit near a HIGH, MED, or LOW boundary;
- the idea is a thesis direction, funded milestone, or months-long commitment;
- the user requests an adversarial or external novelty read.

An exact published precedent does not need another vote. Keep the local retrieval verdict grounded in the paper itself.

## 2. Build the dossier from verified search results

Write `.writing/novelty-dossier.md`, or a temporary file when `.writing/` is absent. Include:

- the proposed idea;
- three to five atomic technical claims;
- verified candidate prior work with DOI, arXiv ID, PMID, URL, or Zotero key;
- exact source locators;
- the local per-claim delta;
- the questions: Is the claim novel? What is the closest work? What is the exact delta? Which recent paper might be missing?

Do not present the local verdict as the answer providers should confirm. Label it as a claim to challenge. Mark unresolved papers `[UNVERIFIED]` and include the needed verification action.

## 3. Run the paired consultation

Launch this command in the background with a Bash timeout of at least `660000` ms:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/paired_consult.py" \
  --cd "<absolute project root>" \
  --handoff-kind novelty \
  --PROMPT "Read <absolute path>/.writing/novelty-dossier.md and the cited original sources. Independently assess each claim's novelty, closest prior work, and exact delta. Do not modify files. Never invent an identifier or locator."
```

Do not poll. A successful result keeps the providers independent. A partial result retains the successful lane. A failed lane is never reconstructed from the other lane.

## 4. Present three separate reads

Use this fixed structure:

```markdown
## Local retrieval verdict
<per-claim assessment grounded in the verified search>

## Codex novelty view
<provider's claims, prior work, deltas, evidence, uncertainties, verification_needed>

## Hermes novelty view
<provider's claims, prior work, deltas, evidence, uncertainties, verification_needed>
```

Do not add a consensus or winner. Provider agreement may be noted as an observation, but it does not replace source verification. Provider disagreement tells the executor which paper to reopen.

Any new paper named by either provider enters `verification_needed` until its identifier resolves and the relevant original passage has been checked. Do not copy an unverified paper into the local prior-work table as fact.

## 5. Trace the result

Keep the dossier and, when the user wants persistence, save the paired handoffs beside the novelty report. Preserve provider provenance for every suggested paper and delta. The overall PROCEED, PROCEED-WITH-CAUTION, or ABANDON call remains the local advisory judgment shown to the user, not the output of a provider vote.
