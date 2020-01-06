
## Python Script to explore historical loans data
Service that consumes a kaggle dataset on a monthly basis

## Features
- Reads data from the dataset it receives
- Aggregates the data and stores it in the database
- Interactive time-driven dashboard that displays data aggregations per field, quality of data supplied by field
- For the analysis, we will ascertain the top 25 historic IBRD borrower, we will determine their total loan disbursements, current loan obligations, and the average interest rates they were charged for all loans.
- The results of the analysis, a  DataFrame containing 25 rows, will be saved as a CSV-format data file.

## Analysis
Tool of choice: Python

Reasons:
- Has a number of libraries that support the analysis and collection of data

Library : Pandas

Reason: Due to the large amount of data there is to analyze, i chose to use the pandas library rather than 
the python CSV library for reading and organizing the loans data.


## Collecting data
Source : CSV
- The dataset contains statements of loans historical data updated on a monthly basis
- Due to the large file size, the raw copy is can be located [here](https://www.kaggle.com/theworldbank/ibrd-statement-of-loans-data/data)
- Download the dataset and place it in the same folder as the python script

## Visualization
Framework of choice: Dash
- Plotly's dash is a new framework for developing interactive web based dashboards for data visualization
- It allows one to write pure python and the framework handles the rest
- Gets data visualization solutions up and running in a relatively quick manner.
## How to run the script
-  Run the script using a Python integrated development environment (IDE) such as Spyder. 
-  To install Spyder, you will need to download the Anaconda installer.  
-  This script is written in Python 3, so you will need the Python 3.x version of the installer. After downloading and installing Anaconda, you will find the Spyder IDE by opening Anaconda Navigator.


