import subprocess
import sys
import os

SCRIPTS_ORDER = [
    "TIF_To_PNG.py",
    "Contour_Form.py", 
    "PDF_Making.py",
    "Merge_Custom.py",
    # "Clear_Folders.py"  # Assuming this generates the final PDF
]

# def convert_notebook(notebook_path):
#     """Convert Jupyter notebook to Python script and execute"""
#     try:
#         subprocess.run([
#             "jupyter", "nbconvert", "--to", "python", 
#             "--execute", "--inplace", notebook_path
#         ], check=True)
#         subprocess.run(["python", notebook_path.replace(".ipynb", ".py")], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Error executing {notebook_path}: {e}")
#         sys.exit(1)

def run_python_script(script_path):
    """Execute Python script"""
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    for script in SCRIPTS_ORDER:
        print(f"\n▶▶ Executing {script}")
        
        if script.endswith(".ipynb"):
            convert_notebook(script)
        elif script.endswith(".py"):
            run_python_script(script)
        else:
            print(f"Unsupported file format: {script}")
            sys.exit(1)
            
    print("\n✅ All scripts executed successfully")
    print(f"📄 Output PDF: {os.getcwd()}/final_report.pdf")
