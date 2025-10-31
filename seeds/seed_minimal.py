import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.core.db import session_scope
from app.models.agency import Agency
from app.models.rocket import Rocket
from app.models.launch import Launch
from datetime import datetime, timezone

def run():
    with session_scope() as s:
        if not s.get(Agency, "NASA"):
            s.add(Agency(id="NASA", name="NASA", country_code="US", type="Government"))

        if not s.get(Rocket, "FALCON9"):
            s.add(Rocket(id="FALCON9", name="Falcon 9", agency_id="NASA"))

        if not s.get(Launch, "TEST-001"):
            s.add(Launch(
                id="TEST-001",
                name="Demo Mission",
                window_start=datetime.now(timezone.utc),
                status="planned",
                rocket_id="FALCON9",
                agency_id="NASA",
                location="Florida"
            ))

if __name__ == "__main__":
    run()
