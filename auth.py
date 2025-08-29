from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.auth.security import authenticate_user, create_access_token, get_current_user, create_user_session
from app.auth.schemas import UserLogin, Token, PasswordChange, UserResponse
from app.models.user import User
from app.core.config import get_settings
from datetime import timedelta
import logging

settings = get_settings()
router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """User login endpoint"""
    
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    # Create user session
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    create_user_session(
        db=db,
        user_id=user.id,
        token=access_token,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    logging.info(f"User {user.username} logged in successfully")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # seconds
        "user": UserResponse.from_orm(user)
    }

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """User logout endpoint"""
    
    # Here you would typically invalidate the session
    # For now, we'll just log the logout
    
    logging.info(f"User {current_user.username} logged out")
    
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse.from_orm(current_user)

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    
    from app.auth.security import verify_password, hash_password
    
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.hashed_password = hash_password(password_data.new_password)
    db.commit()
    
    logging.info(f"User {current_user.username} changed password")
    
    return {"message": "Password changed successfully"}

@router.post("/refresh-token")
async def refresh_token(current_user: User = Depends(get_current_user)):
    """Refresh access token"""
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username, "role": current_user.role, "user_id": current_user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }