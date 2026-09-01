from google.ads.googleads.client import GoogleAdsClient

from app.core.config import settings


def get_google_ads_client() -> GoogleAdsClient:
	config = {
		"developer_token": settings.GOOGLE_ADS_DEVELOPER_TOKEN.strip(),
		"client_id": settings.GOOGLE_ADS_CLIENT_ID.strip(),
		"client_secret": settings.GOOGLE_ADS_CLIENT_SECRET.strip(),
		"refresh_token": settings.GOOGLE_ADS_REFRESH_TOKEN.strip(),
		"use_proto_plus": True,
	}
	login_customer_id = settings.GOOGLE_ADS_LOGIN_CUSTOMER_ID.strip().replace("-", "")
	if login_customer_id:
		config["login_customer_id"] = login_customer_id

	missing = [key for key, value in config.items() if key != "use_proto_plus" and not value]
	if missing:
		raise ValueError(f"Faltan credenciales de Google Ads: {', '.join(missing)}")

	return GoogleAdsClient.load_from_dict(config)
