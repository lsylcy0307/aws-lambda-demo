import json
import sys
import requests
import logging
import pymysql

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

db_host = "memo-db-24.cluster-cpom4o48kk64.us-east-1.rds.amazonaws.com"
name = "admin"
password = "admin123"
db_name = "memo-db-24"

try:
    conn = pymysql.connect(host=db_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("could not connect to mysql")
    logger.error(e)
    sys.exit()

def lambda_handler(event, context):
    logger.info(json.dumps(event))
    request_body = json.loads(event['body'])

    memos = []
    #create a cursor object, which allows you to interact with the MySQL database by executing SQL queries and fetching results
    with conn.cursor() as cur:
        cur.execute("insert into memo (title, content) values (\"{}\", \"{}\")".format(request_body['title'], request_body['content']))
        conn.commit()
        cur.execute("select id, title from memo")

        for row in cur:
            logger.info(row)
            memos.append(row)

    conn.commit()

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     # raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "size": len(memos),
            "memos": memos
        }),
    }
