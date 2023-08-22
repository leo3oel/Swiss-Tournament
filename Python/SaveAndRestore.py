import json
from tkinter import messagebox as msgbox

class SaveAndRestore:

    @staticmethod
    def restore(fileName):
        try:
            if fileName:
                with open(fileName.name, 'r', encoding='utf8') as file:
                    decoded = json.load(file)
                return decoded
        except Exception as e:
            msgbox.showerror("Cannot Read File", "File is unreadable")
            print(e)

    @staticmethod
    def save(fileName, dict):
        try:
            jsonFile = json.dumps(
                dict,
                indent=4, 
                ensure_ascii=False)
            with open(fileName, "w") as file:
                file.write(jsonFile)
        except Exception as e:
            msgbox.showerror("Cannot Read File", "File is unreadable")
            print(e)
