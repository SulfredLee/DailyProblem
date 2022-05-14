import os
from python_mock_trying.observability.apm_agent import APMConfig

SERVICE_TAG = "MOCK_TRY_"

APM_CONFIG = APMConfig(
    os.getenv(
        f"{SERVICE_TAG}APM_URL",
        "https://e91a5507c0f84e598df1619a2862831e.apm.asia-southeast1.gcp.elastic-cloud.com:443",
    ),
    os.getenv(f"{SERVICE_TAG}APM_TOKEN", "lb7gMVHWfccEH38Y0X"),
    os.getenv(f"{SERVICE_TAG}APM_ENV", "dev"),
)

