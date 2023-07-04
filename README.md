# Bed Clock Alarm

```
brew install redis-server 
redis-server # install and run redis server to persist User off-limit hours

pip install requirements.txt

python control_loop.py # run Alarm Clock Control Loop
python server.py # run Flask Server to load calendar webpage, and save to redis cache
```

`localhost:5001` 
