import os
import subprocess


def _run_stocks():
    folders = ["asia", "europe", "usa"]

    for folder in folders:
        folder_path = os.path.join("collector/scraper/stocks", folder)
        if os.path.isdir(folder_path):
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        print(f"Ausführen der Datei: {file_path}")
                        subprocess.run(["python3", file_path], check=True)
                        print(f"Die Datei wurde erfolgreich ausgeführt: {file_path}")
                        
        else:
            print(f"Der Ordner {folder_path} existiert nicht.")


