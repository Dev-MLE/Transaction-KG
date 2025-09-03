from src.kg_manager.loader import load_excel
from src.kg_manager.manager import Neo4jKGManager
import os


def main():
    # === Step 1: Load Excel data ===
    file_path = "transactions.xlsx"  # <-- replace with your actual file
    df = load_excel(file_path)

    # === Step 2: Neo4j credentials (from env vars) ===
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    if not uri or not user or not password:
        raise ValueError("Please set NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD environment variables.")

    # === Step 3: Run KG Manager ===
    kg_manager = Neo4jKGManager(uri, user, password)

    try:
        print("Creating constraints...")
        kg_manager.create_constraints()

        print("Importing data...")
        kg_manager.import_data(df, batch_size=2000)

        print("✅ Data import completed successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        kg_manager.close()


if __name__ == "__main__":
    main()
