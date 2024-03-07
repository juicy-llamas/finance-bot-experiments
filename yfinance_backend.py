
import yfinance as yf
import pandas as pd

from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

rq = CachedLimiterSession(
	limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
	bucket_class=MemoryQueueBucket,
	backend=SQLiteCache("yfinance.cache"),
)

tickers = [ "GOOG", "AMZN", "msft", "tsla", "aapl", "baba", "snap", "pins", "roku", "docu", "crwd", "zm", "spot", "fvrr" ]

df = yf.download( tickers, session = rq )


df.to_excell( "output.excel" )
