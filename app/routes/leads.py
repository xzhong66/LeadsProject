import os
import uuid
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from ..schemas import LeadUpdate, Lead
from ..models import Lead as LeadModel
from ..database import get_db
from ..auth import get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from ..email import send_email

router = APIRouter(
    prefix="/leads",
    tags=["leads"],
)


class Token(BaseModel):
    access_token: str
    token_type: str


print("API started")


# create new lead and save to db
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Lead)
async def create_lead(request: Request, db: Session = Depends(get_db)):
    print("Received request")

    # Get the form data
    form_data = await request.form()
    first_name = form_data.get("first_name")
    last_name = form_data.get("last_name")
    email = form_data.get("email")
    resume = form_data.get("resume")

    # Check if the email already exists in the database
    existing_lead = db.query(LeadModel).filter(LeadModel.email == email).first()
    if existing_lead:
        raise HTTPException(status_code=400, detail="Email address already exists")

    # Save the resume file
    resume_filename = f"{uuid.uuid4().hex}_{resume.filename}"
    resume_path = f"resumes/{resume_filename}"

    print("Resume path is:" + resume_path)

    if not os.path.exists(resume_path):
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(resume_path), exist_ok=True)

    with open(resume_path, "wb") as file:
        contents = await resume.read()
        file.write(contents)

    db_lead = LeadModel(
        first_name=first_name,
        last_name=last_name,
        email=email,
        resume_path=resume_path
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    # Send email notifications
    prospect_email = send_email(
        db_lead.email, "Lead Submission Received", "Thank you for submitting your information."
    )
    attorney_email = send_email(
        "attorney@company.com",
        "New Lead Received",
        f"A new lead has been received: {db_lead.first_name} {db_lead.last_name}",
    )

    return db_lead


# get all leads from db
@router.get("/", response_model=List[Lead])
async def get_leads(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Only authenticated attorneys can access this route
    if current_user != "attorney@company.com":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access leads")
    leads = db.query(LeadModel).all()
    return leads


# get lead based on id
@router.get("/{lead_id}", response_model=Lead)
async def get_lead(lead_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Only authenticated attorneys can access this route
    if current_user != "attorney@company.com":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access leads")
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return lead


# update the lead status according to lead id
@router.patch("/{lead_id}", response_model=Lead)
async def update_lead_state(lead_id: int, lead_update: LeadUpdate, db: Session = Depends(get_db),
                            current_user: str = Depends(get_current_user)):
    # Only authenticated attorneys can update lead state
    if current_user != "attorney@company.com":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update lead state")
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    lead.state = lead_update.state
    db.commit()
    db.refresh(lead)
    return lead


# route for user login
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Hardcode email and password for demo purpose
    user_email = "attorney@company.com"
    password = "password"

    if form_data.username == user_email and form_data.password == password:
        # Create and return a JWT token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"email": user_email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/resumes/{resume_filename}")
async def get_resume(resume_filename: str, current_user: str = Depends(get_current_user)):
    # Only authenticated attorneys can access this route
    if current_user != "attorney@company.com":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access resumes")
    resume_path = f"resumes/{resume_filename}"
    return FileResponse(resume_path)
