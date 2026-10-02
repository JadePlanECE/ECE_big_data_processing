# Lab 5

We will use uv environment for this lab.

## First PowerShell


We start by launching the docker
```bash
docker compose up -d
```

We go get the link for the jupyterhub, and follow the logs of jupyterhub
```bash
docker logs -f pyspark_notebook
```

[something like this](http://localhost:8888/lab?token=b7db1872c28adf1272ba68e8955addfd126e1f716816441e)
[something like that](http://127.0.0.1:8888/lab?token=b7db1872c28adf1272ba68e8955addfd126e1f716816441e)

## Second PowerShell

We create and activate the virtuam environment
```bash
uv venv
```
```bash
uv pip install -r requirements.txt
```
```bash
.venv\Scripts\activate
```

We run the admin.py file
```bash
uv run admin.py
```

We run the wikistream_producer.py file
```bash
uv run wikistream_producer.py
```

On the jupyterlab, we can run the notebook, and see the result on the first PowerShell from the logs

To enrich the code, we can change the notebook, on cell 5 (A simple aggregation of raw data by number of bot edits), line 5 from `window(col("event_time"), "1 hour"),` to `window(col("event_time"), "1 hour", "15 minutes"),`

We can change the streaming input from french to english in `wikistream_producer.py` file, line 27 from `stream.register_filter(server_name='fr.wikipedia.org', type='edit')` to `stream.register_filter(server_name='en.wikipedia.org', type='edit')`
