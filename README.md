# Yahoo-Finance-Stock-Data-Pipeline-with-Airflow-PostgreSQL-and-Metabase
Real-time ETL pipeline integrated with metabase for visualization and constructing dashboard on stock market data
Overview
This project is a data pipeline that extracts stock market data from Yahoo Finance, processes it using Airflow, stores the results in a PostgreSQL database, and visualizes the data using Metabase. The pipeline automates the collection of stock information such as stock codes, names, prices, market changes, and volumes for the most active stocks, transforming and storing it for analysis and reporting.


Features

Data Extraction: Scrapes live stock data from Yahoo Finance using BeautifulSoup.
Data Transformation: Scales relevant numerical fields for better analysis using MinMaxScaler.
Data Storage: Loads the processed data into a PostgreSQL database.
Data Visualization: The data is integrated into a Metabase dashboard for real-time stock monitoring and insights.

Architecture
The pipeline follows a standard ETL (Extract, Transform, Load) architecture using the following components:

Extract: Web scraping with Python using BeautifulSoup and requests.

Transform: Data normalization and processing with pandas and sklearn.

Load: Data insertion into PostgreSQL.

Orchestration: Managed with Apache Airflow to ensure automated data flow.

Visualization: Dashboard built with Metabase for displaying key metrics.

Project Structure
.
├── dags/
│   ├── stock_functions.py  # Contains the extract, transform, and load functions
│   └── stock_pipeline.py   # Defines the Airflow DAG for the pipeline
├── requirements.txt        # Lists project dependencies
├── Dockerfile              # Builds the project in a containerized environment
├── README.md               # Project documentation
└── metabase_dashboard/     # Metabase dashboard setup files

Data Pipeline Tasks

Extract Task:
This task scrapes the Yahoo Finance website for the most active stocks using the URL: https://finance.yahoo.com/markets/stocks/most-active/. Stock codes, names, prices, market changes, and volumes are retrieved and structured as JSON data.

Transform Task:
The scraped data is normalized using MinMaxScaler from sklearn to scale the numerical columns (prices, market changes, volumes) while leaving categorical data (stock codes, names) intact. This ensures the data is well-prepared for analysis and visualization.

Load Task:
The transformed data is inserted into a PostgreSQL table (stocks). Each stock’s code, name, price, market change, and volume are stored in rows, ready for querying and further analysis.

Metabase Integration
Once the data is loaded into PostgreSQL, it is visualized through Metabase, a user-friendly business intelligence tool. A custom dashboard is created that displays:

Stock codes and names.
Market prices.
Percentage changes in market prices.
Stock trading volumes.
This dashboard allows users to monitor stock performance at a glance and analyze trends across various metrics.

Installation
Prerequisites
Docker: The project uses Docker to run Airflow and PostgreSQL in containers.
Metabase: Used for data visualization.
Python 3.8+: Required to run the ETL tasks.
Steps
Clone the Repository:

git clone https://github.com/your-username/yahoo-finance-stock-data-pipeline.git
cd yahoo-finance-stock-data-pipeline
Set up Docker Environment: The project uses Docker for both Airflow and PostgreSQL. You need to have Docker installed on your system.

Build and run the Docker containers:
docker-compose up --build
Install Python Dependencies: Ensure all dependencies are installed.

pip install -r requirements.txt
Set Up Airflow: Once the Docker environment is running, navigate to Airflow at localhost:8080 and trigger the DAG (Stock_Finance_Data). This will start the ETL pipeline.

Connect PostgreSQL to Metabase: After loading the data into PostgreSQL, configure Metabase to connect to the PostgreSQL database. You can then use Metabase to create and customize dashboards for stock data analysis.

Usage
Run the Pipeline:

Start the Airflow DAG manually to initiate the ETL process.
The DAG will extract stock data from Yahoo Finance, transform it, and load it into the PostgreSQL database.
Monitor Data in Metabase:

Open Metabase at localhost:3000, connect to the PostgreSQL database, and view the stock data in your custom dashboard.
The dashboard provides insights into stock market prices, changes, and volumes.
Troubleshooting
Airflow Task Failures: Check the Airflow logs for any task failures, and ensure that the DAG is properly configured.
Database Connection Issues: Verify the connection credentials for PostgreSQL and ensure the database is running.
Metabase Dashboard Issues: Ensure the Metabase setup points to the correct PostgreSQL database, and refresh the dataset if necessary.
Future Enhancements
Real-Time Updates: Automate the pipeline to run at scheduled intervals for real-time stock data tracking.
Additional Metrics: Expand the pipeline to include more stock data points such as P/E ratios, dividends, etc.
Improved Visualizations: Add more sophisticated visualizations in Metabase, such as trendlines and comparative stock analyses.
