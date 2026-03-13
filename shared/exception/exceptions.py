# exception/exceptions.py


class A2ARequestError(Exception):
    """Raised when an incoming A2A request is invalid."""


class KmeansError(Exception):
    """Raised when Kmeans fails."""


class KmeansNotFittedError(KmeansError):
    """Raised when CLUSTER_DATA is called before the model has been fitted."""


class A2ARouterError(A2ARequestError):
    """Raised when an A2A Router message is not supported."""