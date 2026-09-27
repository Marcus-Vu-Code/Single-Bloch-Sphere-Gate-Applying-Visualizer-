"""Project 1b: single-qubit gates and their Bloch-sphere action.

The program intentionally computes Bloch coordinates from expectation values
instead of calling a quantum-computing visualization package.  That keeps the
linear-algebra steps visible and makes the script easy to execute in a normal
Python environment.
"""

from __future__ import annotations

import argparse
import cmath
import math
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, cmath.exp(1j * math.pi / 4)]], dtype=complex)

GATES: dict[str, np.ndarray] = {"X": X, "Y": Y, "Z": Z, "H": H, "S": S, "T": T}
PAULI: dict[str, np.ndarray] = {"x": X, "y": Y, "z": Z}


def state_from_angles(theta: float, phi: float) -> np.ndarray:
    """Return |psi> = cos(theta/2)|0> + exp(i phi)sin(theta/2)|1>."""

    state = np.array(
        [math.cos(theta / 2), cmath.exp(1j * phi) * math.sin(theta / 2)],
        dtype=complex,
    )
    return normalize(state)


def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if np.isclose(norm, 0.0):
        raise ValueError("A quantum state cannot have zero norm.")
    return state / norm


def apply_gate(gate: np.ndarray, state: np.ndarray) -> np.ndarray:
    """Apply a 2x2 unitary and normalize away floating-point drift."""

    return normalize(gate @ state)


def bloch_vector(state: np.ndarray) -> np.ndarray:
    """Compute ( <X>, <Y>, <Z> ) for a normalized state."""

    state = normalize(state)
    values = [np.vdot(state, operator @ state) for operator in (X, Y, Z)]
    return np.real_if_close(values).astype(float)


def rotation_closed_form(axis: str, angle: float) -> np.ndarray:
    """Return R_k(angle) = cos(angle/2)I - i sin(angle/2)sigma_k."""

    try:
        pauli = PAULI[axis.lower()]
    except KeyError as error:
        raise ValueError("axis must be x, y, or z") from error
    return math.cos(angle / 2) * I2 - 1j * math.sin(angle / 2) * pauli


def rotation_matrix_exponential(axis: str, angle: float) -> np.ndarray:
    """Compute exp(-i angle sigma_k / 2) using eigendecomposition.

    This is deliberately independent of ``rotation_closed_form``.  Since a
    Pauli matrix is diagonalizable, exp(V D V^-1) = V exp(D) V^-1.
    """

    try:
        pauli = PAULI[axis.lower()]
    except KeyError as error:
        raise ValueError("axis must be x, y, or z") from error
    eigenvalues, eigenvectors = np.linalg.eig(-1j * angle * pauli / 2)
    diagonal_exponential = np.diag(np.exp(eigenvalues))
    return eigenvectors @ diagonal_exponential @ np.linalg.inv(eigenvectors)


def parse_sequence(sequence: str | Iterable[str]) -> list[str]:
    if isinstance(sequence, str):
        tokens = sequence.replace(",", " ").split()
    else:
        tokens = list(sequence)
    normalized = [token.upper() for token in tokens]
    invalid = sorted(set(normalized) - set(GATES))
    if invalid:
        raise ValueError(f"Unknown gate(s): {', '.join(invalid)}")
    if not normalized:
        raise ValueError("The custom sequence must contain at least one gate.")
    return normalized


def apply_sequence(state: np.ndarray, sequence: Sequence[str]) -> np.ndarray:
    for name in sequence:
        state = apply_gate(GATES[name], state)
    return state


def relative_phase(reference: np.ndarray, candidate: np.ndarray) -> complex:
    """Return the phase relating two equal physical statevectors."""

    reference = normalize(reference)
    candidate = normalize(candidate)
    overlap = np.vdot(reference, candidate)
    if np.isclose(abs(overlap), 0.0):
        raise ValueError("States are orthogonal and have no single relative phase.")
    return overlap / abs(overlap)


def format_complex_vector(vector: np.ndarray) -> str:
    return "[" + ", ".join(f"{value.real:+.6f}{value.imag:+.6f}j" for value in vector) + "]"


def print_gate_table(state: np.ndarray) -> None:
    initial = bloch_vector(state)
    print("Single-qubit gate changes")
    print(f"  initial Bloch vector: {initial}")
    for name, gate in GATES.items():
        transformed = apply_gate(gate, state)
        print(f"  {name}: {bloch_vector(transformed)}")


def repeated_z_rotation(initial: np.ndarray, steps: int = 8) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """Return statevectors and Bloch vectors after each repeated Rz(pi/4)."""

    gate = rotation_closed_form("z", math.pi / 4)
    states = [normalize(initial)]
    vectors = [bloch_vector(initial)]
    state = normalize(initial)
    for _ in range(steps):
        state = apply_gate(gate, state)
        states.append(state)
        vectors.append(bloch_vector(state))
    return states, vectors


def plot_bloch_sphere(
    vectors: Sequence[np.ndarray],
    title: str,
    output_path: Path | None = None,
    *,
    show: bool = False,
) -> None:
    """Plot a unit sphere and a sequence of Bloch vectors."""

    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise RuntimeError(
            "Plotting requires matplotlib. Install dependencies with "
            "python -m pip install -r requirements.txt."
        ) from error

    figure = plt.figure(figsize=(7, 7))
    axis = figure.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, 80)
    v = np.linspace(0, np.pi, 40)
    axis.plot_wireframe(
        np.outer(np.cos(u), np.sin(v)),
        np.outer(np.sin(u), np.sin(v)),
        np.outer(np.ones_like(u), np.cos(v)),
        color="steelblue",
        alpha=0.12,
        linewidth=0.5,
    )

    points = np.asarray(vectors, dtype=float)
    axis.plot(points[:, 0], points[:, 1], points[:, 2], "o-", color="darkorange", label="state path")
    axis.quiver(0, 0, 0, *points[0], color="seagreen", linewidth=2, arrow_length_ratio=0.12)
    axis.quiver(0, 0, 0, *points[-1], color="crimson", linewidth=2, arrow_length_ratio=0.12)
    axis.text(*points[0], " initial", color="seagreen")
    axis.text(*points[-1], " final", color="crimson")

    axis.set_xlim(-1.05, 1.05)
    axis.set_ylim(-1.05, 1.05)
    axis.set_zlim(-1.05, 1.05)
    axis.set_box_aspect((1, 1, 1))
    axis.set_xlabel("x = <X>")
    axis.set_ylabel("y = <Y>")
    axis.set_zlabel("z = <Z>")
    axis.set_title(title)
    axis.legend(loc="upper left")
    figure.tight_layout()

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=160)
        print(f"saved figure: {output_path}")
    if show:
        plt.show()
    plt.close(figure)


def run(theta: float, phi: float, custom_sequence: Sequence[str], output_dir: Path | None) -> None:
    state = state_from_angles(theta, phi)
    initial_bloch = bloch_vector(state)
    print("Project 1b - Bloch sphere and single-qubit gates")
    print(f"input angles: theta={theta:.6f} rad, phi={phi:.6f} rad")
    print(f"initial state: {format_complex_vector(state)}")
    print(f"initial Bloch vector: {initial_bloch}")
    print_gate_table(state)

    if output_dir is not None:
        hadamard_result = apply_gate(H, state)
        plot_bloch_sphere(
            [initial_bloch, bloch_vector(hadamard_result)],
            "Hadamard gate acting on the arbitrary input state",
            output_dir / "hadamard_arbitrary.png",
        )

    print("\nRotation implementation check")
    max_error = 0.0
    for axis in ("x", "y", "z"):
        closed = rotation_closed_form(axis, math.pi / 3)
        exponential = rotation_matrix_exponential(axis, math.pi / 3)
        error = float(np.max(np.abs(closed - exponential)))
        max_error = max(max_error, error)
        print(f"  R_{axis}(pi/3) max matrix error: {error:.3e}")
    print(f"  all rotation checks pass: {max_error < 1e-12}")

    plus = state_from_angles(math.pi / 2, 0.0)
    states, path = repeated_z_rotation(plus)
    phase = relative_phase(plus, states[-1])
    print("\nRepeated Rz(pi/4) experiment")
    for step, vector in enumerate(path):
        print(f"  step {step}: {vector}")
    print(f"  final state: {format_complex_vector(states[-1])}")
    print(f"  global phase relative to |+>: {phase.real:+.6f}{phase.imag:+.6f}j")
    print(f"  Bloch vector returns to start: {np.allclose(path[0], path[-1], atol=1e-12)}")

    custom_result = apply_sequence(state, custom_sequence)
    print("\nStudent-designed gate sequence")
    print(f"  sequence: {' '.join(custom_sequence)}")
    print(f"  final state: {format_complex_vector(custom_result)}")
    print(f"  final Bloch vector: {bloch_vector(custom_result)}")

    if output_dir is not None:
        plot_bloch_sphere(
            [initial_bloch, bloch_vector(custom_result)],
            "Custom gate sequence",
            output_dir / "custom_sequence.png",
        )
        plot_bloch_sphere(
            path,
            r"Repeated $R_z(\pi/4)$ from $|+\rangle$",
            output_dir / "repeated_rz_path.png",
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--theta", type=float, default=0 * math.pi, help="initial polar angle in radians")
    parser.add_argument("--phi", type=float, default=0 * math.pi, help="initial azimuthal angle in radians")
    parser.add_argument(
        "--sequence",
        default="H T X S H",
        help="space- or comma-separated custom gate sequence (X, Y, Z, H, S, T)",
    )
    parser.add_argument("--save-dir", type=Path, default=Path("project1b_outputs"), help="directory for PNG figures")
    parser.add_argument("--no-plots", action="store_true", help="run calculations without importing matplotlib")
    parser.add_argument("--show", action="store_true", help="display figures after saving them")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    sequence = parse_sequence(args.sequence)
    output_dir = None if args.no_plots else args.save_dir
    run(args.theta, args.phi, sequence, output_dir)


if __name__ == "__main__":
    main()
