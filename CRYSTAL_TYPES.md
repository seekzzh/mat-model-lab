# Supported Crystal Systems and Matrix Forms

This document describes the 10 distinct crystal symmetry systems supported by **Mat Model Lab**. Below is the definition of the elastic stiffness matrix ($C_{ij}$) for each system, showing independent constants, dependent relationships, and zero elements.

## Legend

| Symbol | Meaning |
|--------|---------|
| `Cij` | Independent constant (Editable) |
| `=Cij` | Dependent constant (Equal to another) |
| `-Cij` | Dependent constant (Opposite sign) |
| `Expr` | Calculated value (e.g., Isotropic relation) |
| `.` | Zero |

---

## Overview

| # | Crystal System | Independent Constants | Symmetry |
|---|---------------|----------------------|----------|
| 1 | Triclinic | 21 | None |
| 2 | Monoclinic_1 | 13 | Diad // z-axis |
| 3 | Monoclinic_2 | 13 | Diad // y-axis |
| 4 | Orthorhombic | 9 | 3 orthogonal diads |
| 5 | Tetragonal_1 | 6 | 4/mmm |
| 6 | Tetragonal_2 | 7 | 4 |
| 7 | Trigonal_1 | 6 | -3m |
| 8 | Trigonal_2 | 7 | -3 |
| 9 | Hexagonal | 5 | 6/mmm |
| 10 | Cubic | 3 | m-3m |

---

## 1. Triclinic

**Independent Constants (21):** All $C_{ij}$ exist and are independent (symmetry $C_{ij} = C_{ji}$ always applies).

```
C11  C12  C13  C14  C15  C16
C12  C22  C23  C24  C25  C26
C13  C23  C33  C34  C35  C36
C14  C24  C34  C44  C45  C46
C15  C25  C35  C45  C55  C56
C16  C26  C36  C46  C56  C66
```

**Typical Materials:** Low-symmetry minerals, some organic crystals

---

## 2. Monoclinic_1 (Diad // x3 / z-axis)

Standard orientation for Monoclinic.

**Independent Constants (13):** C11, C12, C13, C16, C22, C23, C26, C33, C36, C44, C45, C55, C66

**Constraints:** Symmetry relative to xy-plane (z-axis normal).

```
C11  C12  C13   .    .   C16
C12  C22  C23   .    .   C26
C13  C23  C33   .    .   C36
 .    .    .   C44  C45   .
 .    .    .   C45  C55   .
C16  C26  C36   .    .   C66
```

**Typical Materials:** Gypsum, some feldspars

---

## 3. Monoclinic_2 (Diad // x2 / y-axis)

Alternative orientation.

**Independent Constants (13):** C11, C12, C13, C15, C22, C23, C25, C33, C35, C44, C46, C55, C66

**Constraints:** Symmetry relative to xz-plane.

```
C11  C12  C13   .   C15   .
C12  C22  C23   .   C25   .
C13  C23  C33   .   C35   .
 .    .    .   C44   .   C46
C15  C25  C35   .   C55   .
 .    .    .   C46   .   C66
```

---

## 4. Orthorhombic

**Independent Constants (9):** C11, C12, C13, C22, C23, C33, C44, C55, C66

**Constraints:** No coupling between normal and shear stresses.

```
C11  C12  C13   .    .    .
C12  C22  C23   .    .    .
C13  C23  C33   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C55   .
 .    .    .    .    .   C66
```

**Typical Materials:** Olivine, Topaz, Barite

---

## 5. Tetragonal_1 (Laue Group 4/mmm)

**Independent Constants (6):** C11, C12, C13, C33, C44, C66

**Constraints:**
- $C_{22} = C_{11}$
- $C_{23} = C_{13}$
- $C_{55} = C_{44}$

```
C11  C12  C13   .    .    .
C12  C11  C13   .    .    .
C13  C13  C33   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C44   .
 .    .    .    .    .   C66
```

**Typical Materials:** Rutile (TiO₂), Zircon

---

## 6. Tetragonal_2 (Laue Group 4)

**Independent Constants (7):** C11, C12, C13, C16, C33, C44, C66

**Constraints:**
- $C_{22} = C_{11}$
- $C_{23} = C_{13}$
- $C_{55} = C_{44}$
- $C_{26} = -C_{16}$

```
C11  C12  C13   .    .   C16
C12  C11  C13   .    .  -C16
C13  C13  C33   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C44   .
C16 -C16   .    .    .   C66
```

---

## 7. Trigonal_1 (Laue Group -3m)

**Independent Constants (6):** C11, C12, C13, C14, C33, C44

**Constraints:**
- $C_{22} = C_{11}$
- $C_{23} = C_{13}$
- $C_{55} = C_{44}$
- $C_{24} = -C_{14}$
- $C_{56} = C_{14}$
- $C_{66} = (C_{11} - C_{12}) / 2$

```
C11  C12  C13  C14   .    .
C12  C11  C13 -C14   .    .
C13  C13  C33   .    .    .
C14 -C14   .   C44   .    .
 .    .    .    .   C44  C14
 .    .    .    .   C14  (C11-C12)/2
```

**Typical Materials:** α-Quartz, Calcite, Sapphire

---

## 8. Trigonal_2 (Laue Group -3)

**Independent Constants (7):** C11, C12, C13, C14, C15, C33, C44

**Constraints:**
- $C_{22} = C_{11}$
- $C_{23} = C_{13}$
- $C_{55} = C_{44}$
- $C_{24} = -C_{14}$
- $C_{56} = C_{14}$
- $C_{25} = -C_{15}$
- $C_{46} = -C_{15}$
- $C_{66} = (C_{11} - C_{12}) / 2$

```
C11  C12  C13  C14  C15   .
C12  C11  C13 -C14 -C15   .
C13  C13  C33   .    .    .
C14 -C14   .   C44   .  -C15
C15 -C15   .    .   C44  C14
 .    .    .  -C15  C14  (C11-C12)/2
```

---

## 9. Hexagonal

**Independent Constants (5):** C11, C12, C13, C33, C44

**Constraints:** Transverse Isotropy.
- $C_{22} = C_{11}$
- $C_{23} = C_{13}$
- $C_{55} = C_{44}$
- $C_{66} = (C_{11} - C_{12}) / 2$

```
C11  C12  C13   .    .    .
C12  C11  C13   .    .    .
C13  C13  C33   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C44   .
 .    .    .    .    .   (C11-C12)/2
```

**Typical Materials:** Graphite, Zinc, Magnesium, Ice

---

## 10. Cubic

**Independent Constants (3):** C11, C12, C44

**Constraints:** Highest symmetry.
- $C_{22} = C_{33} = C_{11}$
- $C_{13} = C_{23} = C_{12}$
- $C_{55} = C_{66} = C_{44}$

```
C11  C12  C12   .    .    .
C12  C11  C12   .    .    .
C12  C12  C11   .    .    .
 .    .    .   C44   .    .
 .    .    .    .   C44   .
 .    .    .    .    .   C44
```

**Typical Materials:** Diamond, Silicon, Copper, Iron, Gold, NaCl

---

## Isotropic Materials (Special Case)

For truly isotropic materials, only **2 independent constants** exist:

$$
C_{44} = \frac{C_{11} - C_{12}}{2}
$$

This can be treated as a special case of Cubic symmetry.

---

## References

1. Nye, J.F. (1985). *Physical Properties of Crystals*. Oxford University Press.
2. Hearmon, R.F.S. (1961). *An Introduction to Applied Anisotropic Elasticity*. Oxford University Press.
