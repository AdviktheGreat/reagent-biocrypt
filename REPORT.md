# Sequential, Externally Controlled DNA Rearrangement

**Evidence review, architecture decision, and deterministic topology analysis**  
**Review date:** 2026-08-15

## Executive decision

### Feasibility verdict

The requested behavior is **mechanistically feasible on one DNA molecule, but
not yet demonstrated as a complete biological system**.

The most defensible architecture is a **single-copy circular register with
three empirically screened, mutually orthogonal large-serine-integrase (LSI)
channels**. Each channel uses one cognate antiparallel `attB/attP` pair for its
forward inversion and the resulting `attL/attR` pair for the exact inverse
reaction. Forward chemistry uses integrase; reverse chemistry uses integrase
plus its cognate recombination directionality factor (RDF).

The design has three non-negotiable qualifications:

1. **A fourth direction/mode signal is needed for in-cell reversal.** The same
   three drugs can select channels A, B, and C, but they cannot by themselves
   tell an LSI channel whether to run `BP→LR` or `LR→BP`. A global
   encrypt/decrypt mode, or ex-vivo addition of RDF-containing inverse
   reagents, is the smallest honest modification.
2. **Input selection must be state-gated.** In the prescribed nesting, the
   Step-2 sites are parallel in the starting state, and the Step-3 sites are
   parallel after Step 1. Premature activity therefore deletes DNA rather than
   producing a benign wrong state.
3. **The three LSI/RDF channels cannot be named final until a complete
   pairwise crosstalk matrix is measured.** Bxb1/gp47 and φC31/gp3 are strong
   characterized candidates, and φBT1, TP901-1, SprA/SprB, and newer
   RDF-matched LSIs enlarge the panel. Published results show that enzyme/site
   orthogonality does not guarantee integrase/RDF orthogonality.

No primary paper located demonstrated three independently addressable,
ordered, exact-nucleotide reversible operations through a complete round trip.
The recommendation therefore composes directly demonstrated subsystems, but
the complete architecture remains an experimentally testable inference.

### Evidence labels

- **[D]** directly demonstrated in the cited system
- **[T]** transferred from a related host, topology, or component
- **[C]** deterministic computation in the accompanying artifact
- **[I]** mechanistic inference from established chemistry
- **[U]** untested design assumption

---

## 1. Missing inputs and assumptions

No image attachment was available in the workspace. The biological sequence
design is intentionally not synthesis-ready because the following are missing:

- exact host strain and its reference genome;
- chromosomal landing locus or complete episomal backbone;
- complete A–F payload sequences and whether their reverse complements retain
  the intended meaning;
- maximum register size and whether inversions may include transcriptional
  units;
- allowed markers, origins, and regulatory parts;
- acceptable fourth direction/mode input for decryption;
- intended storage time, cycle count, and tolerable mixed-state fraction;
- whether decryption must occur in the same cells or may be ex vivo;
- the empirically selected LSI/RDF trio and authoritative part records;
- required inducer concentrations and washout capabilities.

The deterministic simulation assumes one covalently closed circular molecule,
one copy, no mutation, exact conservative recombination, full cognate
specificity, and complete reactions. Those assumptions are explicitly relaxed
in the risk analysis, but no empirical kinetic parameters were invented.

---

## 2. Literature landscape

### Large serine integrases and reversible memory

- LSIs catalyze conservative, directionally controlled `attB × attP` exchange
  without relying on host double-strand-break repair. Bxb1 attachment-site
  identity and central-dinucleotide compatibility have been mapped
  mechanistically. **[D]** [R1, R2]
- Bxb1 gp47 changes reaction direction, favoring `attL × attR` and suppressing
  integration chemistry. **[D]** [R3]
- A Bxb1 integrase/RDF module repeatedly wrote and reset one chromosomal DNA
  memory bit in *E. coli*. **[D]** This is the closest direct precedent, but it
  is not a three-channel nested round trip. [R4]
- φC31 gp3-mediated reversal is established in biochemical and mammalian-cell
  contexts. **[D/T]** [R5, R6]
- Integrase–RDF fusion proteins and split-intein φC31 provide additional
  protein-level control concepts. **[D/T]** [R7, R8]
- The common assumption of perfectly irreversible integrase-only chemistry is
  false for all conditions: φC31 integrase-only excision has been observed at
  low frequency. **[D, falsifying]** [R9]
- Published 2024 data show variable noncognate LSI–RDF interactions. Orthogonal
  DNA sites are therefore insufficient evidence of orthogonal reverse
  channels. **[D, falsifying]** [R10]
- 2025 studies expanded experimentally identified RDF candidates but did not
  establish a three-channel repeated in-vivo round trip. **[D/T]** [R11, R12]

### Ordered memory and input control

- Eleven orthogonal integrase channels produced permanent, multiplexed memory
  in *E. coli*. **[D]** This supports channel scalability, not reversibility.
  [R13]
- Recombinase state machines directly encoded three-input event order in
  *E. coli*. **[D]** These devices are primarily irreversible history
  recorders, not exact decryptors. [R14]
- Marionette strains directly provide twelve optimized small-molecule sensors
  in *E. coli*, generally with large dynamic ranges. **[D]** Actual leakage,
  burden, and crosstalk must be remeasured with recombinase loads. [R15]
- Chemically and optically controlled split recombinases can reduce off-state
  activity in mammalian systems. **[D/T]** This evidence does not directly
  validate split LSI/RDF control in the proposed bacterial triple. [R16]
- Degradation tags can shorten enzyme persistence, but shared proteases can
  saturate and couple channels. **[D/T]** Clearance is a mitigation, not a
  logical guarantee. [R17, R18]

### Competing programmable systems

- Bridge-RNA/IS621 recombination directly demonstrated programmable insertion,
  excision, and inversion in vitro and in *E. coli*. **[D]** [R19]
- As of this review, no located paper establishes the prescribed six-transition
  exact product-to-substrate round trip, low-leak three-input control, and
  repeated-cycle fidelity for a bridge-RNA system. **[U/falsifying gap]**
- Orthogonal LoxPsym variants enable multiplexing in prokaryotic and eukaryotic
  hosts. **[D]** [R20] Cre-like inversions remain intrinsically bidirectional,
  so continued enzyme exposure can repeatedly flip the same segment. Locking
  designs based on excision or mutant sites usually sacrifice exact site
  restoration.
- Natural Hin/Gin/Fim-like switches prove that conservative reversible
  inversion is biologically real. **[D]** Their dependence on accessory
  factors, enhancer geometry, supercoiling, and physiological direction bias
  makes them weaker portable command channels. [R21]
- CRISPR double-strand-break/repair inversions can generate the desired
  orientation, but indels, deletions, and heterogeneous junctions conflict
  with exact reversible storage. **[D, falsifying]** [R22]

---

## 3. Architecture comparison

Scores are evidence-weighted judgments from 1 (poor) to 5 (strong). They are
not measured probabilities.

| Criterion | 3 orthogonal LSI/RDF channels | Bridge-RNA recombinase | 3 tyrosine recombinases / orthogonal lox | Natural invertases | CRISPR DSB/repair |
|---|---:|---:|---:|---:|---:|
| Ordered program | 5 | 4 | 4 | 2 | 4 |
| Exact molecular reversibility | 5 | 3 | 4 | 4 | 1 |
| Stable no-input/product state | 4 | 3 | 2 | 2 | 3 |
| Unique addressability | 4 | 5 | 3 | 2 | 5 |
| Low unintended compatible pairing | 3 | 3 | 2 | 3 | 3 |
| Reset direction control | 4 | 2 | 2 | 2 | 1 |
| Circular-DNA compatibility | 5 | 4 | 5 | 4 | 4 |
| Low inter-copy risk | 2 | 2 | 2 | 2 | 3 |
| Host portability | 5 | 3 | 5 | 2 | 3 |
| Construct burden | 3 | 4 | 3 | 3 | 2 |
| Published evidence | 5 | 3 | 5 | 4 | 5 |
| Deterministic validation | 5 | 3 | 4 | 3 | 1 |
| **Rank** | **1** | **2** | **3** | **4** | **5** |

### Why the LSI/RDF architecture wins

It is the only mature class combining all of the following:

- conservative, sequence-defined strand exchange;
- product sites chemically distinct from substrate sites;
- a characterized mechanism for explicitly reversing direction;
- strong operation in bacterial, cell-free, and eukaryotic contexts;
- multiple published orthogonal channels;
- a simple deterministic `BP↔LR` state model.

Its main weakness is not reaction precision but **system composition**:
leakage, noncognate RDF interactions, direct-repeat deletion topologies, and
multiple DNA copies. Those risks can be exposed by a finite experimental
matrix. Bridge recombination is more programmable but currently has a larger
evidence gap for exact repeated reversal. Tyrosine systems are more
intrinsically reversible but provide a poor terminal state because the product
remains a substrate for the same enzyme.

---

## 4. Selected physical and control architecture

### Host and format

**Final proof-of-concept host:** non-pathogenic *E. coli* K-12, with the
message register inserted once at a characterized neutral chromosomal locus.

**Development sequence:**

1. purified or cell-free, single-circular-DNA reaction panel;
2. each channel individually on a reporter plasmid;
3. complete single-copy chromosomal register;
4. only then, a combined autonomous controller.

Cell-free experiments are the fastest way to falsify site chemistry and
crosstalk, but they do not establish heritable cellular memory. Mammalian
culture adds chromatin, transfection-copy, and clearance variability without
improving the first proof.

### Why not a multicopy message plasmid

For `n` message copies, each LSI system has `n` cognate B-like sites and `n`
P-like sites. There are `n²` possible B/P pairings, only `n` of which are the
intended within-copy pairings. Under an intentionally conservative
equal-encounter abstraction, the possible intermolecular fraction is
`1 − 1/n`; real kinetics are topology-dependent, so this is a warning metric,
not a rate estimate. **[C/I]**

Multiple copies also make state gating unsafe: a switched copy can generate a
“next-state” signal while unswitched copies in the same cell still present
direct-repeat deletion substrates. A single-copy chromosome therefore
improves both molecular identity and controller logic.

### Message register

The seven logical boundaries become six active sites plus one inert spacer:

```text
ORI |
S1 = attB1→ | A |
S2 = attB2→ | B |
S3 = attB3→ | C |
S4 = inert  | D |
S5 = ←attP1 | E |
S6 = ←attP3 | F |
S7 = attP2→
```

The non-obvious orientation of Pair 2 is required by the nesting. Pair 2 starts
parallel, then Step 1 reverses S2 but not S7, making Pair 2 antiparallel for
Step 2. Pair 3 starts antiparallel; Step 1 reverses both members, preserving
their relative orientation, and Step 2 reverses S6 but not S3, making Pair 3
antiparallel for Step 3.

This directly falsifies the preliminary assumption that generic palindromic
`fwd/rvs` sites are sufficient. LSI `attB` and `attP` are asymmetric,
heterotypic sites. Their asymmetry and conversion to `attL/attR` supply
directionality. They should not be replaced by invented palindromes.

### Controller

Use a separate, single-copy controller locus or a low-copy, mobilization-
deficient development plasmid. The final design should move the controller to
the chromosome if expression remains adequate.

Symbolic logic:

```text
Forward mode:
  Drug A AND state-0  -> transient Int1
  Drug B AND state-1  -> transient Int2
  Drug C AND state-2  -> transient Int3

Reverse mode:
  Drug C AND state-3 AND DECRYPT -> transient Int3 + RDF3
  Drug B AND state-2 AND DECRYPT -> transient Int2 + RDF2
  Drug A AND state-1 AND DECRYPT -> transient Int1 + RDF1
```

State signals may be generated by orientation-dependent promoter/terminator
arrangements in a small control cassette coupled to the register. The exact
implementation is **[U]** and must be designed so that each of the seven
physical DNA states in the round trip has the intended transcriptional output.
Split-intein integrase logic is a plausible AND-gate implementation for φC31
**[T]**, but equivalent split points and leakage are not established for an
arbitrary three-LSI panel.

Use strong transcriptional repression as the primary OFF mechanism and short
protein half-lives as a cleanup layer. Do not depend on guide degradation,
perfect inducer washout, or proteolysis alone. Inducer withdrawal resets the
controller, not the DNA memory.

In the no-input state, all three channel outputs and DECRYPT are repressed, so
neither integrases nor RDFs should be produced above the empirically defined
long-storage threshold. After each pulse, remove the inducer by media exchange,
then wait for an experimentally measured, tagged-protein clearance criterion;
do not advance after a fixed assumed half-life. During development, confirm
the DNA state before the next pulse. State gating provides the second layer:
if the prior inversion is incomplete, the next integrase remains off rather
than acting on a direct-repeat deletion substrate. The three eventual sensor
chemistries should be chosen from a measured Marionette-compatible crosstalk
panel for the exact strain and media, rather than named a priori.

### Candidate channel panel

Start screening with Bxb1/gp47, φC31/gp3, φBT1 and/or TP901-1, SprA/SprB, plus
the best 2025 RDF-matched LSI candidates. Bxb1 is the preferred anchor channel.
φC31 is well characterized but its measured integrase-only excision makes it a
lower-stability candidate than a simplistic literature summary would imply.

Do **not** assign final A/B/C identities from sequence divergence. Select the
trio after measuring:

1. every integrase against every `attB/attP` pair;
2. every integrase against every `attL/attR` pair without RDF;
3. every RDF with every integrase on every product pair;
4. all three integrases and all three RDFs in mixed reactions;
5. site-dependent forward and reverse efficiencies in every intermediate
   topology.

---

## 5. Deterministic state and round-trip result

The accompanying simulator models ordered double-stranded elements,
orientation, LSI-specific site identity, `B/P/L/R` state, accessibility, and
the real substrate-to-product transition. Nucleotide strings are deterministic
synthetic fixtures, not biological parts.

### Starting state

```text
ORI+ | S1(B1,+) | A+ | S2(B2,+) | B+ | S3(B3,+) | C+ |
S4(inert,+) | D+ | S5(P1,-) | E+ | S6(P3,-) | F+ | S7(P2,+)
```

SHA-256:
`47ad4b15ab0971444b9d24f3c952976ae6e78b6e5450ee57bc8a33e6485173af`

### Input A, operation 1

Control state: `Drug A ∧ state-0 ∧ forward`; Int1 present, RDF1 absent.

Reaction: antiparallel `B1/P1 → L1/R1` inversion.

```text
ORI+ | S5(L1,+) | D- | S4(inert,-) | C- | S3(B3,-) | B- |
S2(B2,-) | A- | S1(R1,-) | E+ | S6(P3,-) | F+ | S7(P2,+)
```

Payload order: `D′ C′ B′ A′ E F`

SHA-256:
`8b17dd4fc8d781351cbfaa0c7d97b4b30857985a5f67739a5edd15dff304e8fe`

Next-site check: Pair 2 is now antiparallel and remains `B2/P2`.

### Input B, operation 2

Control state: `Drug B ∧ state-1 ∧ forward`; Int2 present, RDF2 absent.

Reaction: antiparallel `B2/P2 → L2/R2` inversion.

```text
ORI+ | S5(L1,+) | D- | S4(inert,-) | C- | S3(B3,-) | B- |
S7(L2,-) | F- | S6(P3,+) | E- | S1(R1,+) | A+ | S2(R2,+)
```

Payload order: `D′ C′ B′ F′ E′ A`

SHA-256:
`6c0b75e79d3ea29ee33472b6259a6634cf005bcf08f0d5f57c0d7f116f3d4301`

Next-site check: Pair 3 is now antiparallel and remains `B3/P3`.

### Input C, operation 3

Control state: `Drug C ∧ state-2 ∧ forward`; Int3 present, RDF3 absent.

Reaction: antiparallel `B3/P3 → L3/R3` inversion.

```text
ORI+ | S5(L1,+) | D- | S4(inert,-) | C- | S6(L3,-) | F+ |
S7(L2,+) | B+ | S3(R3,+) | E- | S1(R1,+) | A+ | S2(R2,+)
```

Payload order: `D′ C′ F B E′ A`

SHA-256:
`0984db90d882c71cb813f4799f3f8ab83b48af7475e504a7c506feaf16e69ab0`

### Complete inverse path

With DECRYPT enabled:

1. `Drug C ∧ state-3` supplies Int3+RDF3 and restores the Step-2 DNA string.
2. `Drug B ∧ state-2` supplies Int2+RDF2 and restores the Step-1 DNA string.
3. `Drug A ∧ state-1` supplies Int1+RDF1 and restores the starting DNA string.

Intermediate reverse hashes are therefore, in order:

```text
6c0b75e79d3ea29ee33472b6259a6634cf005bcf08f0d5f57c0d7f116f3d4301
8b17dd4fc8d781351cbfaa0c7d97b4b30857985a5f67739a5edd15dff304e8fe
47ad4b15ab0971444b9d24f3c952976ae6e78b6e5450ee57bc8a33e6485173af
```

The complete 766-bp fixture, including all payloads, active and inert sites,
and the defined linearization origin, compared byte-for-byte equal after the
round trip. Every `attL/attR` fixture returned to its exact original
`attB/attP` sequence. **[C]**

---

## 6. Unintended events and falsifying simulations

### Wrong order

All six input orders were enumerated with real topology classification:

| Forward order | Outcome |
|---|---|
| `ABC` | three intended inversions |
| `ACB` | A inversion, then C deletion |
| `BAC` | immediate B deletion |
| `BCA` | immediate B deletion |
| `CAB` | C inversion, then A deletion |
| `CBA` | C inversion, then B deletion |

For reverse chemistry from the final state, only `CBA` completes. Every other
order reaches a deletion topology. **[C]**

State gating is therefore a safety requirement, not an optional convenience.

### Incomplete reactions and overlapping windows

If Step 1 completes in fraction `pA` before active Int2 appears, the remaining
fraction `1−pA` still has parallel Pair-2 sites and is a deletion substrate.
A single-copy `Drug B AND state-1` gate converts this from deletion to
non-response in unswitched cells. The same logic applies between Steps 2 and 3.

If each operation independently completes with probability `p`, the ideal
fraction of one-copy registers completing the forward path is `p³`; the exact
six-operation round trip is `p⁶`. These are sensitivity calculations, not
biological rate estimates:

| Per-operation completion | Forward, one copy | Round trip, one copy | Round trip, five copies |
|---:|---:|---:|---:|
| 0.90 | 0.729 | 0.531 | 0.042 |
| 0.95 | 0.857 | 0.735 | 0.215 |
| 0.99 | 0.970 | 0.941 | 0.740 |
| 0.999 | 0.997 | 0.994 | 0.970 |

The multicopy column requires every copy to complete every transition and
still omits intermolecular recombination, so it is optimistic.

### Failure-mode register

| Failure | Consequence | Primary mitigation | Residual evidence status |
|---|---|---|---|
| Premature B or C | deletion/excision | state-dependent AND gates | topology proven **[C]**, gate implementation **[U]** |
| Residual earlier integrase | normally inactive product pair; finite basal reverse possible | degradation, dilution, elapsed-time criterion | φC31 counterexample **[D]** |
| RDF in forward mode | unwanted reversal or suppression of forward reaction | explicit direction gate; separate transcriptional repression | **[D/I]** |
| Wrong RDF–integrase pairing | noncognate reverse activity | full cross-matrix screen | observed class risk **[D]** |
| Multiple message copies | mixed registers, cointegrates, unsafe state signals | one-copy chromosome | topology **[I/C]** |
| Sister chromatids during replication | intermolecular rearrangement remains possible | slow-growth timing, short pulses, junction assays | **[I]** |
| Repeats/sites mutate | channel loss or altered specificity | sequence and long-read QC; minimize cycles | **[I]** |
| Regulatory parts invert | cryptic expression or loss of state gate | enumerate every intermediate; insulate parts | **[C/U]** |
| Protease saturation | long enzyme tails and channel coupling | orthogonal degradation tags; measure clearance | transferred **[T]** |
| Population selection | apparent enrichment of a subset | time-resolved single-cell and DNA-level assays | **[I]** |
| Host pseudo-sites | off-target integration/rearrangement | host-genome exact search and unbiased junction sequencing | system-dependent **[D/T]** |

---

## 7. Sequence and model analyses

### Sequence design status

No biological att sites, coding sequences, guide RNAs, primers, or payload
sequences are supplied. That is deliberate. Final sequence checks require the
exact host, insertion locus, vector/controller sequence, payloads, and selected
LSI/RDF trio.

The chosen architecture does not require CRISPR guides. Adding dCas9 masking
or recombinase recruitment would introduce a large, weakly evidenced control
layer and was rejected as the primary mechanism.

When sequences are available, the minimum analysis set is:

1. exact canonical att-site and central-dinucleotide validation;
2. all-by-all site compatibility enumeration in every state;
3. whole-host and controller-message searches for exact and near-match
   recognition sites;
4. circular repeat, low-complexity, and cloning-instability analysis;
5. promoter/terminator and ORF scans on both strands in all seven round-trip
   states;
6. RNA folding for each final transcript and split-intein junction;
7. protein expression and degradation measurements, not sequence prediction
   alone;
8. long-read sequencing plus unbiased junction capture after every transition.

### Proto and model use

| Tool/model | Use in this review | What it supports | What it cannot validate |
|---|---|---|---|
| Proto `ncbi-esearch` / `ncbi-esummary` | Run locally, CPU, seed 0, to resolve PubMed records, PMIDs, and DOIs | citation identity and provenance | mechanistic correctness or experimental quality |
| Deterministic Python topology model | Run, no randomness | exact order/orientation/site-state/string transitions and checksums | kinetics, expression, chromatin, or population behavior |
| Evo2 `evo2-score` | Considered; not run | could compare sequence-context likelihood after a real construct exists | recombination chemistry, specificity, or exact reversibility |
| AlphaGenome `all_folds` | Considered; not run | human/mouse regulatory-track predictions on supported 16 kb–1 Mb contexts | bacterial plasmid regulation or LSI chemistry |
| E. coli Promoter Calculator | Schema inspected; not run | sigma-70 promoter predictions on finalized bacterial sequences | leakage or state-machine correctness |
| ViennaRNA | Schema inspected; not run | MFE structures for finalized RNA controllers | in-cell recombination or expression sufficiency |

Evo2 scoring on the synthetic fixture would have produced a number with no
valid biological interpretation, so running the largest available checkpoint
would have reduced rather than improved scientific quality. AlphaGenome only
accepts human or mouse contexts in the available implementation and is
inappropriate for the recommended *E. coli* proof-of-concept.

The Proto workspace reported zero deployed apps. Citation tools ran in-process.
Initial exact-title `ncbi-esearch` queries returned no IDs; simpler searches and
direct `ncbi-esummary` calls succeeded. Tool semantic versions were not exposed
by the interface, so none are invented.

---

## 8. Confidence assessment

| Subsystem | Confidence | Basis |
|---|---|---|
| Symbolic topology and exact string round trip | **High** | deterministic exhaustive transition model **[C]** |
| One LSI/RDF reversible channel | **High** | direct biochemical and cellular evidence **[D]** |
| Three forward orthogonal LSI channels | **Medium-high** | multiplex integrase evidence, but exact trio pending **[D/U]** |
| Three mutually orthogonal RDF channels | **Medium-low** | variable noncognate interactions **[D/U]** |
| State-dependent suppression of wrong-order deletion | **Medium-low** | logic is necessary and implementable in principle, exact circuit unbuilt **[I/U]** |
| Three small-molecule sensors in *E. coli* | **High** | direct Marionette evidence **[D]** |
| Full in-cell six-operation exact round trip | **Low-medium** | no direct complete-system precedent |
| Multicopy message plasmid suitability | **Low** | topology and heterogeneity argue strongly against it |
| Bridge-RNA replacement | **Medium-low** | strong programmability, insufficient round-trip evidence |

---

## 9. Smallest discriminating proof-of-concept

Do not begin with six payload blocks and a fully autonomous controller.

### Phase 1: chemistry and orthogonality

Use one circular, single-copy-per-reaction DNA substrate with three nested
candidate site pairs and short neutral barcodes. Apply purified or cell-free
enzymes sequentially:

```text
Int1 → Int2 → Int3 → Int3+RDF3 → Int2+RDF2 → Int1+RDF1
```

At each state, use complete-plasmid long-read sequencing or full-length
amplicon sequencing, junction-specific digital PCR, and topology-sensitive
gel/restriction analysis. Include:

- no-enzyme controls;
- each integrase alone in every state;
- every wrong input order;
- each RDF with every noncognate integrase;
- all components mixed at worst-case residual concentrations;
- a second DNA-copy challenge to expose cointegrates.

This experiment distinguishes exact inversion from deletion, incomplete
switching, hidden site crosstalk, spontaneous reverse chemistry, and
intermolecular products.

### Phase 2: one-copy cellular register

Move only a passing register into one *E. coli* K-12 chromosomal locus. Supply
one channel at a time from transient controller plasmids or tightly regulated
expression cassettes. Establish long no-input stability and repeated exact
forward/reverse cycles before combining input sensors.

### Phase 3: ordered control

Add three chemical sensors, then the forward state gates, then the DECRYPT
mode and reverse gates. A pass requires DNA-level state purity, not reporter
color alone.

---

## 10. Remaining questions before construction

1. Is a fourth direction/mode input acceptable, or must decryption occur ex
   vivo with inverse enzyme/RDF reagents?
2. What exact *E. coli* K-12 strain and chromosomal landing locus will be used?
3. What are the complete A–F sequences, and are reverse-complemented payloads
   semantically acceptable?
4. What switching purity, off-state duration, and cycle count are required?
5. Is lineage-level recovery sufficient, or must every DNA molecule in every
   cell be restored?
6. Which candidate LSI/RDF panel is available experimentally?
7. Can full-length long-read sequencing and unbiased junction assays be used?
8. Are all three drugs required to be removable, or can cells be transferred
   between media?
9. Can the message be chromosomal, or is an episome mandatory?
10. What regulatory/selection sequences may be present inside inverted
    intervals?

If the fourth direction signal is forbidden and the same three drug pulses
must deterministically perform both forward and reverse transitions, the
answer becomes negative for the quality threshold in this brief. The smallest
change is to permit one global DECRYPT mode or ex-vivo RDF delivery.

---

## 11. Reproducibility artifacts

- `simulate.py`: deterministic topology, site-state, wrong-order, and
  sensitivity model.
- `simulation_results.json`: full state records, both-strand recognition
  signature counts, event classifications, hashes, all order permutations,
  and non-ideal parameter sweeps.

Run:

```bash
python3 research/sequential_rearrangement/simulate.py
```

The script uses no random number generator. All fixture DNA is derived
deterministically from SHA-256 labels. The JSON records its script hash.

---

## References

1. **[R1]** Ghosh P, Kim AI, Hatfull GF. The orientation of
   mycobacteriophage Bxb1 integration is solely dependent on the central
   dinucleotide of attP and attB. *Molecular Cell* (2003).
   [doi:10.1016/S1097-2765(03)00444-1](https://doi.org/10.1016/S1097-2765(03)00444-1);
   [PMID 14636570](https://pubmed.ncbi.nlm.nih.gov/14636570/).
2. **[R2]** Singh S, Ghosh P, Hatfull GF. Attachment site selection and
   identity in Bxb1 serine integrase-mediated site-specific recombination.
   *PLoS Genetics* (2013).
   [doi:10.1371/journal.pgen.1003490](https://doi.org/10.1371/journal.pgen.1003490);
   [PMID 23658531](https://pubmed.ncbi.nlm.nih.gov/23658531/).
3. **[R3]** Ghosh P, Wasil LR, Hatfull GF. Control of phage Bxb1 excision by a
   novel recombination directionality factor. *PLoS Biology* (2006).
   [doi:10.1371/journal.pbio.0040186](https://doi.org/10.1371/journal.pbio.0040186);
   [PMID 16719562](https://pubmed.ncbi.nlm.nih.gov/16719562/).
4. **[R4]** Bonnet J, Subsoontorn P, Endy D. Rewritable digital data storage in
   live cells via engineered control of recombination directionality. *PNAS*
   (2012).
   [doi:10.1073/pnas.1202344109](https://doi.org/10.1073/pnas.1202344109);
   [PMID 22615351](https://pubmed.ncbi.nlm.nih.gov/22615351/).
5. **[R5]** Khaleel T et al. A phage protein that binds φC31 integrase to switch
   its directionality. *Molecular Microbiology* (2011).
   [doi:10.1111/j.1365-2958.2011.07696.x](https://doi.org/10.1111/j.1365-2958.2011.07696.x);
   [PMID 21564337](https://pubmed.ncbi.nlm.nih.gov/21564337/).
6. **[R6]** Farruggio AP et al. Efficient reversal of phiC31 integrase
   recombination in mammalian cells. *Biotechnology Journal* (2012).
   [doi:10.1002/biot.201200283](https://doi.org/10.1002/biot.201200283);
   [PMID 22933343](https://pubmed.ncbi.nlm.nih.gov/22933343/).
7. **[R7]** Olorunniji FJ et al. Control of serine integrase recombination
   directionality by fusion with the directionality factor. *Nucleic Acids
   Research* (2017).
   [doi:10.1093/nar/gkx567](https://doi.org/10.1093/nar/gkx567);
   [PMID 28666339](https://pubmed.ncbi.nlm.nih.gov/28666339/).
8. **[R8]** Olorunniji FJ et al. Control of φC31 integrase-mediated
   site-specific recombination by protein trans-splicing. *Nucleic Acids
   Research* (2019).
   [doi:10.1093/nar/gkz936](https://doi.org/10.1093/nar/gkz936);
   [PMID 31667500](https://pubmed.ncbi.nlm.nih.gov/31667500/).
9. **[R9]** Duan Y et al. Mitigating genetic instability caused by the
   excision activity of the phiC31 integrase in *Streptomyces*. *Applied and
   Environmental Microbiology* (2025).
   [doi:10.1128/aem.01812-24](https://doi.org/10.1128/aem.01812-24);
   [PMID 39704534](https://pubmed.ncbi.nlm.nih.gov/39704534/);
   [PMC11784100](https://pmc.ncbi.nlm.nih.gov/articles/PMC11784100/).
10. **[R10]** MacDonald AI et al. Variable orthogonality of serine integrase
    interactions within the φC31 family. *Scientific Reports* (2024).
    [doi:10.1038/s41598-024-77570-9](https://doi.org/10.1038/s41598-024-77570-9);
    [PMID 39487291](https://pubmed.ncbi.nlm.nih.gov/39487291/).
11. **[R11]** Alsaleh A et al. Large serine integrases utilise scavenged phage
    proteins as directionality cofactors. *Nucleic Acids Research* (2025).
    [doi:10.1093/nar/gkaf050](https://doi.org/10.1093/nar/gkaf050);
    [PMID 39907112](https://pubmed.ncbi.nlm.nih.gov/39907112/).
12. **[R12]** Shin H et al. Identification of cognate recombination
    directionality factors for large serine recombinases by virtual pulldown.
    *Nucleic Acids Research* (2025).
    [doi:10.1093/nar/gkaf691](https://doi.org/10.1093/nar/gkaf691);
    [PMID 40701553](https://pubmed.ncbi.nlm.nih.gov/40701553/).
13. **[R13]** Yang L et al. Permanent genetic memory with >1-byte capacity.
    *Nature Methods* (2014).
    [doi:10.1038/nmeth.3147](https://doi.org/10.1038/nmeth.3147);
    [PMID 25344638](https://pubmed.ncbi.nlm.nih.gov/25344638/).
14. **[R14]** Roquet N et al. Synthetic recombinase-based state machines in
    living cells. *Science* (2016).
    [doi:10.1126/science.aad8559](https://doi.org/10.1126/science.aad8559);
    [PMID 27463678](https://pubmed.ncbi.nlm.nih.gov/27463678/).
15. **[R15]** Meyer AJ et al. *Escherichia coli* “Marionette” strains with 12
    highly optimized small-molecule sensors. *Nature Chemical Biology* (2019).
    [doi:10.1038/s41589-018-0168-3](https://doi.org/10.1038/s41589-018-0168-3);
    [PMID 30478458](https://pubmed.ncbi.nlm.nih.gov/30478458/).
16. **[R16]** Weinberg BH et al. High-performance chemical- and light-inducible
    recombinases in mammalian cells and mice. *Nature Communications* (2019).
    [doi:10.1038/s41467-019-12800-7](https://doi.org/10.1038/s41467-019-12800-7);
    [PMID 31649244](https://pubmed.ncbi.nlm.nih.gov/31649244/).
17. **[R17]** Cameron DE, Collins JJ. Tunable protein degradation in bacteria.
    *Nature Biotechnology* (2014).
    [doi:10.1038/nbt.3053](https://doi.org/10.1038/nbt.3053);
    [PMID 25402616](https://pubmed.ncbi.nlm.nih.gov/25402616/).
18. **[R18]** Cookson NA et al. Queueing up for enzymatic processing:
    correlated signaling through coupled degradation. *Molecular Systems
    Biology* (2011).
    [doi:10.1038/msb.2011.94](https://doi.org/10.1038/msb.2011.94);
    [PMID 22186735](https://pubmed.ncbi.nlm.nih.gov/22186735/).
19. **[R19]** Durrant MG et al. Bridge RNAs direct programmable recombination
    of target and donor DNA. *Nature* (2024).
    [doi:10.1038/s41586-024-07552-4](https://doi.org/10.1038/s41586-024-07552-4);
    [PMID 38926615](https://pubmed.ncbi.nlm.nih.gov/38926615/).
20. **[R20]** Cautereels C et al. Orthogonal LoxPsym sites allow multiplexed
    site-specific recombination in prokaryotic and eukaryotic hosts. *Nature
    Communications* (2024).
    [doi:10.1038/s41467-024-44996-8](https://doi.org/10.1038/s41467-024-44996-8);
    [PMID 38326330](https://pubmed.ncbi.nlm.nih.gov/38326330/).
21. **[R21]** McLean MM et al. Multiple interfaces between a serine recombinase
    and an enhancer control site-specific DNA inversion. *eLife* (2013).
    [doi:10.7554/eLife.01211](https://doi.org/10.7554/eLife.01211);
    [PMID 24151546](https://pubmed.ncbi.nlm.nih.gov/24151546/).
22. **[R22]** Park SH et al. Comprehensive analysis and accurate
    quantification of unintended large gene modifications induced by
    CRISPR-Cas9 gene editing. *Science Advances* (2022).
    [doi:10.1126/sciadv.abo7676](https://doi.org/10.1126/sciadv.abo7676);
    [PMID 36269834](https://pubmed.ncbi.nlm.nih.gov/36269834/).
23. **[R23]** Xu Z et al. Accuracy and efficiency define Bxb1 integrase as the
    best of fifteen candidate serine recombinases for integration into the
    human genome. *BMC Biotechnology* (2013).
    [doi:10.1186/1472-6750-13-87](https://doi.org/10.1186/1472-6750-13-87);
    [PMID 24139482](https://pubmed.ncbi.nlm.nih.gov/24139482/).
24. **[R24]** Thorpe HM, Smith MCM. In vitro site-specific integration of
    bacteriophage DNA catalyzed by a recombinase of the resolvase/invertase
    family. *PNAS* (1998).
    [doi:10.1073/pnas.95.10.5505](https://doi.org/10.1073/pnas.95.10.5505);
    [PMID 9576912](https://pubmed.ncbi.nlm.nih.gov/9576912/).
