import subprocess
import sys
import os
import shutil

def check_install(package):
    """Check if a package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def install_package(package):
    """Install a package via pip."""
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def clean_build_dirs(dist_name="dist"):
    """Clean previous build directories."""
    print(f"Cleaning previous builds in {dist_name}...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists(dist_name):
        shutil.rmtree(dist_name)

def build_pyinstaller():
    """Build using PyInstaller."""
    # Ensure PyInstaller is installed
    if not check_install("PyInstaller"):
        install_package("pyinstaller")
    
    clean_build_dirs("dist")
    print("Starting PyInstaller build...")
    
    separator = ";" if os.name == 'nt' else ":"
    # Use absolute path for assets to be safe
    assets_src = os.path.abspath("assets")
    assets = f"{assets_src}{separator}assets"
    
    cmd = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        "--windowed",
        "--onefile",
        f"--add-data={assets}",
        f"--paths={os.getcwd()}",
        # Core modules
        "--hidden-import=core",
        "--hidden-import=core.Young_3D",
        "--hidden-import=core.ElasticVRH3D",
        "--hidden-import=core.StableofMechanical",
        # Utils modules
        "--hidden-import=mml_utils",
        "--hidden-import=mml_utils.data_io",
        "--hidden-import=mml_utils.report_generator",
        "--hidden-import=mml_utils.material_db",
        "--hidden-import=mml_utils.code_export",
        # GUI modules
        "--hidden-import=gui",
        "--hidden-import=gui.main_window",
        "--hidden-import=gui.modules",
        "--hidden-import=gui.modules.elasticity",
        "--hidden-import=gui.modules.elasticity.widget",
        "--hidden-import=gui.widgets",
        "--hidden-import=gui.widgets.about_dialog",
        "--hidden-import=gui.widgets.documentation_dialog",
        "--hidden-import=gui.widgets.material_browser",
        "--hidden-import=gui.widgets.plot_canvas",
        # Visualization modules
        "--hidden-import=visualization",
        "--hidden-import=visualization.ElasticPlot_3D",
        "--hidden-import=visualization.ElasticPlot_2D",
        "--hidden-import=visualization.Plot_Slice",
        # Third-party
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        "--hidden-import=matplotlib.backends.backend_qtagg",
        "--hidden-import=scipy",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=docx",
        "--name=MatModelLab",
        f"--icon={os.path.abspath('assets/icon.ico')}",
        "main.py"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    
    print("\n" + "="*50)
    print("PyInstaller Build Successful!")
    print(f"Executable: {os.path.abspath('dist/MatModelLab.exe')}")
    print("="*50)

def main():
    build_pyinstaller()

if __name__ == "__main__":
    # Ensure we run from the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\nError during build: {e}")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        input("Press Enter to exit...")
    else:
        print("\nDone.")
