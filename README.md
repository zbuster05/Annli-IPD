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

# Future Features

The current version of this product allows the user to run the IPD, with minimal extra work. However, there is a lack of other features that would make the product more comfortable to use. The following are some features that may be helpful.

1. **Input/output UI.** Currently, the user specifies game parameters by editing a small python file, `game_specs.py`, and all problems are logged simply to a text file, `problems.txt`. This is functional but slightly scuffed. A simple UI could make this process more streamlined.

2. **Specific search.** The results of the latest game are stored locally in `latest_raw_out.json`, including the series of plays for each matchup. These moves are omitted when the scores are logged onto the spreadsheet, for volume reasons. However, it may potentially be of interest to view the results of a specific matchup, for which a simple searching function may be helpful.

3. **Website.** The folder `ipd-online` is the initial attempt at being able to run the IPD online. The advantages of this would be the user not having to download and install various packages, as well as presumably better UI. However, there is no clean way to be able to run Python code on the browser, thus this idea was paused.

Another class of future features pertains to the students submitting the functions. Currently, there is only very simple code (in the Google Drive folder) that allows them to make sure everything compiles and takes the correct inputs/outputs. Future features may include:

1. **Test run the game.** Allow students to test their own functions in an actual IPD simulation, playing only against themselves and the default functions.

2. **Write functions easier.** Create some sort of tutorial or scaffolding to aid students who are inexperienced in writing Python code. Perhaps even allow them to follow simple templates.

Finally, future work pertaining to the code itself includes cleaning the file structure, improving documentation, and standardizing variable names. And, most importantly, more tests!!!