from elasticsearch import AsyncElasticsearch
from config import ELASTIC_HOST, ELASTIC_USER, ELASTIC_PASSWORD

es_client = AsyncElasticsearch(
    hosts=[ELASTIC_HOST],
    basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    verify_certs=False
)
