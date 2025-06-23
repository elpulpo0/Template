import os

def pytest_sessionfinish(session, exitstatus):
    db_path = "./test.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Fichier supprimé : {db_path}")
