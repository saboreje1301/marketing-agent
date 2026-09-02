"""
Agente de optimización de conversiones.
Obtiene métricas de Google Ads y optimiza automáticamente la campaña
para maximizar conversiones dentro del presupuesto asignado.
"""

from app.infrastructure.google_ads.service import (
    get_campaign_metrics,
    get_ad_group_metrics,
    update_ad_group_bid,
    update_campaign_budget,
)


async def optimize_for_conversions(
    campaign_id: str,
    budget: float,
    min_conversion_rate: float = 0.01,
) -> dict:
    """
    Optimiza una campaña para maximizar conversiones.
    
    Args:
        campaign_id: ID de la campaña en Google Ads
        budget: Presupuesto diario asignado
        min_conversion_rate: Tasa de conversión mínima aceptable
    
    Returns:
        dict con resultados de optimización
    """
    
    # 1. Obtener métricas de la campaña
    campaign_metrics = get_campaign_metrics(campaign_id)
    
    # 2. Obtener métricas por ad group
    ad_groups = get_ad_group_metrics(campaign_id)
    
    # 3. Calcular eficiencia de conversión por ad group
    optimizations = []
    total_conversions_before = campaign_metrics.get("conversions", 0)
    
    for ad_group in ad_groups:
        ad_group_id = ad_group["id"]
        conversions = ad_group.get("conversions", 0)
        clicks = ad_group.get("clicks", 0)
        cost = ad_group.get("cost", 0)
        
        # Calcular conversion rate
        conv_rate = conversions / clicks if clicks > 0 else 0
        
        # Calcular CPA (cost per acquisition)
        cpa = cost / conversions if conversions > 0 else float("inf")
        
        # Estrategia de optimización
        if conv_rate >= min_conversion_rate:
            # Ad group eficiente: aumentar bid para obtener más clics
            new_bid = ad_group.get("avg_cpc", 1.0) * 1.15  # +15% bid
            action = "increase_bid"
        elif conversions > 0:
            # Ad group con algunas conversiones: mantener con pequeño ajuste
            new_bid = ad_group.get("avg_cpc", 1.0) * 1.05  # +5% bid
            action = "maintain_bid"
        else:
            # Ad group sin conversiones: reducir bid
            new_bid = ad_group.get("avg_cpc", 1.0) * 0.85  # -15% bid
            action = "reduce_bid"
        
        # Aplicar cambio
        update_ad_group_bid(campaign_id, ad_group_id, new_bid)
        
        optimizations.append({
            "ad_group_id": ad_group_id,
            "ad_group_name": ad_group.get("name"),
            "conversions": conversions,
            "conversion_rate": round(conv_rate * 100, 2),
            "cpa": round(cpa, 2) if cpa != float("inf") else "N/A",
            "old_bid": round(ad_group.get("avg_cpc", 0), 2),
            "new_bid": round(new_bid, 2),
            "action": action,
        })
    
    # 4. Ajustar presupuesto de campaña
    if campaign_metrics.get("budget_spent", 0) < budget:
        # Aún hay presupuesto disponible
        update_campaign_budget(campaign_id, budget)
        budget_action = "increased_to_target"
    else:
        budget_action = "budget_consumed"
    
    return {
        "campaign_id": campaign_id,
        "status": "optimized",
        "conversions_before": total_conversions_before,
        "conversions_projected": total_conversions_before * 1.2,  # Proyección conservadora
        "budget_assigned": budget,
        "budget_action": budget_action,
        "optimizations": optimizations,
        "summary": f"Optimización completada: {len(optimizations)} ad groups ajustados",
    }
