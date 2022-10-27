# IPD Online (but not online)

Usable interface for running and testing code for the Iterated Prisoner's Dilemma game :)

# Get Started

1. **Download code.** Clone the repository:
    ```bash
    git clone https://github.com/annliz/IPD
    ```

2. **Get spreadsheet API key.** For security reasons, the API key is not included in the Github repository. *You need this key to run the code*. Contact Annli for the key. Then, download this file and move it into the folder `ipd_local`. Make sure it is still named `service_account.json`.

3. **Install necessary libraries.** The following Python libraries are used in this code: `numpy`, `pandas`, `gspread`, `gspread_dataframe`, `requests`, `tqdm`. Make sure you have them installed with:
    ```bash
    pip3 install LIBRARYNAME
    ```

4. **Get access to submission and results spreadsheets.** This is where students submit their code, and where result are logged. Ask Annli for access to the Google sheets.

# Running a Simulation

1. **Navigate to folder.** In your terminal, navigate to the folder `ipd_local` to run the simulation on your machine.

2. **Specify game parameters.** Edit the file `game_specs.py` to change game parameters such as noise level and score matrix.

3. **Run the game.** Run the actual simulation:
    ```bash
    python3 main.py
    ```

4. **View results.** View the results of the game at the results spreadsheet that has been shared with you. This sheet only saves the results of the latest run, so if you want to save these results permanently, create a copy.

5. **Read error log.** All submissions that had issues of any sort are logged in `problems.txt`. Make sure to read this file and notify students of their issues so they can fix their code.