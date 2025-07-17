from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

sqlite_file_name = "main.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

@app.get("/")
async def root():
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
    return HTMLResponse(content=html_content, status_code=200)