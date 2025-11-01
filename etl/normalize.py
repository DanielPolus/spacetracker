from datetime import datetime, timezone

def norm_launch(item: dict) -> dict:
    name = item.get("name") or "Unknown"
    ws = item.get("window_start") or item.get("net")
    window_start = None
    if ws:
        try:
            window_start = datetime.fromisoformat(ws.replace("Z", "+00:00"))
        except Exception:
            window_start = None

    status = (item.get("status") or {}).get("name")
    rocket_name = (item.get("rocket") or {}).get("configuration", {}).get("name")
    rocket_id = rocket_name.upper().replace(" ", "") if rocket_name else None
    agency_name = (item.get("launch_service_provider") or {}).get("name")
    agency_id = agency_name.upper().replace(" ", "") if agency_name else None
    loc = None
    pad = item.get("pad") or {}
    if pad.get("name"):
        loc = pad["name"]

    ext_id = item.get("id")
    launch_id = ext_id or f"{name}-{window_start or 'TBD'}"

    return {
        "id": launch_id[:64],
        "name": name[:255],
        "window_start": window_start,
        "status": (status or None),
        "rocket_id": rocket_id[:64] if rocket_id else None,
        "agency_id": agency_id[:64] if agency_id else None,
        "location": loc[:255] if loc else None,
        "_rocket_name": rocket_name,
        "_agency_name": agency_name,
    }
