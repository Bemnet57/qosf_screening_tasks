# Gate Tomography — Toffoli Gate Decomposition

## QOFS Quantum Computing Mentorship Screening Task 1

### 📘 Task Description

The goal is to find the parameters of two U3(θ, φ, λ) gates such that the following circuit is equivalent to a Toffoli (CCX) gate.
Each U3 represents a single-qubit rotation used in the decomposition of a Toffoli into basic gates (U3 and CX).

The task tests understanding of universal gate sets and circuit equivalence.

### 🧮 Theoretical Background

In Qiskit,

𝑈
3
(
𝜃
,
𝜙
,
𝜆
)
=
(
cos
⁡
(
𝜃
2
)
	
−
𝑒
𝑖
𝜆
sin
⁡
(
𝜃
2
)


𝑒
𝑖
𝜙
sin
⁡
(
𝜃
2
)
	
𝑒
𝑖
(
𝜙
+
𝜆
)
cos
⁡
(
𝜃
2
)
)
U3(θ,ϕ,λ)=(
cos(
2
θ
	​

)
e
iϕ
sin(
2
θ
	​

)
	​

−e
iλ
sin(
2
θ
	​

)
e
i(ϕ+λ)
cos(
2
θ
	​

)
	​

)

A Toffoli gate (CCX) can be implemented using controlled-√X and controlled-√X† gates, alongside CNOTs and phase rotations.
Thus, the task reduces to finding the parameters of √X and √X† in the U3 form.

### ✅ Derived Parameters

The two gates are:

Operation	U3(θ, φ, λ) parameters	Equivalent name
√X (V)	U3(π/2, -π/2, π/2)	Square-root of X
√X† (V†)	U3(π/2, π/2, -π/2)	Adjoint (inverse) of √X

These satisfy:

𝑉
2
=
𝑋
and
𝑉
†
=
𝑉
−
1
V
2
=XandV
†
=V
−1

up to a global phase.

### 🧠 Verification Approach

A Python script (toffoli_decomp.py) was written using Qiskit and NumPy to:

Construct both U3 matrices from the parameters above.

Verify numerically that 
𝑉
2
=
𝑋
V
2
=X up to a global phase.

Confirm 
𝑉
†
≈
𝑉
†
V
†
≈V
†
 (Hermitian conjugate).

Build a Toffoli circuit (ccx) and transpile it into only {u3, cx} gates to check that these same parameters appear.

Compare the full 3-qubit unitary matrices of both circuits for equivalence up to a global phase.

### 🖥️ How to Run
1️⃣ Setup  
```bash
git clone https://github.com/Bemnet57/quantum-gate-tomography-qofs.git  
cd quantum-gate-tomography-qofs  
python -m venv qc-env
# activate virtualenv:
# Windows:
qc-env\Scripts\activate
# Linux/macOS:
source qc-env/bin/activate  
pip install -r requirements.txt
```
2️⃣ Run script
```bash
python toffoli_decomp.py
```

You should see:

The printed matrices for V and Vdg

A confirmation that V^2 = X (up to global phase)

A text-based Toffoli decomposition containing multiple u3 and cx gates

The final check confirming the decomposed circuit and built-in Toffoli are equivalent

### 📊 Sample Output (abridged)
```bash
=== Single-qubit checks ===
Is V^2 equal to X up to global phase? True
Is Vdg ≈ V† ? True

=== Toffoli decomposition via transpile (basis: ['u3','cx']) ===
u3(1.570796, -1.570796, 1.570796) on qubits [2]
u3(1.570796, 1.570796, -1.570796) on qubits [2]
...
Are the transpiled unitary and built-in CCX equal up to a global phase? True
```
### 📚 Key Takeaways

Any unitary operation can be expressed as a combination of a universal set such as {U3, CX}.

The Toffoli gate’s equivalence relies on decomposing multi-controlled operations into smaller rotations and entangling gates.

U3(π/2, -π/2, π/2) and its adjoint are fundamental in this decomposition as the √X building blocks.

### 🧾 References

Qiskit Textbook — Universal single-qubit gates

Nielsen & Chuang, Quantum Computation and Quantum Information (Chapter 4)

IBM Quantum documentation for U3

### 👨🏽‍💻 Author

Bemnet Asseged  
QOFS Quantum Mentorship Screening Submission  
(October 2025)