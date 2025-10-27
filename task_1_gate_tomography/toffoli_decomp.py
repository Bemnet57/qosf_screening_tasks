#main script
# toffoli_decomp.py
# Run: python toffoli_decomp.py
import numpy as np
from math import pi, isclose
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator

# U3 helper (Qiskit convention)
def u3(theta, phi, lam):
    # Qiskit's U3 matrix
    t2 = theta / 2.0
    return np.array([
        [np.cos(t2), -np.exp(1j*lam)*np.sin(t2)],
        [np.exp(1j*phi)*np.sin(t2), np.exp(1j*(phi+lam))*np.cos(t2)]
    ], dtype=complex)

# Provided parameters for sqrt(X) and its adjoint
V_params = (pi/2, -pi/2,  pi/2)   # U3(theta, phi, lambda) -> sqrt(X)
Vdg_params = (pi/2,  pi/2, -pi/2) # U3 for sqrt(X)^\dagger

V = u3(*V_params)
Vdg = u3(*Vdg_params)
X = np.array([[0,1],[1,0]], dtype=complex)

# Numeric checks
def approx_equal(A, B, tol=1e-8):
    return np.allclose(A, B, atol=tol, rtol=0)

print("=== Single-qubit checks ===")
print("V (u3(pi/2, -pi/2, pi/2)) =\n", np.round(V, 6))
print("\nVdg (u3(pi/2, pi/2, -pi/2)) =\n", np.round(Vdg, 6))

# Check V^2 ≈ X (up to global phase)
VV = V.dot(V)
# Find global phase between VV and X: phi = arg(trace(X^† VV)/2)
phase = np.angle(np.vdot(X.flatten(), VV.flatten()))  # estimate
globalPhase = np.exp(-1j*phase)  # multiply VV by this to remove phase (approx)
VV_unphased = globalPhase * VV

print("\nCheck V * V (should equal X up to global phase):")
print("V^2 (raw) =\n", np.round(VV, 6))
print("V^2 (after removing estimated global phase) =\n", np.round(VV_unphased, 6))
print("X =\n", X)

print("\nIs V^2 equal to X up to global phase?", approx_equal(VV_unphased, X, tol=1e-7))

# Check Vdg is Hermitian adjoint of V (Vdg ≈ V^\u2020)
print("\nIs Vdg ≈ V^\\u2020 ? ", approx_equal(Vdg, V.conj().T, tol=1e-8))

# === Toffoli circuit and transpile to u3 + cx ===
print("\n=== Toffoli decomposition via transpile (basis: ['u3','cx']) ===")
ccx = QuantumCircuit(3)
ccx.ccx(0,1,2)  # control qubits: 0 & 1, target: 2

# Transpile to only u3 and cx (no optimization to keep a standard decomposition)
tgt_basis = ['u3', 'cx']
transpiled = transpile(ccx, basis_gates=tgt_basis, optimization_level=0)

print("\nTranspiled circuit (to u3 and cx):")
print(transpiled.draw(output='text'))

# Extract u3 gates and print their parameters
for inst, qargs, cargs in transpiled.data:
    name = inst.name
    if name == 'u3':
        theta = float(inst.params[0])
        phi = float(inst.params[1])
        lam = float(inst.params[2])
        # Robust extraction of qubit index for different Qiskit versions
        qubit_indices = []
        for q in qargs:
            idx = getattr(q, 'index', None)
            if idx is None:
                idx = getattr(q, '_index', None)
            qubit_indices.append(idx)
        print(f"u3({theta:.6f}, {phi:.6f}, {lam:.6f}) on qubits {qubit_indices}")


# Optional: compare unitaries of original CCX and transpiled circuit (should match)
U_ccx = Operator(ccx).data
U_trans = Operator(transpiled).data
# Check equality up to global phase:
M = U_trans.dot(U_ccx.conj().T)
# Extract phase from first non-negligible diagonal element
diag = np.diag(M)
# find a diag entry with magnitude > small threshold
idx = None
for i, val in enumerate(diag):
    if abs(val) > 1e-8:
        idx = i
        break
if idx is None:
    print("\nCould not determine global phase for checking equality.")
else:
    phi = np.angle(diag[idx])
    global_phase = np.exp(-1j*phi)
    equal_up_to_phase = approx_equal(global_phase * U_trans, U_ccx, tol=1e-7)
    print("\nAre the transpiled unitary and built-in CCX equal up to a global phase?", equal_up_to_phase)
