import sys
from getpass import getpass
from sqlalchemy.orm import Session
from backend.db.database import SessionLocal, engine
from backend.db import db_models
from backend.core.auth_utils import get_password_hash

def main():
    print("--- Admin User Creation ---")
    db = SessionLocal()
    
    username = input("Enter admin username: ")
    if db.query(db_models.User).filter(db_models.User.username == username).first():
        print("Error: A user with this username already exists.")
        db.close()
        sys.exit(1)
        
    password = getpass("Enter admin password: ")
    
    hashed_password = get_password_hash(password)
    
    admin_user = db_models.User(
        username=username,
        hashed_password=hashed_password,
        role=db_models.UserRole.ADMIN # Set the role to admin!
    )
    
    db.add(admin_user)
    db.commit()
    
    print(f"Admin user '{username}' created successfully.")
    db.close()

if __name__ == "__main__":
    # Ensure the tables are created
    db_models.Base.metadata.create_all(bind=engine)
    main()