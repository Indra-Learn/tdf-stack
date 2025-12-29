# tdf-stack
tdf-stack with Streamlit, Fastapi and N8N applications 


## Follow The Below Steps To Develop Same Applications -


### One-Time Activity -

1. Clone The GitHub Repo - 
    ```bash
    git clone 
    ```
2. Create Python Virtual Environment -
    ```bash
    cd /opt/tdf-stack

    sudo apt update
    sudo apt install python3-venv

    python3 -m venv .venv
    source ./.venv/bin/activate

    python3 -m pip install --upgrade pip
    pip install -r ./requirements.txt

    apt install docker-compose
    ```

### Daily Activity after above "One-Time Activity" is done -

1. Run below Docker Commands to -
    ```bash
    docker compose up -d --build
    docker down

    # docker image ls
    # docker ps -a
    # docker stop <container>
    # docker rm -f <container>
    # docker rmi -f <image>
    ```

### Applications -

| ID  | App Name | App Details | Reference |
| --- | :------- | ----------- | --------- |
| 1. | [TDF-ChatBot](http://thedatafestai.com:8501`) | `streamlit run ./tdf_chatbot/app.py`| |
| 2. | [TDF-Api](http://72.61.231.147:8000) | `python3 tdf_api/app.py`</br>`streamlit run ./tdf_api/client.py` | |


## 
```bash
cd /opt/tdf-stack
source ./.venv/bin/activate

docker build -t api:0.1 ./tdf_api/
docker run -d --name tdfapi -p 8000:8000 --env-file .env -it tdf-fastapi:0.1 

docker build -t client:0.1 ./tdf_chatbot/
docker run --name tdfbot -d -p 8501:8501 tdf-streamlit:0.1
```
