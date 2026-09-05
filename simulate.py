#!/usr/bin/env python3
"""Deterministic topology model for a three-step reversible DNA program.

The nucleotide sequences in this file are synthetic fixtures, not biological
recognition sites or synthesis-ready constructs. The model treats each active
site as two recombinase-specific half-sites and applies the substrate/product
state change BP <-> LR expected for a large serine integrase (LSI). It models
the topological consequence of recombination on one circular DNA molecule.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

BASES = "ACGT"
FORWARD_PROGRAM = ("A", "B", "C")
REVERSE_PROGRAM = ("C", "B", "A")
SYSTEM_FOR_INPUT = {"A": "LSI-1", "B": "LSI-2", "C": "LSI-3"}


def reverse_complement(sequence: str) -> str:
    """Return the reverse complement of a DNA sequence."""
    return sequence.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def fixture_dna(label: str, length: int) -> str:
    """Generate deterministic DNA for symbolic simulation fixtures."""
    output = []
    counter = 0
    while len(output) < length:
        digest = hashlib.sha256(f"{label}:{counter}".encode()).digest()
        output.extend(BASES[byte & 0b11] for byte in digest)
        counter += 1
    return "".join(output[:length])


@dataclass(frozen=True)
class PairDefinition:
    """Synthetic half-sites used to model LSI substrate/product chemistry."""

    system: str
    b_site_id: str
    p_site_id: str
    b_left: str
    b_right: str
    p_left: str
    p_right: str
    crossover: str = "GC"

    def sequence_for(self, state: str) -> str:
        """Return a symbolic site sequence for B, P, L, or R."""
        combinations = {
            "B": (self.b_left, self.b_right),
            "P": (self.p_left, self.p_right),
            # For the canonical forward orientation, L joins the B left
            # half-site to the P right half-site; R is the reciprocal hybrid.
            "L": (self.b_left, self.p_right),
            "R": (self.p_left, self.b_right),
        }
        left, right = combinations[state]
        return left + self.crossover + right


@dataclass
class Element:
    """A physically ordered DNA element."""

    identity: str
    kind: Literal["origin", "payload", "site"]
    canonical_sequence: str
    orientation: int = 1
    system: str | None = None
    site_state: str | None = None
    accessible: bool = True

    @property
    def sequence(self) -> str:
        """Return the sequence in its current physical orientation."""
        if self.orientation == 1:
            return self.canonical_sequence
        return reverse_complement(self.canonical_sequence)

    def label(self) -> str:
        """Return a compact physical-state label."""
        sign = "+" if self.orientation == 1 else "-"
        if self.kind == "site":
            return f"{self.identity}({self.site_state},{sign})"
        return f"{self.identity}{sign}"


@dataclass
class Event:
    """A classified recombination event."""

    input_name: str
    system: str
    chemistry: Literal["Int", "Int+RDF"]
    pair_state: str
    relative_orientation: Literal["opposite", "parallel"]
    outcome: str
    intended: bool
    note: str


def pair_definitions() -> dict[str, PairDefinition]:
    """Build three mutually distinct symbolic LSI site pairs."""
    site_ids = {
        "LSI-1": ("S1", "S5"),
        "LSI-2": ("S2", "S7"),
        "LSI-3": ("S3", "S6"),
    }
    definitions = {}
    for system, (b_site_id, p_site_id) in site_ids.items():
        definitions[system] = PairDefinition(
            system=system,
            b_site_id=b_site_id,
            p_site_id=p_site_id,
            b_left=fixture_dna(f"{system}:B:left", 16),
            b_right=fixture_dna(f"{system}:B:right", 16),
            p_left=fixture_dna(f"{system}:P:left", 16),
            p_right=fixture_dna(f"{system}:P:right", 16),
        )
    return definitions


def initial_construct(
    definitions: dict[str, PairDefinition],
) -> list[Element]:
    """Create the starting circular construct, linearized at a fixed origin."""
    site_specs = {
        # Pair 1 is antiparallel at Step 1.
        "S1": ("LSI-1", "B", 1),
        "S5": ("LSI-1", "P", -1),
        # Pair 2 starts parallel; Step 1 flips S2 but not S7.
        "S2": ("LSI-2", "B", 1),
        "S7": ("LSI-2", "P", 1),
        # Pair 3 is antiparallel and both members undergo one prior inversion.
        "S3": ("LSI-3", "B", 1),
        "S6": ("LSI-3", "P", -1),
    }

    elements = [
        Element("ORI", "origin", fixture_dna("defined-linearization-origin", 96)),
    ]
    for index, payload in enumerate("ABCDEF", start=1):
        site_id = f"S{index}"
        if site_id == "S4":
            elements.append(
                Element(
                    site_id,
                    "site",
                    fixture_dna("S4:inert-boundary", 34),
                    orientation=1,
                    system=None,
                    site_state="inert",
                    accessible=False,
                )
            )
        else:
            system, state, orientation = site_specs[site_id]
            elements.append(
                Element(
                    site_id,
                    "site",
                    definitions[system].sequence_for(state),
                    orientation=orientation,
                    system=system,
                    site_state=state,
                )
            )
        elements.append(
            Element(payload, "payload", fixture_dna(f"payload:{payload}", 72))
        )

    system, state, orientation = site_specs["S7"]
    elements.append(
        Element(
            "S7",
            "site",
            definitions[system].sequence_for(state),
            orientation=orientation,
            system=system,
            site_state=state,
        )
    )
    return elements


def construct_sequence(elements: list[Element]) -> str:
    """Linearize one circular construct relative to ORI."""
    assert elements[0].identity == "ORI"
    return "".join(element.sequence for element in elements)


def sequence_hash(elements: list[Element]) -> str:
    """Return the SHA-256 hash of the full linearized construct."""
    return hashlib.sha256(construct_sequence(elements).encode()).hexdigest()


def circular_count(sequence: str, query: str) -> int:
    """Count exact query starts on a circular forward-strand representation."""
    extended = sequence + sequence[: len(query) - 1]
    return sum(
        extended.startswith(query, index) for index in range(len(sequence))
    )


def recognition_signature_counts(
    elements: list[Element], definitions: dict[str, PairDefinition]
) -> dict[str, int]:
    """Count every synthetic B/P/L/R signature on either strand."""
    sequence = construct_sequence(elements)
    counts = {}
    for system, definition in definitions.items():
        for state in ("B", "P", "L", "R"):
            signature = definition.sequence_for(state)
            counts[f"{system}:{state}"] = circular_count(
                sequence, signature
            ) + circular_count(sequence, reverse_complement(signature))
    return counts


def payload_order(elements: list[Element]) -> list[str]:
    """Return physical payload order and orientation."""
    return [
        ("+" if element.orientation == 1 else "-") + element.identity
        for element in elements
        if element.kind == "payload"
    ]


def pair_elements(elements: list[Element], system: str) -> tuple[Element, Element]:
    """Return the two sites belonging to one recombinase system."""
    sites = [element for element in elements if element.system == system]
    assert len(sites) == 2
    return sites[0], sites[1]


def pair_state(elements: list[Element], system: str) -> str:
    """Return BP or LR for one cognate pair."""
    states = {element.site_state for element in pair_elements(elements, system)}
    if states == {"B", "P"}:
        return "BP"
    if states == {"L", "R"}:
        return "LR"
    raise AssertionError(f"Invalid site-state combination for {system}: {states}")


def relative_orientation(
    elements: list[Element], system: str
) -> Literal["opposite", "parallel"]:
    """Return the relative physical orientation of a cognate pair."""
    first, second = pair_elements(elements, system)
    if first.orientation != second.orientation:
        return "opposite"
    return "parallel"


def classify_event(
    elements: list[Element],
    input_name: str,
    chemistry: Literal["Int", "Int+RDF"],
) -> Event:
    """Classify the topological outcome without mutating DNA."""
    system = SYSTEM_FOR_INPUT[input_name]
    state = pair_state(elements, system)
    orientation = relative_orientation(elements, system)

    if chemistry == "Int":
        if state == "LR":
            outcome = "inactive_pairing"
            note = (
                "LSI product sites are nominally inactive without cognate RDF; "
                "basal reverse activity must still be measured."
            )
        elif orientation == "opposite":
            outcome = "inversion"
            note = "attB x attP intramolecular inversion."
        else:
            outcome = "deletion"
            note = "attB x attP direct-repeat recombination excises the interval."
    else:
        if state == "BP":
            outcome = "inactive_pairing"
            note = "Cognate RDF suppresses integration chemistry in the ideal model."
        elif orientation == "opposite":
            outcome = "inversion"
            note = "attL x attR intramolecular inverse inversion."
        else:
            outcome = "deletion"
            note = "attL x attR direct-repeat recombination excises the interval."

    intended = (
        outcome == "inversion"
        and ((chemistry == "Int" and state == "BP") or (chemistry == "Int+RDF" and state == "LR"))
    )
    return Event(
        input_name=input_name,
        system=system,
        chemistry=chemistry,
        pair_state=state,
        relative_orientation=orientation,
        outcome=outcome,
        intended=intended,
        note=note,
    )


def update_site_products(
    elements: list[Element],
    definition: PairDefinition,
    chemistry: Literal["Int", "Int+RDF"],
) -> None:
    """Apply the LSI half-site substrate/product conversion."""
    for element in elements:
        if element.identity == definition.b_site_id:
            next_state = "R" if chemistry == "Int" else "B"
            element.site_state = next_state
            element.canonical_sequence = definition.sequence_for(next_state)
        elif element.identity == definition.p_site_id:
            next_state = "L" if chemistry == "Int" else "P"
            element.site_state = next_state
            element.canonical_sequence = definition.sequence_for(next_state)


def apply_inversion(
    elements: list[Element],
    definitions: dict[str, PairDefinition],
    input_name: str,
    chemistry: Literal["Int", "Int+RDF"],
) -> Event:
    """Apply one intended inversion and the real BP/LR site-state conversion."""
    event = classify_event(elements, input_name, chemistry)
    if event.outcome != "inversion":
        return event

    indices = [
        index
        for index, element in enumerate(elements)
        if element.system == event.system
    ]
    left, right = min(indices), max(indices)
    segment = deepcopy(elements[left : right + 1])
    segment.reverse()
    for element in segment:
        element.orientation *= -1
    elements[left : right + 1] = segment
    update_site_products(elements, definitions[event.system], chemistry)
    return event


def state_record(
    name: str,
    elements: list[Element],
    definitions: dict[str, PairDefinition],
    active_input: str | None,
    chemistry: str | None,
) -> dict[str, object]:
    """Serialize a complete ideal-state snapshot."""
    possible = []
    for input_name in FORWARD_PROGRAM:
        for possible_chemistry in ("Int", "Int+RDF"):
            possible.append(
                asdict(
                    classify_event(
                        elements,
                        input_name,
                        possible_chemistry,
                    )
                )
            )
    signature_counts = recognition_signature_counts(elements, definitions)
    for system in SYSTEM_FOR_INPUT.values():
        state = pair_state(elements, system)
        assert signature_counts[f"{system}:{state[0]}"] == 1
        assert signature_counts[f"{system}:{state[1]}"] == 1
        for inactive_state in {"B", "P", "L", "R"} - set(state):
            assert signature_counts[f"{system}:{inactive_state}"] == 0

    return {
        "name": name,
        "active_input": active_input,
        "chemistry": chemistry,
        "sha256": sequence_hash(elements),
        "length_bp": len(construct_sequence(elements)),
        "physical_elements": [element.label() for element in elements],
        "payload_order": payload_order(elements),
        "site_accessibility": {
            element.identity: {
                "system": element.system,
                "state": element.site_state,
                "orientation": element.orientation,
                "accessible": element.accessible,
            }
            for element in elements
            if element.kind == "site"
        },
        "exact_recognition_signature_counts_both_strands": signature_counts,
        "possible_cognate_events": possible,
        "cross_system_events": (
            "inactive in the ideal orthogonality model; pairwise enzyme-site and "
            "integrase-RDF crosstalk require empirical measurement"
        ),
        "intermolecular_events": (
            "not represented in the single-molecule state; any second construct "
            "copy creates possible cognate integration/cointegrate substrates"
        ),
    }


def run_round_trip(
    definitions: dict[str, PairDefinition],
) -> tuple[list[dict[str, object]], bool]:
    """Run the prescribed forward and reverse paths."""
    elements = initial_construct(definitions)
    start_sequence = construct_sequence(elements)
    states = [state_record("start", elements, definitions, None, None)]

    for step, input_name in enumerate(FORWARD_PROGRAM, start=1):
        event = apply_inversion(elements, definitions, input_name, "Int")
        assert event.intended
        states.append(
            state_record(
                f"forward_{step}",
                elements,
                definitions,
                input_name,
                "Int",
            )
        )

    for step, input_name in enumerate(REVERSE_PROGRAM, start=1):
        event = apply_inversion(elements, definitions, input_name, "Int+RDF")
        assert event.intended
        states.append(
            state_record(
                f"reverse_{step}",
                elements,
                definitions,
                input_name,
                "Int+RDF",
            )
        )

    restored = construct_sequence(elements) == start_sequence
    assert restored
    assert states[0]["sha256"] == states[-1]["sha256"]
    return states, restored


def run_order_permutations(
    definitions: dict[str, PairDefinition],
    starting_elements: list[Element],
    chemistry: Literal["Int", "Int+RDF"],
) -> list[dict[str, object]]:
    """Enumerate all input orders until inversion or deletion outcomes resolve."""
    outputs = []
    for order in itertools.permutations(FORWARD_PROGRAM):
        elements = deepcopy(starting_elements)
        events = []
        terminated = False
        for input_name in order:
            event = apply_inversion(elements, definitions, input_name, chemistry)
            events.append(asdict(event))
            if event.outcome == "deletion":
                terminated = True
                break
        outputs.append(
            {
                "order": "".join(order),
                "events": events,
                "terminated_on_deletion": terminated,
                "final_sha256_if_single_circle": (
                    None if terminated else sequence_hash(elements)
                ),
                "payload_order_if_single_circle": (
                    None if terminated else payload_order(elements)
                ),
            }
        )
    return outputs


def deterministic_stress_table() -> list[dict[str, object]]:
    """Calculate illustrative completeness values without fitting biological rates."""
    rows = []
    for per_step in (0.90, 0.95, 0.99, 0.999):
        for copies in (1, 2, 5, 20):
            rows.append(
                {
                    "per_operation_completion": per_step,
                    "message_copies": copies,
                    "possible_cognate_pairings_per_system": copies**2,
                    "intramolecular_pairings_per_system": copies,
                    "intermolecular_pairings_per_system": copies * (copies - 1),
                    "intermolecular_fraction_if_all_pairings_equiprobable": (
                        1 - 1 / copies
                    ),
                    "all_copies_correct_after_forward": per_step ** (3 * copies),
                    "all_copies_exact_after_round_trip": per_step ** (6 * copies),
                }
            )
    return rows


def architecture_models() -> dict[str, object]:
    """State what can and cannot be deterministically validated for alternatives."""
    return {
        "large_serine_integrases": {
            "deterministic_rule": "BP --Int--> LR; LR --Int+RDF--> BP",
            "topology": {
                "opposite_orientation": "inversion",
                "parallel_orientation": "deletion/excision",
                "different_molecules": "integration/cointegrate",
            },
            "exact_round_trip_modeled": True,
        },
        "tyrosine_recombinases": {
            "deterministic_rule": (
                "homotypic sites remain substrates after inversion; continued "
                "enzyme exposure makes forward and reverse inversions reachable"
            ),
            "topology": {
                "opposite_orientation": "reversible inversion/oscillation",
                "parallel_orientation": "deletion; reintegration is disfavored",
                "different_molecules": "integration/translocation",
            },
            "exact_round_trip_modeled": (
                "string-level inversion is exact, but a homogeneous endpoint is "
                "not deterministic without an additional locking mechanism"
            ),
        },
        "bridge_rna_recombinase": {
            "deterministic_rule": (
                "ideal targeted inversion can be represented as an exact string "
                "operation, but a validated product-to-substrate inverse program "
                "for this six-transition cycle was not established here"
            ),
            "exact_round_trip_modeled": False,
            "reason": "mechanistic and experimental evidence is not yet sufficient",
        },
        "crispr_dsb_repair": {
            "deterministic_rule": (
                "two cuts plus repair can yield inversion, deletion, indels, or "
                "other junctions; exact repair is not guaranteed"
            ),
            "exact_round_trip_modeled": False,
            "reason": "repair outcomes are intrinsically non-deterministic",
        },
    }


def main() -> None:
    """Run all analyses and write one reproducibility artifact."""
    definitions = pair_definitions()
    states, restored = run_round_trip(definitions)

    start = initial_construct(definitions)
    final_elements = initial_construct(definitions)
    for input_name in FORWARD_PROGRAM:
        event = apply_inversion(final_elements, definitions, input_name, "Int")
        assert event.intended

    results = {
        "artifact": {
            "model": "symbolic-LSI-topology-v1",
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "random_seed": None,
            "randomness_used": False,
            "sequence_fixture_warning": (
                "All nucleotide strings are deterministic synthetic fixtures and "
                "are not characterized recombination sites or construct designs."
            ),
        },
        "round_trip": {
            "restored_exactly": restored,
            "states": states,
        },
        "forward_order_permutations": run_order_permutations(
            definitions, start, "Int"
        ),
        "reverse_order_permutations": run_order_permutations(
            definitions, final_elements, "Int+RDF"
        ),
        "nonideal_parameter_sweep": {
            "warning": (
                "These are deterministic sensitivity calculations, not empirical "
                "rate estimates; they exclude intermolecular recombination."
            ),
            "rows": deterministic_stress_table(),
            "overlap_without_state_gate": (
                "If Step 1 completes with fraction p_A before active Step 2, the "
                "unswitched fraction (1-p_A) presents parallel Step-2 sites and is "
                "a deletion substrate."
            ),
            "overlap_with_single_copy_state_gate": (
                "Drug B AND state-1 gating keeps Int-2 absent in unswitched cells; "
                "this logic fails on multicopy message DNA if one switched copy "
                "activates Int-2 while other copies remain unswitched."
            ),
        },
        "alternative_architecture_models": architecture_models(),
    }

    output_path = Path(__file__).with_name("simulation_results.json")
    output_path.write_text(json.dumps(results, indent=2) + "\n")
    print(output_path)
    print(
        json.dumps(
            {
                "restored_exactly": restored,
                "start_sha256": states[0]["sha256"],
                "final_sha256": states[3]["sha256"],
                "restored_sha256": states[-1]["sha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
