from typing import Optional

from app.core.security import verify_password, get_password_hash
from app.schemas.user import UserInDB

# In-memory user "database"
DUMMY_USERS_DB: dict[str, UserInDB] = {
    "testuser": UserInDB(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("testpassword")
    )
}

def get_user(username: str) -> Optional[UserInDB]:
    return DUMMY_USERS_DB.get(username)

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """
    Authenticate a user.
    """
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
