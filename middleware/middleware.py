from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

def setup_cors(app: FastAPI):
    origins = [
        "http://localhost:5173",     
        "http://127.0.0.1:5173",  
        "http://localhost:3000",    
        "http://127.0.0.1:3000", 
    ]    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "X-Requested-With",
            "Accept",
            "Origin",
            "User-Agent",
            "Referer"
        ],
        expose_headers=["*"],
        max_age=600, 
    )