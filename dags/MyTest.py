from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import oracledb
import io
import smtplib
import unicodecsv as csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
#import pytds
from datetime import timedelta, datetime, date
import pytz



def read_data():
    

    
    try:
        df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQnYo1SZES9qS1vuhvAySa0kzP9Gblw1sPxsAj0V-kUzQqK3nwu8sVSgtGzuFyPMZhLQfu5HzeVhtAC/pub?gid=401314020&single=true&output=csv')
        
        print(type(df))
        print(df)
        
        return df
    
    except oracledb.Error as error:
        print(error)
  

            
def send_email_func(**kwargs):
    ti = kwargs["ti"]
    df = ti.xcom_pull(task_ids="read_data", key="return_value")


    if df is None:
        body = "<h2>Daily Report : Test</h2><h3>เกิดข้อผิดพลาดในการเชื่อมต่อกับ Oracle DB</h3>"
    else:
        body = "<h2>Daily Report : Test</h2><h3>ตาราง : สรุปผลรวมงาน</h3>"
        body += df.to_html(index=False)  # Ensure correct encoding
	#.to_html(index=False)
    
    try:
        # ข้อมูลเชื่อมต่อ SMTP server
        sender_email = "sender_email"
        receiver_email = "receiver_email"
        # receiver_email = "kollathee.wis@casmatt.co.th"
        password = "sender_password"

        # สร้างออบเจ็กต์ MIMEMultipart
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Airflow System : Test"

        

        # สร้างเนื้อหาของอีเมล
        #body = "<h2>Daily Report : Test</h2>"
        #body += "<h3>ตาราง : สรุปผลรวมงาน</h3>"
        #body += df.to_html(index=False)

        # เพิ่มเนื้อหาของอีเมล
        message.attach(MIMEText(body, "html", "utf-8"))

        # Convert DataFrame to CSV and attach
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)  # Ensure correct encoding
        csv_buffer.seek(0)  # Move to the start of the buffer

        attachment = MIMEApplication(csv_buffer.getvalue().encode('utf-8'), Name="Data.csv")
        attachment['Content-Disposition'] = 'attachment; filename="Data.csv"'
        message.attach(attachment)

        # เชื่อมต่อ SMTP server และส่งเมล
        with smtplib.SMTP_SSL("mail.tqm.co.th", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("ส่งอีเมลเรียบร้อยแล้ว!")

    except Exception as e:
        print("เกิดข้อผิดพลาดในการส่งอีเมล:", e)           
 

default_args = {
    'owner': 'MyTest',
    'depends_on_past': False,
}


dag = DAG(
    dag_id='MyTest',
    default_args=default_args,
    catchup=False,
    description='Execute query ',
    start_date= datetime(2024, 4, 24, 16, 30, 0, 0), #days_ago(1),
    schedule_interval= '0 * * * *',
)


read_data = PythonOperator(
    task_id='read_data',
    python_callable=read_data,
    dag=dag,
)

send_email = PythonOperator(
    task_id='send_email',
    python_callable=send_email_func,
    op_kwargs={'df': '{{ ti.xcom_pull(task_ids="read_data") }}'},
    dag=dag,
)

#send_email = PythonOperator(
#    task_id='send_email',
#    python_callable=send_email,
#    dag=dag,
#)

read_data  >> send_email

