```markdown
# Daily Delhi Climate - Temperature Forecasting Pipeline

**Group 2:** Paulette Dushime | Mahe Digne | Samuel Gakuru Wanjohi  
**Date:** March 2026  

## 1. Introduction: What is this project?
Welcome to our time-series data pipeline! This project aims to predict the daily average temperature in New Delhi, India. 

Delhi experiences extreme weather, dropping to 6°C in the winter and soaring to nearly 39°C in the summer. Accurate weather forecasting is incredibly important for farmers planning their crops, city planners managing electricity grids, and public health officials preparing for heatwaves. 

To solve this problem, our team took over 4 years of daily weather data and built a complete software system from scratch. Our system cleans the raw data, stores it in two different types of databases, hosts a web server (API) to manage the records, and uses a Machine Learning model (Artificial Intelligence) to accurately guess tomorrow's temperature based on today's weather patterns.

## 2. Project Explanation: The 4 Main Tasks We Completed

* **Task 1: Data Cleaning & AI Training:** We explored a public Kaggle dataset containing Delhi's climate data from 2013 to 2017. We looked for trends and created new data points, like 7-day moving averages and 1-day lags (because yesterday's temperature is the best predictor of today's). We then trained a Random Forest Machine Learning model to find patterns and predict future temperatures.
* **Task 2: Database Design:** We built two databases to safely store our weather records:
  * A structured relational database using **MySQL** (designed with 3 connected tables).
  * A flexible document database using **MongoDB Atlas** (storing everything in nested JSON format).
* **Task 3: Building the API:** We created a web server using **FastAPI**. This acts as a bridge, allowing users to Create, Read, Update, and Delete (CRUD) weather records from both databases simply by sending web requests.
* **Task 4: AI Prediction Script:** We wrote a standalone Python script that automatically grabs the latest weather data from our API, feeds it into our trained AI model, and prints out a live prediction for tomorrow's temperature.

---

## 3. Logical Folder Structure
To keep our code clean and easy to read, we have logically organized our files into separate folders for the server code, databases, raw data, machine learning, scripts, and outputs.

```text
delhi-climate-pipeline/
├── api/
│   └── main.py                  # Our FastAPI web server and database routes
├── database/
│   ├── schema.sql               # The MySQL table designs and queries
│   └── mongodb_queries.txt      # The MongoDB document structure and queries
├── data/
│   ├── DailyDelhiClimateTrain.csv # The raw historical data used for training
│   └── DailyDelhiClimateTest.csv  # The raw data used for testing
├── ml/
│   └── notebook.ipynb           # Our data exploration and AI training workspace
├── models/
│   ├── best_model.pkl           # The saved Random Forest AI brain
│   └── metadata.json            # Details about how accurate the AI is
├── scripts/
│   └── predict_latest.py        # The script that makes the actual weather forecast
├── outputs/
│   └── data_visualizations.png  # Saved graphs and terminal execution logs
├── requirements.txt             # The list of Python tools needed to run this
└── README.md                    # The project documentation

```

---

## 4. Instructions for Reproducing Results (How to Run Locally)

If you want to run this project on your own computer and reproduce our exact results, please follow these step-by-step instructions.

**Step 1: Download the Code and Install Tools**
First, clone this repository to your computer and install the required Python libraries.

```bash
git clone <paste-your-github-repo-link-here>
cd delhi-climate-pipeline
pip install -r requirements.txt

```

**Step 2: Reproduce the AI Model**
To reproduce how we cleaned the data and trained the AI:

1. Open the `ml/notebook.ipynb` file in Jupyter Notebook or Google Colab.
2. Run all the code cells from top to bottom.
3. The notebook will automatically train the model, show the accuracy scores, and save a new `best_model.pkl` file into the `models/` folder. It will also generate graphs that you can save to the `outputs/` folder.

**Step 3: Set Up the MySQL Database**
You need a local MySQL database to store the relational data.

1. Open your MySQL terminal on your computer.
2. Create a database named `assignment_db`.
3. Create a user named `paulette_api` with the password `AgriPredict123!`.
4. Give that user full permissions to the database.
5. Run the code inside `database/schema.sql` to build the 3 empty tables.
*(Note: Our MongoDB database is hosted in the cloud via Atlas. The connection link is already in the code, so you do not need to set up anything locally for it!)*

**Step 4: Turn on the API Server**
Make sure you are in the main project folder in your terminal, and then start the FastAPI web server:

```bash
python3 -m uvicorn api.main:app --reload

```

Once the terminal says "Application startup complete", open your web browser and go to: **http://127.0.0.1:8000/docs**. You will see a fully interactive dashboard where you can test all the CRUD and time-series endpoints!

**Step 5: Run the AI Prediction Script**
Leave the API running in the background. Open a *new* terminal window, make sure you are in the main project folder, and run our final forecast script:

```bash
python3 scripts/predict_latest.py

```

This script will fetch the latest data from the API, process the 11 required weather features, load the `best_model.pkl`, and print the final predicted temperature for the next day directly to your terminal screen.

---

## 5. Team Contributions

* **Paulette Dushime:** Designed the MySQL and MongoDB database structures, wrote the SQL/NoSQL queries, created the Task 4 automated prediction script, and wrote the project documentation (README).
* **Mahe Digne:** Handled the Machine Learning. Explored the data, answered the 5 analytical questions, performed feature engineering, and trained/exported the final Random Forest prediction model.
* **Samuel Gakuru Wanjohi:** Built the FastAPI integration. Wrote the web server code, connected the Python app to both databases, created the CRUD and time-series endpoints, and managed the GitHub repository setup.

```
