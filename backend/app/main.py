from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.geoapify import get_restaurants
from fastapi.responses import FileResponse
from app.excel.excel_service import create_excel
from app.utils.cache import restaurant_cache
from fastapi import HTTPException

app = FastAPI(title="Restaurant Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Restaurant Intelligence API is running 🚀"
    }

@app.get("/restaurants")
def restaurants(city: str, limit: int = 100):

    restaurant_list = get_restaurants(city, limit)
    cache_key = f"{city.lower()}_{limit}"
    restaurant_cache[cache_key] = restaurant_list

    return {
        "city": city,
        "count": len(restaurant_list),
        "restaurants": restaurant_list
    }

@app.get("/download")
def download(city: str, limit: int = 100):

    cache_key = f"{city.lower()}_{limit}"
    restaurant_list = restaurant_cache.get(cache_key, [])

    if not restaurant_list:
        raise HTTPException(
        status_code=404,
        detail="No cached data found. Please search restaurants first."
        )

    file_name = create_excel(restaurant_list, city)

    return FileResponse(
        path=file_name,
        filename=file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )