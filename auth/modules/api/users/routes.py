from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from utils.logger_config import configure_logger
from modules.database.dependencies import get_users_db
from modules.api.users.functions import get_current_user, get_user_by_email
from modules.api.users.schemas import UserResponse, UserCreate, RoleUpdate, UserUpdate
from modules.api.users.models import User, Role
from modules.api.auth.security import anonymize, hash_password

logger = configure_logger()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

users_router = APIRouter()


@users_router.get("/users/me", response_model=UserResponse)
def read_users_me(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_users_db)
):
    user = get_user_by_email(current_user.sub, db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        role=user.role.role,
    )


@users_router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Retrieve a user by ID",
    description="Returns the information of a specific user based on their ID.",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_users_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        role=user.role.role,
    )


@users_router.get("/users", response_model=list[UserResponse])
def get_all_users(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_users_db)
):
    if "admin" not in current_user.scopes:
        raise HTTPException(
            status_code=403, detail="Access denied: administrators only."
        )

    users = db.query(User).all()

    return [
        UserResponse(
            id=u.id,
            name=u.name,
            email=u.email,
            is_active=u.is_active,
            role=u.role.role,
        )
        for u in users
    ]


@users_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_users_db),
):
    if "admin" not in current_user.scopes:
        raise HTTPException(
            status_code=403,
            detail="Access denied: administrators only.",
        )

    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found.")

    db.delete(user_to_delete)
    db.commit()

    return JSONResponse({"message": "User deleted"})


@users_router.post(
    "/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user_data: UserCreate, db: Session = Depends(get_users_db)):
    anonymized_email = anonymize(user_data.email)
    existing_user = get_user_by_email(anonymized_email, db)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="A user with this email already exists."
        )

    role_obj = db.query(Role).filter_by(role="reader").first()
    if not role_obj:
        raise HTTPException(
            status_code=500, detail="The role 'reader' could not be found."
        )

    new_user = User(
        email=anonymized_email,
        name=user_data.name,
        hashed_password =hash_password(user_data.password),
        role_id=role_obj.id,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        is_active=new_user.is_active,
        role=new_user.role.role,
    )


@users_router.patch("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role_update: RoleUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_users_db),
):
    if "admin" not in current_user.scopes:
        raise HTTPException(
            status_code=403, detail="Access denied: administrators only."
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    new_role = db.query(Role).filter(Role.role == role_update.role).first()
    if not new_role:
        raise HTTPException(status_code=404, detail="The role could not be found.")

    user.role_id = new_role.id
    db.commit()
    db.refresh(user)

    return JSONResponse({"message": f"User role updated to '{new_role.role}'."})


@users_router.patch("/users/me", response_model=UserResponse)
def update_current_user(
    update_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_users_db),
):
    user = get_user_by_email(current_user.sub, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if update_data.name:
        user.name = update_data.name

    if update_data.email:
        user.email = anonymize(update_data.email)

    if update_data.password:
        user.hashed_password = hash_password(update_data.password)

    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        role=user.role.role,
    )


@users_router.patch("/users/{user_id}", response_model=UserResponse)
def admin_update_user(
    user_id: int,
    update_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_users_db),
):
    if "admin" not in current_user.scopes:
        raise HTTPException(
            status_code=403, detail="Access denied: administrators only."
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if update_data.name:
        user.name = update_data.name

    if update_data.email:
        user.email = anonymize(update_data.email)

    if update_data.password:
        user.hashed_password = hash_password(update_data.password)

    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        role=user.role.role,
    )
