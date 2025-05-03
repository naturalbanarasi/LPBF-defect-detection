import os
import shutil

# Configuration - Replace these paths with your actual folder paths
FOLDERS_TO_CLEAN = [
    "Compatible_Input",
    "Processed_Images", 
    "Processed_Stats",

]

def clean_folders():
    """Delete all files from specified folders while preserving directory structure"""
    for folder in FOLDERS_TO_CLEAN:
        if not os.path.exists(folder):
            print(f"⚠️ Folder not found: {folder}")
            continue
            
        print(f"\n🔍 Scanning {folder}...")
        file_count = 0
        
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    file_count += 1
                    print(f"🗑️ Deleted: {filename}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"🗂️ Deleted directory: {filename}")
            except Exception as e:
                print(f"❌ Error deleting {filename}: {str(e)}")
        
        print(f"✅ Finished cleaning {folder} - Removed {file_count} items")

if __name__ == "__main__":
    print("🚀 Starting cleaning process...")
    clean_folders()
    print("\n✨ All operations completed!")

