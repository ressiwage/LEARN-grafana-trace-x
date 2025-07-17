from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
import datetime

sqlite_file_name = "main.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

class Entry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    success: int = Field(index=True)
    message: str | None = Field(default=None, index=True)
    timestamp: str = Field(default_factory=lambda: str(datetime.datetime.now().date()), index=True)

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

@app.get("/")
async def root(session: SessionDep):
    html_content = """
    <html>
        <head>
            <title>grafana</title>
        </head>
        <body>
            <iframe src="http://82.115.5.3:3000/d-solo/028e6dee-b868-48e7-bd31-ccf99abdca37/new-dashboard?orgId=1&from=1752722653113&to=1752744253113&timezone=browser&panelId=1&__feature.dashboardSceneSolo" width="450" height="200" frameborder="0"></iframe>
        </body>
    </html>
    """
    entry = Entry(
        timestamp=str(datetime.datetime.now().date()),
        success=1,
        message='visit'
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return HTMLResponse(content=html_content, status_code=200)