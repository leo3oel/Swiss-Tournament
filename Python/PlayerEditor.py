import tkinter as tk
from tkinter import ttk

class PlayerEditor(tk.Toplevel):
    def __init__(self, master, teams_with_players, callback):
        super().__init__(master)
        self.title("Player Editor")
        self.transient(master)
        self.grab_set()
        self.callback = callback

        self.teams_with_players = teams_with_players
        self.team_names = list(teams_with_players.keys())

        # Team dropdown
        dropdown_frame = tk.Frame(self)
        dropdown_frame.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="ew")
        tk.Label(dropdown_frame, text="Team:").grid(row=0, column=0, sticky="w")
        self.team_var = tk.StringVar()
        self.team_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.team_var, values=self.team_names, state="readonly")
        self.team_dropdown.grid(row=0, column=1, columnspan=2, sticky="ew")
        self.team_dropdown.current(0)
        self.team_dropdown.bind("<<ComboboxSelected>>", self.on_team_change)

        # Header row
        tk.Label(self, text="Nummer").grid(row=1, column=1)
        tk.Label(self, text="Name").grid(row=1, column=2)

        # Player fields
        self.number_vars = []
        self.name_vars = []
        self.entries = []
        self.num_players = 12
        for i in range(self.num_players):
            num_var = tk.StringVar()
            name_var = tk.StringVar()
            self.number_vars.append(num_var)
            self.name_vars.append(name_var)
            num_entry = tk.Entry(self, textvariable=num_var, width=5)
            name_entry = tk.Entry(self, textvariable=name_var, width=20)
            num_entry.grid(row=i+2, column=1)
            name_entry.grid(row=i+2, column=2)
            self.entries.append((num_entry, name_entry))

        self.load_players(self.team_names[0])

        # Save button
        save_btn = tk.Button(self, text="Speichern", command=self.save)
        save_btn.grid(row=self.num_players+2, column=1, pady=10)

        # Save & Close button
        save_close_btn = tk.Button(self, text="Speichern und Schließen", command=self.save_close)
        save_close_btn.grid(row=self.num_players+2, column=2, pady=10)

    def load_players(self, team):
        players = self.teams_with_players.get(team, [])
        
        # Sort players by number (convert to int if possible, else put at end)
        def sort_key(p):
            number = p.get('number', '')
            try:
                return int(number)
            except (ValueError, TypeError):
                return float('inf')  # Push non-numeric or missing numbers to the end

        sorted_players = sorted(players, key=sort_key)

        for i in range(self.num_players):
            num = sorted_players[i]['number'] if i < len(sorted_players) else ''
            name = sorted_players[i]['name'] if i < len(sorted_players) else ''
            self.number_vars[i].set(num)
            self.name_vars[i].set(name)

    def on_team_change(self, event=None):
        team = self.team_var.get()
        self.load_players(team)

    def save(self):
        team = self.team_var.get()
        players = []
        for num_var, name_var in zip(self.number_vars, self.name_vars):
            number = num_var.get()
            name = name_var.get()
            players.append({'number': number, 'name': name})
        self.callback(team, players)

    def save_close(self):
        self.save()
        self.destroy()

# Example usage:
if __name__ == "__main__":
    def on_save(team, players):
        print("Selected team:", team)
        print("Players:", players)

    root = tk.Tk()
    teams_with_players = {
        "Team A": [
            {'number': '1', 'name': 'Alice'},
            {'number': '2', 'name': 'Bob'},
            {'number': '3', 'name': 'Charlie'},
        ],
        "Team B": [
            {'number': '4', 'name': 'David'},
            {'number': '5', 'name': 'Eve'},
        ],
        "Team C": [
            {'number': '6', 'name': 'Frank'},
        ],
    }
    editor = PlayerEditor(root, teams_with_players, on_save)
    editor.wait_window()
    root.destroy()