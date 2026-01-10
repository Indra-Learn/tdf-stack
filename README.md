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
3. Install Nginx and Certbot on the VPS -
    ```sh
    apt update
    apt install -y nginx certbot python3-certbot-nginx

    # # Make sure Nginx is running:
    # systemctl status nginx

    # # 
    nano /etc/nginx/sites-available/default

    # # Update the nginx file for basic Nginx reverse proxy setup
    <!-- Main site configs are in: /etc/nginx/sites-available/ -->
    <!-- Enabled sites (symlinks) are in: /etc/nginx/sites-enabled/ -->
    # # sudo nano /etc/nginx/sites-available/default
    cat /opt/tdf-stack/tdf_others/default > /etc/nginx/sites-available/default

    # # Test and reload:
    sudo nginx -t
    sudo systemctl reload nginx

    # # Add HTTPS with Certbot
    <!-- certbot --nginx -d yourdomain.com -d api.yourdomain.com  -->
    sudo certbot --nginx -d thedatafestai.com

    # # Test and reload again:
    sudo nginx -t
    sudo systemctl reload nginx

    # # save log to "/var/log/letsencrypt/letsencrypt.log"
    ```

### Daily Activity after above "One-Time Activity" is done -

1. Run below Docker Commands to -
    ```bash
    source ./.venv/bin/activate

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


### Test The Application Using Separate Dockerfile -
```bash
cd /opt/tdf-stack
source ./.venv/bin/activate

docker build -t tdf-fastapi:0.1 ./tdf_api/
docker run -d --name tdfapi -p 8000:8000 --env-file .env -it tdf-fastapi:0.1 
docker run -d --name tdfapi -p 8000:8000 --env-file .env tdf-stack-api:latest

docker build -t tdf-streamlit:0.1 ./tdf_chatbot/
docker run --name tdfbot -d -p 8501:8501 tdf-streamlit:0.1
```

## Other Details - 

Ref:
1. https://github.com/amolnaik/pynance/blob/master/app_utility/form_13f.py

### Suggestions - 
- Nginx listens on ports 80/443 on the VPS and reverse‑proxies:
- https://yourdomain.com → Streamlit container
- https://api.yourdomain.com (or a path like /api) → FastAPI container

- A record for api.yourdomain.com → your VPS IP
- https://github.com/nileshsarkarRA/Python-Simple-ChatBot
- Kite (https://kite.trade/docs/pykiteconnect/v4/)

## error -
requests.exceptions.ConnectionError: HTTPConnectionPool(host='localhost', port=8000): Max retries exceeded with url: /company_summary/invoke (Caused by NewConnectionError("HTTPConnection(host='localhost', port=8000): Failed to establish a new connection: [Errno 111] Connection refused"))
Traceback:
File "/app/app.py", line 515, in <module>
    company_summary = call_tdf_llm_apis("company_summary", input_company_ticker)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/app/app.py", line 33, in call_tdf_llm_apis
    response = requests.post(f"http://localhost:8000/{endpoint}/invoke",
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.12/site-packages/requests/api.py", line 115, in post
    return request("post", url, data=data, json=json, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.12/site-packages/requests/api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.12/site-packages/requests/sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.12/site-packages/requests/sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.12/site-packages/requests/adapters.py", line 677, in send
    raise ConnectionError(e, request=request)