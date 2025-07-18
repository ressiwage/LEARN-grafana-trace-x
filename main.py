from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
import datetime

sqlite_file_name = "/home/grafana/main.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

grafana_ts = lambda dt: int(dt.timestamp()*1000)
week = datetime.timedelta(weeks=1)

class Maindata(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    success: int = Field(index=True)
    message: str | None = Field(default=None, index=True)
    timestamp: str = Field(default_factory=lambda: str(datetime.datetime.now().isoformat()), index=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post('/add_entry')
def add_entry(
   session: SessionDep,
    success: int = Query(..., description="Message text"),
    message: str = Query(..., description="Message text")
) -> Maindata:
    """
    Add a new entry to the database.
    """
    if success < 0 or success > 1:
        raise HTTPException(status_code=400, detail="Success must be 0 or 1")
    entry = Maindata(success=success, message=message)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return {"id": entry.id, "success": entry.success, "message": entry.message}

@app.get("/")
async def root(session: SessionDep):
    from_ = grafana_ts(datetime.datetime.now() - week)
    to = grafana_ts(datetime.datetime.now())
    html_content = f"""
    <html>
        <head>
            <title>grafana</title>
        </head>
        <body>
            <span><a href="http://82.115.5.3:3000/">admin</a></span>
            <span><a href="http://82.115.5.3:8000/docs">docs</a></span>
            <hr>
            <h1>grafana analytics</h1>
            <h3>errors and successes</h3>
            <iframe src="http://82.115.5.3:3000/d-solo/028e6dee-b868-48e7-bd31-ccf99abdca37/new-dashboard?orgId=1&from={from_}&to={to}&timezone=browser&panelId=2&__feature.dashboardSceneSolo" width="100%" height="30%" frameborder="0"></iframe>
            <hr>
            <h3>visits</h3>
            <iframe src="http://82.115.5.3:3000/d-solo/028e6dee-b868-48e7-bd31-ccf99abdca37/new-dashboard?orgId=1&from={from_}&to={to}&timezone=browser&panelId=1&__feature.dashboardSceneSolo" width="100%" height="30%" frameborder="0"></iframe>
            <hr>
            <h3>logs</h3>
            <iframe src="http://82.115.5.3:3000/d-solo/028e6dee-b868-48e7-bd31-ccf99abdca37/new-dashboard?orgId=1&from={from_}&to={to}&timezone=browser&panelId=4&__feature.dashboardSceneSolo" width="100%" height="30%" frameborder="0"></iframe>
        </body>
    </html>
    """
    entry = Maindata(
        timestamp=str(datetime.datetime.now().isoformat()),
        success=2,
        message='visit'
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return HTMLResponse(content=html_content, status_code=200)