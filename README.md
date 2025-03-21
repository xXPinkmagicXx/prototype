# prototype
This contains the proto type for the course Software Architecture


# Run the code

## Run the FastAPI

To start the application
```bash
uvicorn api:app --reload
```

Open another teminal

```bash
python send_requests.py
```
The output should be something like
```bash
running main
Now creating 5000 users.
Now getting 5000 users.
Create users: avg response time (ms):  2.6273900985717775 ; requests per second:  380.5068684495124
Get users: avg response time (ms):   1.2473440170288086 ; requests per second:  801.3403155317231
```