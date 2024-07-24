# Airflow

[Airflow-System : This Project Created By Nanthiphat T.]

[Tech Stack]

    Programing Language : Python 3.12

    Environment : Apache Airflow

    Framework : Apache Airflow

    Deployment Server : Ubuntu 22.04.2 LTS

    Deployment Tool : Docker 22.0.7 , Docker Compose v2.21.0

[Step Set Up]

[1. Install Docker and Docker Compose]

    # Add Docker's official GPG key:

    1.1 sudo apt-get update

    1.2 sudo apt-get install ca-certificates curl

    1.3 sudo install -m 0755 -d /etc/apt/keyrings

    1.4 sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc

    1.5 sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:

    1.6 echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
         $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    1.7 sudo apt-get update

    1.8 sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    1.9 docker version

[2. Install Apache Airflow]

    2.1 curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.0/docker-compose.yaml'

    2.2 Change Image (docker-compose.yaml) -> image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.9.0-python3.12}

    2.3 mkdir -p ./dags ./logs ./plugins ./config

    2.4 echo -e "AIRFLOW_UID=$(id -u)" > .env

    2.5 Change AIRFLOW_UID=1000 => 50000

[3. Deploy]

    Run This Command

        sudo docker compose up airflow-init

        sudo docker compose up

        sudo docker compose down

        sudo docker build -t apache/airflow:2.9.0-python3.12 .

        sudo docker compose up
