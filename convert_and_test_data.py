import os
import re
import numpy as np

# Constants for unit conversion
NM_TO_BOHR = 1/0.0529177210903  # 1 nm = 1/0.0529177210903 Bohr
NM_TO_HARTREE = 45.6337117  # 1 nm wavelength ≈ 45.6337117 Hartree
CROSS_SECTION_TO_AO2 = 1e12  # 1 cm² = 10^12 a₀²

def ensure_converted_directory():
    """Ensure the converted_results directory exists, create if it doesn't"""
    conv_dir = os.path.join(os.path.dirname(__file__), 'converted_results')
    if not os.path.exists(conv_dir):
        os.makedirs(conv_dir)
    return conv_dir

def validate_filename(filename):
    """Validate if filename matches the expected pattern and extract info"""
    pattern = r'^(H2\+|HeH\+|He2\+|CaH\+|LiH\+|MgH\+|NaH\+)_rot_(\d{2})_vib_(\d{2})\.dat$'
    match = re.match(pattern, filename)
    if match:
        return match.groups()  # Returns (molecule, rot_num, vib_num)
    return None

def read_and_convert_data(filepath):
    """Read data and convert to atomic units"""
    wavelengths = []
    cross_sections = []
    
    with open(filepath, 'r') as f:
        next(f)  # Skip header
        for line in f:
            wl, cs = line.strip().split()
            # Convert wavelength (nm) to Hartree
            energy_hartree = NM_TO_HARTREE / float(wl)
            # Convert cross section (Å²) to atomic units (a₀²)
            cs_atomic = float(cs) * CROSS_SECTION_TO_AO2
            
            wavelengths.append(energy_hartree)
            cross_sections.append(cs_atomic)
    
    return np.array(wavelengths), np.array(cross_sections)

def save_converted_data(molecule, rot_num, vib_num, energies, cross_sections, conv_dir):
    """Save converted data in atomic units"""
    # Create molecule directory if it doesn't exist
    mol_dir = os.path.join(conv_dir, molecule.replace('+', ''))
    if not os.path.exists(mol_dir):
        os.makedirs(mol_dir)
    
    # Save data with atomic units prefix
    filename = f"au_{molecule}_rot_{rot_num}_vib_{vib_num}.dat"
    filepath = os.path.join(mol_dir, filename)
    
    # Save with header and data
    with open(filepath, 'w') as f:
        f.write("# Energy(Hartree) CrossSection(a0^2)\n")
        for e, cs in zip(energies, cross_sections):
            f.write(f"{e:.8e} {cs:.8e}\n")
    
    return filepath

def main():
    # Ensure directories exist
    conv_dir = ensure_converted_directory()
    download_dir = os.path.join(os.path.dirname(__file__), 'downloaded_results')
    
    # Check if downloaded_results exists
    if not os.path.exists(download_dir):
        print("Error: downloaded_results directory does not exist")
        print("Please run download_results.py first")
        return 1
    
    # Process each file
    print("Converting files to atomic units...")
    print("-" * 50)
    
    files_processed = 0
    for filename in os.listdir(download_dir):
        # Validate filename and extract info
        result = validate_filename(filename)
        if not result:
            continue
        
        molecule, rot_num, vib_num = result
        filepath = os.path.join(download_dir, filename)
        
        try:
            # Read and convert data
            energies, cross_sections = read_and_convert_data(filepath)
            
            # Save converted data
            output_path = save_converted_data(
                molecule, rot_num, vib_num,
                energies, cross_sections,
                conv_dir
            )
            
            rel_path = os.path.relpath(output_path, conv_dir)
            print(f"Converted {filename} -> {rel_path}")
            files_processed += 1
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    print("-" * 50)
    print(f"Successfully converted {files_processed} files to atomic units")
    return 0

if __name__ == "__main__":
    exit(main())
