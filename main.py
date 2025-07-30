from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
import hashlib
import secrets
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient


# --- Config ---
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "cascadefund"
USERS_COLLECTION = "users"

app = FastAPI()

# Mongo client and collection
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[DB_NAME]
users_collection = db[USERS_COLLECTION]

# --- Request and response models ---
class RootResponse(BaseModel):
    message: str

class AccessTokenRequest(BaseModel):
    code: str

class AccessTokenResponse(BaseModel):
    id: str
    name: str
    session: str
    avatar_url: Optional[str] = None

# --- Helper functions ---
async def exchange_code_for_access_token(code: str) -> str:
    url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data=data, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        access_token = data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token from GitHub")
        return access_token

async def get_github_user_info(token: str) -> dict:
    url = "https://api.github.com/user"
    headers = {"Authorization": f"token {token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

def hash_token(token: str, salt: Optional[bytes] = None) -> (str, bytes):
    if not salt:
        salt = secrets.token_bytes(16)  # 16 bytes salt
    hashed = hashlib.pbkdf2_hmac("sha256", token.encode(), salt, 100000)
    return hashed.hex(), salt

# --- API endpoint ---
@app.get("/", response_model=RootResponse)
async def root():
    return {"message": "CascadeFund API"}

@app.post("/user/access-token", response_model=AccessTokenResponse)
async def create_access_token(request: AccessTokenRequest):
    # Exchange code for github access_token
    access_token = await exchange_code_for_access_token(request.code)

    # Get github user info
    user_info = await get_github_user_info(access_token)
    github_id = str(user_info.get("id"))
    name = user_info.get("name") or user_info.get("login")
    avatar_url = user_info.get("avatar_url")

    if not github_id or not name:
        raise HTTPException(status_code=400, detail="Invalid user info returned from GitHub")

    # Check user in db
    user_doc = await users_collection.find_one({"id": github_id})

    # Generate salt and hashed session token
    hashed_token, salt = hash_token(access_token)

    if not user_doc:
        # New user, insert document
        user_doc = {
            "id": github_id,
            "name": name,
            "avatar_url": avatar_url,
            "hashed_access_token": hashed_token,
            "salt": salt.hex(),
        }
        await users_collection.insert_one(user_doc)
    else:
        # Update existing user's token and salt
        await users_collection.update_one(
            {"id": github_id},
            {"$set": {
                "hashed_access_token": hashed_token,
                "salt": salt.hex(),
                "name": name,
                "avatar_url": avatar_url,
            }}
        )

    # Return response
    return AccessTokenResponse(
        id=github_id,
        name=name,
        session=hashed_token,
        avatar_url=avatar_url
    )

