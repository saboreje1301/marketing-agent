"""
API endpoint para optimización de campañas enfocada en conversiones.
Sin dependencia de base de datos.
"""

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from google.ads.googleads.errors import GoogleAdsException

from app.ai.conversion_optimizer_agent import optimize_for_conversions

router = APIRouter(
    prefix="/api/v1",
    tags=["Optimization"],
)


class OptimizeRequest(BaseModel):
    """Request para optimizar una campaña."""
    campaign_id: str
    budget: float


class OptimizeResponse(BaseModel):
    """Response de optimización."""
    campaign_id: str
    status: str
    conversions_before: int
    conversions_projected: float
    budget_assigned: float
    budget_action: str
    optimizations: list
    summary: str


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_campaign(request: OptimizeRequest):
    """
    Optimiza una campaña de Google Ads para maximizar conversiones.
    
    - **campaign_id**: ID de la campaña en Google Ads
    - **budget**: Presupuesto diario a asignar
    
    Retorna análisis detallado y cambios realizados automáticamente.
    """
    try:
        if request.budget <= 0:
            raise HTTPException(status_code=400, detail="El presupuesto debe ser mayor a 0")
        
        result = await optimize_for_conversions(
            campaign_id=request.campaign_id,
            budget=request.budget,
        )
        
        return OptimizeResponse(**result)
    
    except HTTPException:
        raise
    except (GoogleAdsException, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al optimizar campaña: {str(error)}"
        ) from error
