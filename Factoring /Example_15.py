"""
Factoring and period finding
"""

import numpy as np
import pandas as pd

from qiskit import QuantumCircuit
import sys

np.set_printoptions(threshold=sys.maxsize)

from fractions import Fraction

from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram


# Directly prepare the quantum state:
def get_coeffs(x, N, n_q, n_count):
    """
    x-> guess
    N-> target number
    n_q -> number of qubits
    n_count -> number qubits for qft #t
    """
    vec = np.zeros(2 ** n_q)
    base = 1
    for i in range(2 ** n_count):
        s1 = np.binary_repr(i, n_count)
        mod2 = np.mod(base, N)
        base = mod2 * x
        s2 = np.binary_repr(mod2, n_q - n_count)
        print(i, mod2, s1, s2)
        vec[int(s2 + s1, 2)] = 1
    return vec


def qft_dagger(n):
    """n-qubit QFTdagger the first n qubits in circ"""
    qc = QuantumCircuit(n)
    # Don't forget the Swaps!
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / float(2 ** (j - m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc


# Example: x=3, N=15:

x = 3
N = 15
n_q = 10  # total number of Qubits (QFT_register + a**i_register)
n_count = 4  # number of qubits of QFT_register

print("x:", x)
print("N:", N)
print("n_q:", n_q)
print("n_count:", n_count)

vec = get_coeffs(x, N, n_q, n_count)
vec =  np.multiply(vec, 1/np.sqrt(2**n_count))
print("vec:", vec)

## Simulation:

Q = QuantumCircuit(n_q,n_count)
Q.initialize(vec)

Q.append(qft_dagger(n_count),range(n_count))
Q.measure(range(n_count),range(n_count))
Q.draw(fold=-1)  # -1 means 'do not fold'

aer_sim = Aer.get_backend('aer_simulator')
t_qc = transpile(Q, aer_sim)
qobj = assemble(t_qc)
results = aer_sim.run(qobj).result()
counts = results.get_counts()
plot_histogram(counts)

## Compute the continuous fraction, and obtain from there the candidate factors:

rows, measured_phases = [], []
for output in counts:
    decimal = int(output, 2)  # Convert (base 2) string to decimal
    phase = decimal/(2**n_count)  # Find corresponding eigenvalue
    measured_phases.append(phase)

    # Add these values to the rows in our table:
    frac = Fraction(phase).limit_denominator(N)
    #rows.append([f"{output}(bin) = {decimal:>3}(dec)", f"{decimal}/{2**n_count} = {phase:.2f}",f"{frac.numerator}/{frac.denominator}", frac.denominator, np.gcd(x**(frac.denominator//2)-1, N), np.gcd(x**(frac.denominator//2)+1, N)])
    rows.append([f"{output}(bin) = {decimal:>3}(dec)", f"{frac.numerator}/{frac.denominator}", frac.denominator, np.gcd(x**(frac.denominator//2)-1, N), np.gcd(x**(frac.denominator//2)+1, N)])
# Print the rows in a table
#headers=["Register Output", "Phase", "Fraction", "Guess for r", "guess1","guess2"]
headers=["Register Output", "Fraction", "Guess for r", "guess1","guess2"]
df = pd.DataFrame(rows, columns=headers)
print(df)



