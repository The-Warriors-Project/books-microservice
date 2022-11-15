# Books-Microservice
This program is build as part of a Cloud Computing Class at Columbia University.

### Microservice Properties
- FastAPI 
- Python 3.10 
- Pymysql

### Steps to run the program locally

1. Add environment configuration for DB_USER_NAME, DB_PASS, and DB_RDS_HOST.

2. Install the requirements file 
`pip install -r requirements.txt` 

3. Make sure the AWS RDS instance is on.

4. Run the command to activate the program 
`uvicorn main:app --host 0.0.0.0 --port 5011`

Open [http://0.0.0.0:5011/docs](http://0.0.0.0:5011/docs) to view the updated swagger in your browser.