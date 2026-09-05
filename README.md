# Reagent BioCrypt

This repository contains the completed computational work for the **re:AGENT
2026 BioCrypt project**.

The project asked whether a DNA message register could:

1. respond to three inputs in the required forward order, `A → B → C`;
2. rearrange its DNA into a final encoded state;
3. reverse those operations in the order `C → B → A`; and
4. return to the original DNA sequence exactly, byte for byte.

The proposed system uses three large serine integrase channels in
non-pathogenic *Escherichia coli* K-12:

- Bxb1 integrase with gp47 RDF;
- phiC31 integrase with gp3 RDF;
- TP901-1 integrase with Xis.

Integrases perform the forward DNA inversions. Recombinase directionality
factors, or RDFs, enable the corresponding reverse reactions.

## End result

The repository is the final computational deliverable, not a synthesis-ready
wet-lab design.

The deterministic simulator showed that:

- forward `ABC` reaches the intended final state;
- reverse `CBA` restores the original sequence exactly;
- all other forward and reverse orders fail to complete;
- wrong orders can create deletion/excision substrates, so strict state and
  input gating is required;
- all **280 hard computational constraints** pass; and
- the automated test suite contains **30 passing tests**.

The design still requires experimental validation of recombinase crosstalk,
RDF specificity, regulatory leakage, state-gate behavior, host integration,
expression, and repeated-cycle reliability.

## Main deliverables

The three primary sequence records are available in both GenBank and FASTA
formats:

| Record | Purpose | Length |
|---|---|---:|
| `design_v1/sequences/01_message_register.gb` | DNA message cassette | 966 bp |
| `design_v1/sequences/02_forward_controller.gb` | expresses the forward integrases | 9,584 bp |
| `design_v1/sequences/03_reverse_controller.gb` | expresses integrases with their RDFs | 10,727 bp |

Seven additional GenBank/FASTA records in `design_v1/states/` represent every
step from the initial register through encryption and exact restoration.

## Repository contents

```text
.
├── REPORT.md
│   Literature review, architecture rationale, risks, and experimental plan
├── simulate.py
│   Original deterministic symbolic simulator
├── simulation_results.json
│   Results from the original simulator
└── design_v1/
    ├── sequences/
    │   Three primary message and controller records
    ├── states/
    │   Seven physical message-state records
    ├── src/
    │   Topology, controller, validation, optimization, and export code
    ├── tests/
    │   Automated tests and deliberately invalid fixtures
    ├── configs/
    │   Channel, host, constraint, and model-run definitions
    ├── candidates/
    │   Pareto-ranked neutral payload alternatives
    ├── reports/
    │   Validation, comparison, topology, model, and risk reports
    ├── artifacts/
    │   Provenance records, model inputs/outputs, manifests, and hashes
    ├── references.bib
    │   Machine-readable literature references
    ├── assumptions.yaml
    │   Explicit assumptions and unresolved inputs
    └── design_decisions.md
        Explanation of the selected architecture and its limitations
```

## Recommended starting points

- [`REPORT.md`](REPORT.md), full project background and literature review.
- [`design_v1/reports/validation_report.md`](design_v1/reports/validation_report.md),
  concise computational verdict and evidence boundaries.
- [`design_v1/design_decisions.md`](design_v1/design_decisions.md), why this
  architecture, channel set, and sensor set were selected.
- [`design_v1/reports/unresolved_risks.md`](design_v1/reports/unresolved_risks.md),
  experimental blockers and release criteria.
- [`design_v1/artifacts/package_manifest.json`](design_v1/artifacts/package_manifest.json),
  SHA-256 checksums for the reproducibility package.

## Analyses performed

### Deterministic analyses

Custom Python and Biopython code handled:

- typed attachment-site topology and exact recombination chemistry;
- all forward and reverse input permutations;
- exact sequence restoration;
- controller truth tables and fail-closed input behavior;
- GenBank/FASTA export and parse-back validation;
- CDS translation and sequence provenance checks;
- GC, repeat, homopolymer, motif, restriction-site, ORF, and host-site scans;
- neutral-payload Pareto optimization; and
- complete package hashing.

### Proto model analyses

- **ESM-2 15B** compared the three integrases and three RDFs using protein
  embeddings. It helped prioritize crosstalk experiments but did not prove
  biological orthogonality.
- **ViennaRNA** folded nine translation-initiation windows to flag possible RNA
  structures that could affect protein expression. The regulatory sequences
  remain placeholders, so this did not validate expression.

Neither model changed the selected design. The exact `ABC → CBA` proof comes
from the deterministic topology simulator.

## Reproducing the computational checks

Python 3.11 or newer is recommended.

```bash
cd design_v1
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/build_constructs.py
python src/run_model_scoring.py
python src/finalize_package.py
pytest -q
ruff check src tests
ruff format --check src tests
```

Captured model outputs are already included. Rebuilding the deterministic
artifacts does not require rerunning the remote models.

## Important limitation

This repository demonstrates computational consistency and exact symbolic
reversibility. It does **not** demonstrate that the complete system works in
cells, and its placeholder regulatory parts must not be treated as
synthesis-ready sequences.
