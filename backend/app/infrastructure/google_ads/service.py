from decimal import Decimal

from app.core.config import settings
from app.infrastructure.google_ads.client import get_google_ads_client


def create_campaign(name: str, status: str, budget: Decimal) -> dict[str, str | Decimal]:
	customer_id = settings.GOOGLE_ADS_CUSTOMER_ID.strip().replace("-", "")
	if not customer_id or not customer_id.isdigit():
		raise ValueError("GOOGLE_ADS_CUSTOMER_ID debe ser numérico y no contener guiones")
	if budget <= 0:
		raise ValueError("El presupuesto debe ser mayor que cero")

	client = get_google_ads_client()
	budget_service = client.get_service("CampaignBudgetService")
	budget_operation = client.get_type("CampaignBudgetOperation")
	campaign_budget = budget_operation.create
	campaign_budget.name = f"Presupuesto - {name}"
	campaign_budget.amount_micros = int(budget * Decimal("1000000"))
	campaign_budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD

	budget_response = budget_service.mutate_campaign_budgets(
		customer_id=customer_id,
		operations=[budget_operation],
	)

	campaign_operation = client.get_type("CampaignOperation")
	campaign = campaign_operation.create
	campaign.name = name
	campaign.status = getattr(client.enums.CampaignStatusEnum, status.upper())
	campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
	campaign.campaign_budget = budget_response.results[0].resource_name
	campaign.contains_eu_political_advertising = (
		client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
	)
	campaign.manual_cpc.enhanced_cpc_enabled = False
	campaign.network_settings.target_google_search = True
	campaign.network_settings.target_search_network = True

	campaign_service = client.get_service("CampaignService")
	campaign_response = campaign_service.mutate_campaigns(
		customer_id=customer_id,
		operations=[campaign_operation],
	)
	campaign_id = campaign_response.results[0].resource_name.rsplit("/", 1)[-1]

	return {
		"id": campaign_id,
		"name": name,
		"status": status.upper(),
		"budget": budget,
	}


def list_campaigns() -> list[dict[str, str]]:
	customer_id = settings.GOOGLE_ADS_CUSTOMER_ID.strip().replace("-", "")
	if not customer_id or not customer_id.isdigit():
		raise ValueError("GOOGLE_ADS_CUSTOMER_ID debe ser numérico y no contener guiones")

	query = """
		SELECT
		  campaign.id,
		  campaign.name,
		  campaign.status
		FROM campaign
		ORDER BY campaign.id
	"""

	google_ads_service = get_google_ads_client().get_service("GoogleAdsService")
	response = google_ads_service.search(customer_id=customer_id, query=query)

	return [
		{
			"id": str(row.campaign.id),
			"name": row.campaign.name,
			"status": row.campaign.status.name,
		}
		for row in response
	]


def get_campaign_metrics(campaign_id: str, date_range: str) -> dict[str, str | int | Decimal]:
	customer_id = settings.GOOGLE_ADS_CUSTOMER_ID.strip().replace("-", "")
	if not customer_id or not customer_id.isdigit():
		raise ValueError("GOOGLE_ADS_CUSTOMER_ID debe ser numérico y no contener guiones")
	if not campaign_id.isdigit():
		raise ValueError("El ID de campaña de Google Ads debe ser numérico")

	allowed_ranges = {
		"TODAY",
		"YESTERDAY",
		"LAST_7_DAYS",
		"LAST_14_DAYS",
		"LAST_30_DAYS",
		"THIS_MONTH",
		"LAST_MONTH",
	}
	if date_range not in allowed_ranges:
		raise ValueError("date_range no es válido para Google Ads")

	query = f"""
		SELECT
		  campaign.id,
		  metrics.impressions,
		  metrics.clicks,
		  metrics.ctr,
		  metrics.cost_micros,
		  metrics.conversions,
		  metrics.average_cpc
		FROM campaign
		WHERE campaign.id = {campaign_id}
		  AND segments.date DURING {date_range}
	"""
	response = get_google_ads_client().get_service("GoogleAdsService").search(
		customer_id=customer_id,
		query=query,
	)

	impressions = clicks = 0
	cost_micros = conversions = average_cpc_micros = 0
	ctr = Decimal("0")
	for row in response:
		impressions += row.metrics.impressions
		clicks += row.metrics.clicks
		cost_micros += row.metrics.cost_micros
		conversions += row.metrics.conversions
		average_cpc_micros += row.metrics.average_cpc
		ctr = row.metrics.ctr

	return {
		"campaign_id": campaign_id,
		"date_range": date_range,
		"impressions": impressions,
		"clicks": clicks,
		"ctr": Decimal(str(ctr)),
		"cost": Decimal(cost_micros) / Decimal("1000000"),
		"conversions": Decimal(str(conversions)),
		"average_cpc": Decimal(average_cpc_micros) / Decimal("1000000"),
	}


def create_ad_group(campaign_id: str, name: str, cpc_bid: Decimal) -> dict[str, str]:
	customer_id = settings.GOOGLE_ADS_CUSTOMER_ID.strip().replace("-", "")
	if not customer_id or not customer_id.isdigit():
		raise ValueError("GOOGLE_ADS_CUSTOMER_ID debe ser numérico y no contener guiones")
	if not campaign_id.isdigit():
		raise ValueError("El ID de campaña de Google Ads debe ser numérico")
	if cpc_bid <= 0:
		raise ValueError("La puja CPC debe ser mayor que cero")

	client = get_google_ads_client()
	operation = client.get_type("AdGroupOperation")
	ad_group = operation.create
	ad_group.name = name
	ad_group.campaign = client.get_service("GoogleAdsService").campaign_path(
		customer_id, campaign_id
	)
	ad_group.status = client.enums.AdGroupStatusEnum.PAUSED
	ad_group.type = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
	ad_group.cpc_bid_micros = int(cpc_bid * Decimal("1000000"))

	response = client.get_service("AdGroupService").mutate_ad_groups(
		customer_id=customer_id,
		operations=[operation],
	)
	ad_group_id = response.results[0].resource_name.rsplit("/", 1)[-1]

	return {
		"id": ad_group_id,
		"name": name,
		"status": "PAUSED",
		"campaign_id": campaign_id,
	}


def list_ad_groups(campaign_id: str) -> list[dict[str, str]]:
	customer_id = settings.GOOGLE_ADS_CUSTOMER_ID.strip().replace("-", "")
	if not customer_id or not customer_id.isdigit():
		raise ValueError("GOOGLE_ADS_CUSTOMER_ID debe ser numérico y no contener guiones")
	if not campaign_id.isdigit():
		raise ValueError("El ID de campaña de Google Ads debe ser numérico")

	query = f"""
		SELECT
		  campaign.id,
		  ad_group.id,
		  ad_group.name,
		  ad_group.status
		FROM ad_group
		WHERE campaign.id = {campaign_id}
		ORDER BY ad_group.id
	"""
	response = get_google_ads_client().get_service("GoogleAdsService").search(
		customer_id=customer_id,
		query=query,
	)

	return [
		{
			"id": str(row.ad_group.id),
			"name": row.ad_group.name,
			"status": row.ad_group.status.name,
			"campaign_id": str(row.campaign.id),
		}
		for row in response
	]


def create_keyword(ad_group_id: str, text: str, match_type: str) -> dict[str, str]:
	customer_id = settings.GOOGLE_ADS_CUSTOMER_ID.strip().replace("-", "")
	if not customer_id or not customer_id.isdigit():
		raise ValueError("GOOGLE_ADS_CUSTOMER_ID debe ser numérico y no contener guiones")
	if not ad_group_id.isdigit():
		raise ValueError("El ID del grupo de anuncios debe ser numérico")
	if not text.strip():
		raise ValueError("La palabra clave no puede estar vacía")

	match_type_name = match_type.upper()
	match_types = {
		"BROAD": "BROAD",
		"PHRASE": "PHRASE",
		"EXACT": "EXACT",
	}
	if match_type_name not in match_types:
		raise ValueError("match_type debe ser BROAD, PHRASE o EXACT")

	client = get_google_ads_client()
	operation = client.get_type("AdGroupCriterionOperation")
	criterion = operation.create
	criterion.ad_group = client.get_service("GoogleAdsService").ad_group_path(
		customer_id, ad_group_id
	)
	criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
	criterion.keyword.text = text.strip()
	criterion.keyword.match_type = getattr(
		client.enums.KeywordMatchTypeEnum, match_types[match_type_name]
	)

	response = client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(
		customer_id=customer_id,
		operations=[operation],
	)
	keyword_id = response.results[0].resource_name.rsplit("/", 1)[-1]

	return {
		"id": keyword_id,
		"text": text.strip(),
		"match_type": match_type_name,
		"status": "ENABLED",
		"ad_group_id": ad_group_id,
	}


def create_search_ad(
	ad_group_id: str,
	final_url: str,
	headlines: list[str],
	descriptions: list[str],
) -> dict[str, str]:
	customer_id = settings.GOOGLE_ADS_CUSTOMER_ID.strip().replace("-", "")
	if not customer_id or not customer_id.isdigit():
		raise ValueError("GOOGLE_ADS_CUSTOMER_ID debe ser numérico y no contener guiones")
	if not ad_group_id.isdigit():
		raise ValueError("El ID del grupo de anuncios debe ser numérico")
	if not final_url.strip():
		raise ValueError("La URL final no puede estar vacía")
	if len(headlines) < 3 or len(descriptions) < 2:
		raise ValueError("El anuncio necesita al menos 3 títulos y 2 descripciones")

	client = get_google_ads_client()
	operation = client.get_type("AdGroupAdOperation")
	ad_group_ad = operation.create
	ad_group_ad.ad_group = client.get_service("GoogleAdsService").ad_group_path(
		customer_id, ad_group_id
	)
	ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
	responsive_search_ad = ad_group_ad.ad.responsive_search_ad
	responsive_search_ad.path1 = "marketing"
	responsive_search_ad.path2 = "digital"
	for headline in headlines:
		asset = client.get_type("AdTextAsset")
		asset.text = headline
		responsive_search_ad.headlines.append(asset)
	for description in descriptions:
		asset = client.get_type("AdTextAsset")
		asset.text = description
		responsive_search_ad.descriptions.append(asset)
	ad_group_ad.ad.final_urls.append(final_url.strip())

	response = client.get_service("AdGroupAdService").mutate_ad_group_ads(
		customer_id=customer_id,
		operations=[operation],
	)
	resource_name = response.results[0].resource_name
	ad_id = resource_name.rsplit("/", 1)[-1]

	return {
		"id": ad_id,
		"ad_group_id": ad_group_id,
		"status": "PAUSED",
		"final_url": final_url.strip(),
	}
