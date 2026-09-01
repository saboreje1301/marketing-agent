from app.ai.analytics_agent import analyze_campaign
from app.ai.seo_agent import audit_url_with_ai
from app.schemas.analytics import CampaignMetricsRequest
from app.schemas.coordinator import CoordinatorReportRequest, CoordinatorReportResponse
from app.schemas.seo import SeoAuditRequest


async def create_report(request: CoordinatorReportRequest) -> CoordinatorReportResponse:
    seo = await audit_url_with_ai(SeoAuditRequest(url=request.url, keyword=request.keyword))
    analytics = analyze_campaign(
        CampaignMetricsRequest(
            campaign_id=request.campaign_id,
            date_range=request.date_range,
        )
    )
    if analytics.impressions == 0:
        evaluation_phase = "data_collection"
        change_policy = "No hagas cambios de rendimiento todavía; verifica estado, aprobación y segmentación."
        safe_changes = [
            "Corregir URLs rotas o anuncios rechazados.",
            "Verificar conversiones y etiquetas de medición.",
        ]
    elif analytics.impressions < 100 or analytics.clicks < 10:
        evaluation_phase = "learning"
        change_policy = "Haz solo cambios urgentes y espera más datos antes de optimizar."
        safe_changes = [
            "Corregir anuncios rechazados o problemas de medición.",
            "Añadir keywords claramente relevantes sin cambiar el presupuesto.",
        ]
    else:
        evaluation_phase = "optimization"
        change_policy = "Optimiza una variable a la vez y revisa el resultado después de varios días."
        safe_changes = [
            "Pausar keywords con bajo rendimiento tras revisar suficientes datos.",
            "Ajustar el presupuesto gradualmente, preferiblemente no más de 15-20%.",
            "Probar nuevas variantes de anuncios manteniendo una versión de control.",
        ]
    next_actions = list(seo.recommendations)
    if analytics.impressions == 0:
        next_actions.append("La campaña no tiene impresiones en el período seleccionado.")
    elif analytics.clicks == 0:
        next_actions.append("Revisa keywords y anuncios: hay impresiones, pero ningún clic.")
    return CoordinatorReportResponse(
        seo=seo,
        analytics=analytics,
        evaluation_phase=evaluation_phase,
        change_policy=change_policy,
        safe_changes=safe_changes,
        next_actions=next_actions,
    )