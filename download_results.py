import os
import json
from ingestion.data_ingestion import get_XY
from ingestion.molecules import MOLECULES

def ensure_download_directory():
    """Ensure the downloaded_results directory exists, create if it doesn't"""
    download_dir = os.path.join(os.path.dirname(__file__), 'downloaded_results')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir

def parse_quantum_numbers(line):
    """Parse a line to get rotational and vibrational quantum numbers"""
    parts = [p.strip() for p in line.split('|')]
    if len(parts) >= 4:
        name = parts[1].strip()
        l = parts[2].strip()  # rotational quantum number
        n_values = parts[3].strip()  # vibrational quantum numbers
        if l != 'NULL' and n_values != 'NULL':
            return name, int(l), [int(n) for n in n_values.split(',')]
    return None, None, None

def get_molecular_denotation(name):
    """Get the molecular denotation for a given name"""
    if name == 'Calcium monohydride cation':
        return 'CaH+'
    elif name == 'Helium hydride cation':
        return 'HeH+'
    elif name == 'Helium molecular ion':
        return 'He2+'
    elif name == 'Hydrogen molecular ion':
        return 'H2+'
    elif name == 'Lithium hydride cation':
        return 'LiH+'
    elif name == 'Magnesium monohydride cation':
        return 'MgH+'
    elif name == 'Sodium hydride cation':
        return 'NaH+'
    return ''

def save_molecular_data(molecule_name, rot_num, vib_num, data, download_dir):
    """Save molecular data to a file"""
    denotation = get_molecular_denotation(molecule_name)
    if not denotation:
        return
    
    # Format numbers as two digits
    rot_str = f"{rot_num:02d}"
    vib_str = f"{vib_num:02d}"
    
    # Create filename
    filename = f"{denotation}_rot_{rot_str}_vib_{vib_str}.dat"
    filepath = os.path.join(download_dir, filename)
    
    # Save data
    wavelengths = data[0]
    cross_sections = data[1]
    
    with open(filepath, 'w') as f:
        f.write("# Wavelength(nm) DifferentialCrossSection\n")
        for wl, cs in zip(wavelengths, cross_sections):
            f.write(f"{wl} {cs}\n")
    
    print(f"Saved data to {filename}")

# Create download directory
download_dir = ensure_download_directory()

# Read and process the quantum_ranges file
quantum_ranges_path = os.path.join(os.path.dirname(__file__), 'data', 'quantum_ranges')

# First, show available quantum ranges
print("\nQuantum ranges for molecular ions:")
print("-" * 80)

current_molecule = None
with open(quantum_ranges_path, 'r') as f:
    # Skip header lines
    next(f); next(f); next(f)
    
    for line in f:
        line = line.strip()
        if line.startswith('+'): # Skip table formatting lines
            continue
            
        name, l, n_values = parse_quantum_numbers(line)
        if name and l is not None and n_values:
            if current_molecule != name:
                current_molecule = name
                denotation = get_molecular_denotation(name)
                if denotation:
                    print(f"\n{name} ({denotation}):")
                    print("  Rotational(l) Vibrational(n)")
                    print("  " + "-" * 30)
            print(f"  l = {l:<8} n = {min(n_values)}..{max(n_values)} ({len(n_values)} values)")

# Now download data for each quantum state
print("\nDownloading data for all quantum states...")
print("-" * 80)

with open(quantum_ranges_path, 'r') as f:
    # Skip header lines
    next(f); next(f); next(f)
    
    for line in f:
        line = line.strip()
        if line.startswith('+'): # Skip table formatting lines
            continue
            
        name, l, n_values = parse_quantum_numbers(line)
        if name and l is not None and n_values:
            denotation = get_molecular_denotation(name)
            if denotation:
                # Get the InChIKey for this molecule
                identifier = MOLECULES.get(denotation)
                if not identifier:
                    print(f"Warning: No InChIKey found for {denotation}")
                    continue
                
                print(f"\nProcessing {name} ({denotation}) with l={l}:")
                # Download data for each vibrational state
                for n in n_values:
                    try:
                        data = get_XY(identifier, n, l)
                        save_molecular_data(name, l, n, data, download_dir)
                    except Exception as e:
                        print(f"Error fetching data for {denotation} (l={l}, n={n}): {e}")
