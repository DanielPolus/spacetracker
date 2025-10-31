import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.core.db import SessionLocal
from app.models.launch import Launch

with SessionLocal() as s:
    launches = s.query(Launch).order_by(Launch.window_start.desc()).limit(3).all()
    print(f"Found {len(launches)} launches")
    for l in launches:
        print(l.id, l.name, l.window_start, l.status)
