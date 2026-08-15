from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from typing import List, Dict, Any
import os
import downloader

app = FastAPI(title="Tickerrer API")

@app.get("/api/data")
def get_stored_data() -> List[Dict[str, Any]]:
    """API endpoint to provide the data being stored by the downloader module."""
    data = downloader.get_data()
    return data

@app.post("/api/data")
def update_stored_data(data: List[Dict[str, Any]]) -> Dict[str, str]:
    """API endpoint to store or update downloader data."""
    downloader.save_data(data)
    return {"message": "Data saved successfully"}

@app.get("/api/chart")
def get_chart() -> FileResponse:
    """API endpoint to serve the rendered chart based on stored data."""
    chart_path = downloader.generate_chart()
    if not os.path.exists(chart_path):
        raise HTTPException(status_code=404, detail="Chart image not found")
    return FileResponse(chart_path, media_type="image/png")
