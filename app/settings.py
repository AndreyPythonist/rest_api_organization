import os


DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/postgres")
API_KEY: str = os.getenv("API_KEY", "TdaIFgO2HlmSVQ?3QoHOP139vrnYVc9=x!/YXSseyJwP-THfDbFmgBLVhzKtqHnZ")
