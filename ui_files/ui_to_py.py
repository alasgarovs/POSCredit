from PyQt5 import uic
import os
import subprocess


def generate_python_files():
    py_files = ['main.py', 'stakeholder.py', 'product.py', 'payment.py', 'price.py', 'document.py', 'list.py']
    ui_files = ['main.ui', 'stakeholder.ui', 'product.ui', 'payment.ui', 'price.ui', 'document.ui', 'list.ui']

    for py_file, ui_file in zip(py_files, ui_files):
        py_path = os.path.join('..', 'src/ui_pycode', py_file)
        ui_path = ui_file

        try:
            with open(py_path, 'w', encoding="utf-8") as gui:
                uic.compileUi(ui_path, gui)
            print(f"Compiled {ui_file} to {py_file}")
        except Exception as e:
            print(f"Error compiling {ui_file}: {e}")

    try:
        subprocess.run(['pyrcc5', '-o', '../src/resources_rc.py', 'resources.qrc'], check=True)
        print("Compiled resources.qrc to resources_rc.py")
    except Exception as e:
        print(f"Error compiling resources.qrc: {e}")


if __name__ == "__main__":
    generate_python_files()
