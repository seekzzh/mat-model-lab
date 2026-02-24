# Core calculation functions for Mat Model Lab

from .young import Young_3D
from .bulk import Bulk_3D
from .poisson import Poisson_3D, Poisson_4D
from .shear import Shear_3D, Shear_4D
from .hardness import Hardness_3D, Hardness_4D
from .elastic_vrh import ElasticVRH3D

# New modules
from .stability import StableofMechanical, check_stability_detailed
from .crystal_type import (
    get_crystal_type_name, 
    get_independent_constants,
    get_enabled_indices,
    fill_symmetric_matrix,
    identify_crystal_type,
    list_crystal_types,
    CRYSTAL_TYPES_3D,
    CRYSTAL_TYPES_2D
)
from .conversions import (
    D2toD3,
    D3toD2,
    Direction2Ang,
    Ang2Direction,
    rotate_stiffness_matrix
)

__all__ = [
    # Original modules
    'Young_3D',
    'Bulk_3D',
    'Poisson_3D',
    'Poisson_4D',
    'Shear_3D',
    'Shear_4D',
    'Hardness_3D',
    'Hardness_4D',
    'ElasticVRH3D',
    # Stability
    'StableofMechanical',
    'check_stability_detailed',
    # Crystal type
    'get_crystal_type_name',
    'get_independent_constants',
    'get_enabled_indices',
    'fill_symmetric_matrix',
    'identify_crystal_type',
    'list_crystal_types',
    'CRYSTAL_TYPES_3D',
    'CRYSTAL_TYPES_2D',
    # Conversions
    'D2toD3',
    'D3toD2',
    'Direction2Ang',
    'Ang2Direction',
    'rotate_stiffness_matrix'
]