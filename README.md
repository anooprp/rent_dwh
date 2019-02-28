# rent_dwh
Sample Python Pandas for extracting json data
This code can be scheduled to run for every hour using cron/Airflow

This will pull data from s3 to local and will load to Python data frames.I have defined total 5 data sets from the extracted json
This code will project 5 data frames and will load to a postgres instance.

The DDL for the table is defined in the DDL txt file which is part of the code base.For simplicity  I haven't fine tuned the 
data types of the table .This table design is simple and one can join tables using the 'id' column and can get the required result


