import shutil
import os

def cleanup(dir1, dir2, db, acro):
    try:
        if os.path.exists(dir1):
            for filename in os.listdir(dir1):
                file_path = os.path.join(dir1, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    shutil.rmtree(file_path)  # For subdirectories

        if os.path.exists(dir2):
            for filename in os.listdir(dir2):
                file_path = os.path.join(dir2, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    shutil.rmtree(file_path)  # For subdirectories
        
        if os.path.exists(db):
                os.remove(db)
        
        if os.path.exists(acro):
                os.remove(acro)
    
    except Exception as e:
        print("An error occurred during cleanup:", e)