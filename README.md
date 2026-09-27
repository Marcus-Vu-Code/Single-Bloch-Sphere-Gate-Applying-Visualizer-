# Physics 161 Project 1b: Interactive Bloch Sphere

This project demonstrates how single-qubit gates transform quantum states and
how those transformations appear geometrically on the Bloch sphere. It has
two complementary parts:

- `project1_bloch_sphere.py` performs the calculations, creates figures, and
  verifies the rotation formulas numerically.
- `bloch_sphere_app.html` is a browser-based interactive visualization with
  animated gate buttons, reset, state readouts, gate history, and a draggable
  three-dimensional view.

## Interactive web app

The app supports the standard single-qubit gates `X`, `Y`, `Z`, `H`, `S`, and
`T`. Choose an initial state from:

- Computational/Z basis: `|0>` or `|1>`
- Hadamard/X basis: `|+>` or `|->`
- Y basis: `|+i>` or `|-i>`
- Custom Bloch-sphere angles `theta` and `phi`

The app uses the conventional axes: computational states are the ±z poles,
Hadamard states are ±x, and ±i states are ±y. The display reports the
statevector, Bloch coordinates `(x, y, z) = (<X>, <Y>, <Z>)`, measurement
probabilities, vector length, and the most recent gate matrix.

### Run locally

Requirements: Node.js 18 or newer.

```powershell
node serve_app.js
```

Open <http://localhost:8000/bloch_sphere_app.html> in a browser. Stop the
server with `Ctrl+C`.

The server has no external Node dependencies. It serves only files from this
project directory and defaults to `127.0.0.1:8000`. To use another port:

```powershell
$env:PORT=8080
node serve_app.js
```

## Python calculation project

Requirements: Python 3.10 or newer, NumPy, and Matplotlib.

Create an environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the calculation and generate the Bloch-sphere figures:

```powershell
python project1_bloch_sphere.py
```

Use `--show` to open the figures interactively or `--no-plots` to run the
calculations without importing Matplotlib. The generated images are saved in
`project1b_outputs/`.

Useful customization example:

```powershell
python project1_bloch_sphere.py --theta 1.2 --phi 2.0 --sequence "H T Y Z"
```

## What the calculations demonstrate

For

`|psi> = cos(theta/2)|0> + exp(i phi) sin(theta/2)|1>`,

the program computes the Bloch vector from Pauli expectation values. It
applies `X`, `Y`, `Z`, `H`, `S`, and `T`; compares the closed-form rotation

`R_k(gamma) = cos(gamma/2) I - i sin(gamma/2) sigma_k`

with an independent eigendecomposition-based matrix exponential; and applies
`R_z(pi/4)` eight times to `|+>`. The Bloch vector returns to its starting
point while the statevector acquires the global phase `-1`.

## Tests

```powershell
python -m unittest -v
```

The test suite checks normalization, known gate transformations, rotation
agreement, global phase, sequence validation, and zero-vector handling.

## Project files

| File | Purpose |
| --- | --- |
| `bloch_sphere_app.html` | Interactive browser visualization |
| `serve_app.js` | Dependency-free local web server |
| `project1_bloch_sphere.py` | Executable numerical/plotting project |
| `test_project1_bloch_sphere.py` | Python unit tests |
| `project1b_outputs/` | Generated Bloch-sphere figures |
| `Project1b_Evaluative_Writeup.md` | Evaluation draft to personalize |
| `requirements.txt` | Python dependencies |

## Assignment note

The evaluative write-up is a working draft. Rewrite it in your own voice and
describe your own execution, predictions, and changes before submitting. The
required execution video must also be recorded separately.
