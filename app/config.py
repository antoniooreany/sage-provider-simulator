import os


class Config:
    PROVIDER_API_KEY = os.environ.get("PROVIDER_API_KEY", "test-api-key-not-a-secret")
