# Physics 161 Project 1b: Evaluative Write-up

## AI-use disclosure

I used AI assistance to help organize the Python implementation, check syntax,
and suggest test cases. I reviewed the mathematics, selected the initial
angles and custom gate sequence, ran the program, and interpreted the output
myself. AI was not used to replace my explanation of what I learned from the
experiment.

## Evaluation

For Project 1b, I wrote a Python program that connects the matrix description
of single-qubit gates to the geometric picture of the Bloch sphere. The code
creates an arbitrary pure state from two angles, theta and phi, and then
calculates its three Bloch coordinates as the expectation values of the Pauli
X, Y, and Z operators. I chose theta = 0.73 pi and phi = 0.31 pi for the
initial state. I also included X, Y, Z, H, S, and T gates so that I could
compare gates that visibly move the state with phase gates whose effects are
less obvious in the computational-basis amplitudes.

The part that stretched me most was implementing rotations in two different
ways. The first implementation uses the closed form

`R_k(gamma) = cos(gamma/2) I - i sin(gamma/2) sigma_k`.

The second treats the exponent as a matrix and evaluates its exponential using
an eigendecomposition. The program compares the two matrices numerically for
the x, y, and z axes. This test helped me understand that the trigonometric
formula is not an unrelated shortcut: it follows from the special algebra of
the Pauli matrices. It also gave me a concrete way to find an implementation
error instead of trusting a plot that might look plausible.

The repeated-rotation experiment was the most useful result. Starting with
the plus state, I applied R_z(pi/4) eight times. Each step moved the Bloch
vector by another 45 degrees around the equator, and after eight steps the
Bloch vector returned to its original coordinates. At the same time, the
final statevector was related to the initial state by a factor of -1. Before
writing this program, I tended to treat that difference as evidence that the
state had changed physically. Comparing the statevector and the Bloch vector
side by side made the distinction between global phase and an observable
change much clearer: a global phase changes the vector of complex amplitudes,
but it does not change measurement probabilities or the physical point on the
Bloch sphere.

I also added the custom sequence `H T X S H`. This was useful because it made
me predict a result for a less familiar combination instead of only repeating
examples from class. I learned that a sequence has to be read right-to-left
when it is written as a product of matrices, while a program that applies
gates in a loop naturally describes the chronological order. Checking the
initial and final Bloch vectors helped me catch that conceptual issue.

The main difficulty during the implementation was keeping numerical roundoff
from looking like a physical effect. Values that should be zero appeared as
very small numbers, so I used `allclose` tolerances for comparisons and
normalized the state after each gate. A second difficulty was making a plot
that showed a path rather than only a final point. The repeated-rotation plot
solved that by drawing every intermediate Bloch vector. The unit tests then
checked the calculations without depending on visual judgment alone.

As a follow-up, I would extend the program to mixed states using density
matrices. That would show points inside the Bloch sphere rather than only on
its surface and would make the connection between pure-state rotations and
decoherence more concrete. I would also compare the ideal gate sequence with a
small numerical noise model to see which features of the trajectory are most
fragile.
