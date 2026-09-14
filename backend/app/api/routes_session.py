from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import HTMLResponse
from backend.app.schemas.api_models import AnalyzeResponse
from backend.app.services.report_service import report_service
from backend.app.services.storage_service import storage_service

router = APIRouter(prefix="/v1", tags=["Session & Reports"])


@router.get("/session/{session_id}", response_model=AnalyzeResponse)
async def get_session(session_id: str) -> AnalyzeResponse:
    """Retrieves full analysis response and execution trace for a given session."""
    response = storage_service.get_session_response(session_id)
    if not response:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    return response


@router.get("/session/{session_id}/report")
async def get_session_report(
    session_id: str,
    format: str = Query(default="pdf", regex="^(pdf|json|html)$"),
):
    """Generates downloadable analysis report with complete data parity."""
    response = storage_service.get_session_response(session_id)
    if not response:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    if format == "json":
        return Response(
            content=report_service.render_json(response),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=satquery_report_{session_id}.json"},
        )

    # HTML / printable format
    html_content = report_service.render_html_report(response)
    return HTMLResponse(content=html_content)
