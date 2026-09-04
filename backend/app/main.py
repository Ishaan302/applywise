# What should happen when an HTTP request reaches this endpoint?

from fastapi import FastAPI,HTTPException, Depends  # calling get_db() nd give taking database session
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm  # 
from .utils.auth import hash_password, verify_password, create_access_token, get_current_user
from .utils.analytics_engine import applications_to_df, compute_stats, compute_weekly_trend, compute_funnel
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)  #creating database tables 

app = FastAPI(title="Job Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

#creating new application
@app.post("/applications", response_model=schemas.ApplicationOut)  # means the response should follow the ApplicationOut schema.
def create_application(app_data: schemas.ApplicationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):  # The request body should be validated according to ApplicationCreate.
                                                           # telling fastapi that i need database session, get by executing get_db()
    new_app = models.Application(**app_data.model_dump(), user_id = current_user.id)  # Take the validated Pydantic data and use it to create a SQLAlchemy Application object.
    db.add(new_app)  # not permanenlty saving it to postgresql
    db.commit()    # now saving 
    db.refresh(new_app) # PostgreSQL may have generated val like-id, created_at
    return new_app

# db: Session = Depends(get_db) -->
# Incoming request -> FastAPI sees Depends(get_db) -> run get_db() ->create database session ->give session to endpoint ->db ->run endpoint ->request finished ->finally:db.close()
# Depends() is basically FastAPI's way of supplying things that your function needs, basically provide something your function needs.
  

# return applicaions of the user which is non archived
# Find Application rows -> keep only is_archived = False -> execute query -> return all matching rows
@app.get("/applications", response_model=list[schemas.ApplicationOut]) # When someone sends GET /applications, return a list of applications.
def list_applications(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    
    return db.query(models.Application).filter(models.Application.user_id == current_user.id, models.Application.is_archived == False).all()  



# the main idea is ==> url contains ID--> find applicatio  in DB--> if it exists
#                                                                    |       |
#                                                              404 <-NO     YES-> continue



@app.get("/applications/{app_id}", response_model=schemas.ApplicationOut)
def get_application(app_id:int, db:Session =  Depends(get_db), current_user: models.User = Depends(get_current_user)
):

# goes to application(table) class in models and matches if models.Application.id == app_id exists is yes then it rerturn 1st mstching obj 
    application = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == current_user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return application



@app.patch("/applications/{app_id}", response_model=schemas.ApplicationOut)
def update_application(app_id:int, updates:schemas.ApplicationUpdate, db:Session=Depends(get_db),current_user: models.User = Depends(get_current_user)):

    application = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == current_user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

# it only gives the fields the client actually sent not the ones that default to None, all none fields it excludes them 
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)
#       it gives which field is sent by the client along with its value
#  like--   setattr(application, "status", "Interview")


    db.commit()
    db.refresh(application)
    return application


#archive application(not delete)
@app.delete("/applications/{app_id}")
def delete_application(app_id:int, db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    application = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == current_user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application.is_archived = True   # we marked the row as archived
    db.commit()
    return {"detail":"Application archived"}



@app.post("/auth/register", response_model=schemas.Token) # Creates a new user with a hashed password and immediately gives them a JWT.
def register(user_data:schemas.UserCreate, db:Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_data.email).first()  # checking if the email exists or not
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = models.User(   # creating sqlalchemy obj
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)  # save new user 
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub":new_user.email})  #creatimg jwt token for registered user
    return {"access_token":token}



@app.post("/auth/login", response_model=schemas.Token)  # login to existing account, Checks the submitted email/password against PostgreSQL and gives the user a JWT if valid.
def login(form_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = create_access_token({"sub":user.email})  #creates jwt 
    return {"access_token":token}  # sends jwt to client


#######  more than 1 rounds for 1 application

@app.post("/applications/{app_id}/rounds", response_model=schemas.RoundOut)
def creae_round(app_id:int, round_data:schemas.RoundCreate, db:Session = Depends(get_db), current_user:models.User = Depends(get_current_user)):
    application = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == current_user.id).first()  # checks if this application exists AND does this application belong to logged in user ?

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    new_round = models.InterviewRound(**round_data.model_dump(), application_id=app_id) # updating the new round

    db.add(new_round)
    db.commit()
    db.refresh(new_round)
    return new_round


######## SPECIFIC INTERVIEW ROUNDS ENDPOINTS

@app.get("/applications/{app_id}/rounds", response_model=list[schemas.RoundOut])  # returning all interview rounds for that particular application, we use list coz the response contains multiple RoundOut obj
def list_rounds(app_id:int, db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    application = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == current_user.id).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return db.query(models.InterviewRound).filter(models.InterviewRound.application_id == app_id).all()


@app.get("/applications/{app_id}/rounds/{round_id}", response_model=schemas.RoundOut)
def get_round(app_id: int, round_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    application = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == current_user.id).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    round = db.query(models.InterviewRound).filter(models.InterviewRound.id == round_id, models.InterviewRound.application_id == app_id).first()

    if not round:
        raise HTTPException(status_code=404, detail="Round not found")

    return round


@app.patch("/applications/{app_id}/rounds/{round_id}", response_model=schemas.RoundOut)
def update_round(app_id: int, round_id: int, updates: schemas.RoundUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    application = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == current_user.id).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    round = db.query(models.InterviewRound).filter(models.InterviewRound.id == round_id, models.InterviewRound.application_id == app_id).first()

    if not round:
        raise HTTPException(status_code=404, detail="Round not found")

    update_data = updates.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(round, field, value)

    db.commit()
    db.refresh(round)

    return round


@app.delete("/applications/{app_id}/rounds/{round_id}")
def delete_round(app_id: int, round_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    application = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == current_user.id).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    round = db.query(models.InterviewRound).filter(models.InterviewRound.id == round_id, models.InterviewRound.application_id == app_id).first()

    if not round:
        raise HTTPException(status_code=404, detail="Round not found")

    db.delete(round)
    db.commit()

    return {"detail": "Round deleted"}



############ ANALYTICS ENGINE ENDPOINTS

def get_user_applications(db: Session, user_id: int):
    return db.query(models.Application).filter(
        models.Application.user_id == user_id,
        models.Application.is_archived == False
    ).all()

@app.get("/analytics/stats")
def analytics_stats(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    apps = get_user_applications(db, current_user.id)
    df = applications_to_df(apps)
    return compute_stats(df)

@app.get("/analytics/weekly")
def analytics_weekly(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    apps = get_user_applications(db, current_user.id)
    df = applications_to_df(apps)
    return compute_weekly_trend(df)

@app.get("/analytics/funnel")
def analytics_funnel(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    apps = get_user_applications(db, current_user.id)
    df = applications_to_df(apps)
    return compute_funnel(df)