from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any
from pathlib import Path
import uvicorn

# Import your existing backend logic
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from router import router
from general import generalchat
# We assume browse.py exists from the previous step
from browse import fetch_restaurants, fetch_menu

# --- APP CONFIGURATION ---
app = FastAPI(title="Relaxdash API")

# Allow CORS so your React app (running on localhost:3000) can hit this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- STARTUP EVENT ---
@app.on_event("startup")
def startup_event():
    """Load resources when the API starts."""
    faqs_path = Path(__file__).parent / "resources/FAQ_Relaxdash.csv"
    ingest_faq_data(faqs_path)
    print("✅ FAQ Data Ingested")

# --- DATA MODELS (Pydantic) ---
# These define the shape of the JSON data your React app sends/receives

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: List[Message] = []

class ChatResponse(BaseModel):
    response: str
    route_used: str

class Restaurant(BaseModel):
    id: int
    name: str
    address: str

class MenuItem(BaseModel):
    name: str
    description: str
    price: float
    dietary_type: str

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "Relaxdash API is running"}

# In main.py

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        # 1. Convert history safely
        history_dicts = [msg.model_dump() for msg in request.history]
        
        # 2. Router Logic (WITH SAFETY FIX)
        # We capture the object first, then safely extract the name.
        route_obj = router(request.query)
        
        # If .name is None, default to "general"
        route = route_obj.name if route_obj.name else "general"
        
        response_text = ""
        
        # 3. Execution Logic
        if route == 'faq':
            response_text = faq_chain(request.query)
        elif route == 'sql':
            response_text = sql_chain(request.query)
        else:
            # General chat handles the fallback
            response_text = generalchat(request.query, history_dicts)
            
        # 4. Return Response
        # Now 'route' is guaranteed to be a string ("general"), so it won't crash.
        return ChatResponse(response=response_text, route_used=route)

    except Exception as e:
        print(f"❌ SERVER CRASH: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/restaurants", response_model=List[Restaurant])
def get_restaurants():
    """Fetches all restaurants for the Browse page."""
    try:
        data = fetch_restaurants()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/restaurants/{restaurant_id}/menu", response_model=List[MenuItem])
def get_menu(restaurant_id: int):
    """Fetches menu for a specific restaurant."""
    try:
        data = fetch_menu(restaurant_id)
        if not data:
            raise HTTPException(status_code=404, detail="Menu not found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- RUNNER ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)