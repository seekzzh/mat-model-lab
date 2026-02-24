# Calculation Methods and Formulas

This document describes the theoretical background and mathematical formulas used in **Mat Model Lab** for post-processing elastic constants.

---

## 1. Elastic Constants Matrices

### Stiffness Matrix (Cij)
The 6×6 stiffness matrix relates stress (σ) to strain (ε) in Voigt notation:

$$
\sigma_i = C_{ij} \varepsilon_j, \quad i,j = 1...6
$$

### Compliance Matrix (Sij)
The compliance matrix is the inverse of the stiffness matrix:

$$
S = C^{-1}
$$

It relates strain to stress: $\varepsilon_i = S_{ij} \sigma_j$

---

## 2. Voigt-Reuss-Hill (VRH) Averaging

The VRH method provides bounds and averages for polycrystalline aggregates.

### Voigt Average (Upper Bound)
Assumes uniform strain throughout the polycrystal.

**Bulk Modulus (K_V):**
$$
K_V = \frac{C_{11} + C_{22} + C_{33} + 2(C_{12} + C_{13} + C_{23})}{9}
$$

**Shear Modulus (G_V):**
$$
G_V = \frac{C_{11} + C_{22} + C_{33} - (C_{12} + C_{13} + C_{23}) + 3(C_{44} + C_{55} + C_{66})}{15}
$$

### Reuss Average (Lower Bound)
Assumes uniform stress throughout the polycrystal.

**Bulk Modulus (K_R):**
$$
K_R = \frac{1}{S_{11} + S_{22} + S_{33} + 2(S_{12} + S_{13} + S_{23})}
$$

**Shear Modulus (G_R):**
$$
G_R = \frac{15}{4(S_{11} + S_{22} + S_{33}) - 4(S_{12} + S_{13} + S_{23}) + 3(S_{44} + S_{55} + S_{66})}
$$

### Hill Average
Arithmetic mean of Voigt and Reuss bounds:

$$
K_{VRH} = \frac{K_V + K_R}{2}, \quad G_{VRH} = \frac{G_V + G_R}{2}
$$

---

## 3. Derived Elastic Properties

### Young's Modulus (E)
$$
E = \frac{9 K_{VRH} G_{VRH}}{3 K_{VRH} + G_{VRH}}
$$

### Poisson's Ratio (ν)
$$
\nu = \frac{3 K_{VRH} - 2 G_{VRH}}{6 K_{VRH} + 2 G_{VRH}}
$$

### Universal Anisotropy Index (A^U)
Measures the degree of elastic anisotropy:

$$
A^U = 5 \frac{G_V}{G_R} + \frac{K_V}{K_R} - 6
$$

- $A^U = 0$: Isotropic material
- $A^U > 0$: Anisotropic material (larger = more anisotropic)

### Cauchy Pressure (P_C)
$$
P_C = C_{12} - C_{44}
$$

- $P_C > 0$: Ionic bonding character
- $P_C < 0$: Covalent bonding character

### Pugh's Ratio (k = B/G)
Ductility/brittleness indicator:

$$
k = \frac{K_{VRH}}{G_{VRH}}
$$

- $k > 1.75$: Ductile
- $k < 1.75$: Brittle

### Hardness (Chen-Niu Model)
$$
H = 2 \left( \frac{G_{VRH}^2}{K_{VRH}} \right)^{0.585} - 3
$$

---

## 4. Directional Properties (3D Visualization)

Directional properties are calculated as functions of spherical angles (θ, φ).

### Direction Cosines
$$
l = \sin\theta \cos\phi, \quad m = \sin\theta \sin\phi, \quad n = \cos\theta
$$

### Directional Young's Modulus E(θ, φ)
$$
\frac{1}{E(\theta, \phi)} = \sum_{i=1}^{6} \sum_{j=1}^{6} S_{ij} \cdot a_i \cdot a_j
$$

where $a_i$ are products of direction cosines in Voigt notation:
- $a_1 = l^2, \quad a_2 = m^2, \quad a_3 = n^2$
- $a_4 = mn, \quad a_5 = ln, \quad a_6 = lm$

### Directional Shear Modulus G(θ, φ, χ)
Shear modulus depends on an additional angle χ (shear plane rotation):

$$
\frac{1}{G(\theta, \phi, \chi)} = 4 \sum_{ijkl} S_{ijkl} \cdot n_i \cdot m_j \cdot n_k \cdot m_l
$$

where $S_{ijkl}$ is the 4th-order compliance tensor and $\mathbf{n}$, $\mathbf{m}$ are orthogonal unit vectors.

For 3D visualization, the minimum, average, and maximum values over χ are computed.

### Directional Poisson's Ratio ν(θ, φ, χ)
$$
\nu(\theta, \phi, \chi) = -\frac{\sum_{ij} S_{ij} \cdot a_{1i} \cdot a_{2j}}{\sum_{i} S_{ii} \cdot a_{1i}^2}
$$

where $a_{1i}$ and $a_{2i}$ are direction cosine products for the loading and lateral directions.

### Linear Compressibility β(θ, φ)
$$
\beta(\theta, \phi) = \frac{1}{3 \sum_{i=1}^{6} \sum_{j=1}^{3} S_{ij} \cdot a_i}
$$

---

## 5. Mechanical Stability (Born Criteria)

A material is mechanically stable if and only if all eigenvalues of the stiffness matrix are positive:

$$
\text{Stable} \iff \lambda_i(C) > 0 \quad \forall i
$$

This is equivalent to requiring that the stiffness matrix is positive definite.

---

## 6. Wave Velocities

### Longitudinal Wave Velocity (V_L)
$$
V_L = \sqrt{\frac{K_{VRH} + \frac{4}{3}G_{VRH}}{\rho}}
$$

### Transverse Wave Velocity (V_T)
$$
V_T = \sqrt{\frac{G_{VRH}}{\rho}}
$$

### Average Wave Velocity (V_m)
$$
V_m = \left[ \frac{1}{3} \left( \frac{1}{V_L^3} + \frac{2}{V_T^3} \right) \right]^{-1/3}
$$

---

## 7. Debye Temperature

$$
\Theta_D = \frac{h}{k_B} \left( \frac{3n}{4\pi V_a} \right)^{1/3} V_m
$$

where:
- $h$: Planck's constant
- $k_B$: Boltzmann constant
- $n$: Number of atoms per formula unit
- $V_a$: Atomic volume

---

## 8. References

1. Voigt, W. (1928). *Lehrbuch der Kristallphysik*
2. Reuss, A. (1929). *Z. Angew. Math. Mech.*, 9, 49-58
3. Hill, R. (1952). *Proc. Phys. Soc.*, 65, 349-354
4. Ranganathan, S.I. & Ostoja-Starzewski, M. (2008). *Phys. Rev. Lett.*, 101, 055504
5. Chen, X.Q., Niu, H., Li, D. & Li, Y. (2011). *Intermetallics*, 19, 1275-1281
6. Born, M. & Huang, K. (1954). *Dynamical Theory of Crystal Lattices*
7. Anderson, O.L. (1963). *J. Phys. Chem. Solids*, 24, 909-917
