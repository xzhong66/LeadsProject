from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List

from ..schemas import LeadCreate, LeadUpdate, Lead
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


# create new lead and save to db
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Lead)
async def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    # Create a new lead instance
    try:
        db_lead = LeadModel(**lead.dict())
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email address already exists")

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
