# Tennis Match Simulator
This project simulates tennis matches between chosen two players based on their statistical data.  The program pulls data from the Ultimate Tennis Statistics website using web scraping techniques and uses metrics such as ace percentage, win rates on serves and more to predict results of multiple matches and output most probable scores.

# Features
- Simulate a user-defined number of tennis matches
- Use real-world player statistics from the Ultimate Tennis Statistics website
- Adjust number of sets in a match (best of 3 or 5)
- View the most frequent match and set scores
- Track detailed match outcomes such as wins, game outcomes, and tie-break performance
- Use proxy for web scraping if required



# Usage
Clone the repository:
```bash
git clone https://github.com/WileQ/Tennis_prediction_algorithm.git
cd Tennis_prediction_algorithm
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run it:
```bash
python code/main.py
```

Input Fields:

Number of matches: Specify how many matches you want to simulate.

Best of sets: Choose whether the matches are best of 3 or best of 5 sets.

Player names: Provide the full names of the two players to simulate.

Use Proxy: If you need to use a proxy, you can input your proxy details in the format (ip):(port).

Example input:
- How many games do you want to simulate: 100
- Best of 3 or 5 sets: 3
- Tennis player who will serve first: Novak Djokovic
- Tennis player who will serve second: Andy Murray
- Do you want to use a proxy (yes/no): no

# Output details
After running the simulations, the program will output:
- Most Frequent Match Scores: Displays the 5 most frequent match outcomes.
- Most Frequent Set Scores: Displays the 10 most frequent set outcomes.
- Overall Wins: A summary showing how many matches each player won across the simulations.

# Notes and limitations
Notes and Limitations
- Data Source: The program depends on the Ultimate Tennis Statistics website for data, so changes to the website may require updates to the scraping code.
- Selenium Setup: Ensure that the ChromeDriver is compatible with the version of Chrome installed on your machine.
- Simulation Accuracy: The simulation is based on probabilities and may not perfectly replicate real-world results, especially for edge cases like rare player matchups or unconventional statistics.

# License
This project is licensed under the Apache License 2.0.
