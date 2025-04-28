from ingestion.data_ingestion import get_XY
from ingestion.molecules import MOLECULES

def main():
    print("Available molecules:")
    for name in MOLECULES.keys():
        print(f"- {name}")

    molecule_name = input("Enter molecule name exactly as listed: ").strip()
    
    vibrational_state = int(input("Enter vibrational quantum number: "))
    rotational_state = int(input("Enter rotational quantum number: "))

    identifier = MOLECULES.get(molecule_name)

    if not identifier:
        print(f"No InChIKey found for {molecule_name}. Cannot fetch data.")
        return

    try:
        data = get_XY(identifier, vibrational_state, rotational_state)
        print("Data fetched successfully!")
        print(data)
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()
