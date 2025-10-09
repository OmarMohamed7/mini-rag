from enum import Enum


class VectorDBEnums(Enum):
    PINECONE = "PINECONE"
    QDRANT = "QDRANT"
    ELASTICSEARCH = "ELASTICSEARCH"


class DistanceMethodsEnums(Enum):
    COSINE = "Cosine"
    DOT = "Dot"
