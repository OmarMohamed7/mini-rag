from enum import Enum


class VectorDBEnums(Enum):
    PINECONE = "PINECONE"
    QDRANT = "QDRANT"
    ELASTICSEARCH = "ELASTICSEARCH"


class DistanceMethodsEnums(Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    MANHATTAN = "manhattan"
    CHEBYSHEV = "chebyshev"
    MINKOWSKI = "minkowski"
    DOT = "dot"
    HAMMING = "hamming"
    JACCARD = "jaccard"
    TANIMOTO = "tanimoto"
