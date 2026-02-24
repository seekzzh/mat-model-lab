import os

from mml_utils.paths import resource_path

def export_model(file_path, format_type, cij_matrix, material_name="Material", crystal_type="Unknown"):
    """
    Export material model to specified format.
    
    Args:
        file_path (str): Destination file path.
        format_type (str): 'abaqus' or 'comsol'.
        cij_matrix (numpy.ndarray): 6x6 stiffness matrix (GPa).
        material_name (str): Name of the material.
        crystal_type (str): Crystal system name.
    """
    
    if format_type == 'abaqus':
        template_file = 'abaqus_umat.f'
    elif format_type == 'comsol':
        template_file = 'comsol_parameters.txt'
    else:
        raise ValueError(f"Unknown format: {format_type}")
        
    template_path = resource_path(os.path.join('assets', 'templates', template_file))
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
        
    # Prepare context
    context = {
        'material_name': material_name,
        'crystal_type': crystal_type,
    }
    
    # Add Cij values to context
    # Assuming GPa input, verify output units required by software?
    # ABAQUS/COMSOL usually require consistent units. We export the values as-is (labeled GPa in params).
    for i in range(6):
        for j in range(6):
            # 1-based indexing for template keys: C11, C12...
            key = f"C{i+1}{j+1}"
            context[key] = f"{cij_matrix[i, j]:.6f}"
            
    # Simple replacement engine
    output_content = template_content
    for key, value in context.items():
        placeholder = f"{{{{{key}}}}}" # {{key}}
        output_content = output_content.replace(placeholder, str(value))
        
    # Save to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
        
    return True
