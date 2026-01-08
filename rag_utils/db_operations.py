import os
import shutil
import gc
import time
DB_DIR = os.path.join("DATA", "DB")
DOCS_DIR = os.path.join("DATA", "Docs")
def delete_db():
    """Delete the entire DB folder."""
    if not os.path.exists(DB_DIR):
        return False, "DB folder does not exist."

    # Force any cached Chroma objects to release file locks
    gc.collect()
    time.sleep(0.3)

    try:
        shutil.rmtree(DB_DIR)
        return True, "DB folder deleted successfully."
    except PermissionError:
        # Retry once after a short wait
        time.sleep(0.7)
        gc.collect()
        try:
            shutil.rmtree(DB_DIR)
            return True, "DB folder deleted successfully."
        except PermissionError:
            return False, "DB is still in use. Please stop the Streamlit app (Ctrl+C) and try again."
        

def add_txt_file(file_name, content):
    """Add a .txt file to the Docs folder."""
    if not file_name.endswith('.txt'):
        return False, "File extension must be .txt"
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
    file_path = os.path.join(DOCS_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return True, f"{file_name} added to Docs folder."

def add_md_file(file_name, content):
    """Add a .md file to the Docs folder."""
    if not file_name.endswith('.md'):
        return False, "File extension must be .md"
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
    file_path = os.path.join(DOCS_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return True, f"{file_name} added to Docs folder."

def delete_txt_files():
    """Delete all .txt files from the Docs folder."""
    if not os.path.exists(DOCS_DIR):
        return False, "Docs folder does not exist."
    deleted = 0
    for file in os.listdir(DOCS_DIR):
        if file.endswith('.txt'):
            os.remove(os.path.join(DOCS_DIR, file))
            deleted += 1
    return True, f"Deleted {deleted} .txt files from Docs folder."

def delete_md_files():
    """Delete all .md files from the Docs folder."""
    if not os.path.exists(DOCS_DIR):
        return False, "Docs folder does not exist."
    deleted = 0
    for file in os.listdir(DOCS_DIR):
        if file.endswith('.md'):
            os.remove(os.path.join(DOCS_DIR, file))
            deleted += 1
    return True, f"Deleted {deleted} .md files from Docs folder."

def delete_all_docs_files():
    """Delete all files from the Docs folder."""
    if not os.path.exists(DOCS_DIR):
        return False, "Docs folder does not exist."
    deleted = 0
    for file in os.listdir(DOCS_DIR):
        file_path = os.path.join(DOCS_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            deleted += 1
    return True, f"Deleted {deleted} files from Docs folder."


def delete_db_after_app_stops():
    """
    Helper: Creates a script to delete DATA/DB after Streamlit app is stopped,
    then restarts the app automatically.
    """
    script_path = "delete_and_restart.bat"
    with open(script_path, "w") as f:
        f.write(f"""@echo off
timeout /t 2
rmdir /s /q "{DB_DIR}"
streamlit run main_streamlit_v2.py
""")
    return script_path, "Batch script created. Please close the Streamlit app, then double-click delete_and_restart.bat to delete DB and restart the app."
