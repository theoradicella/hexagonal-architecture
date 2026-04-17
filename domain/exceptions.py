class DomainError(Exception):
    """Base class for all domain exceptions."""


class CustomerNotFoundError(DomainError):
    """Raised when a customer cannot be found."""


class VendorNotFoundError(DomainError):
    """Raised when a vendor cannot be found."""


class OrderNotFoundError(DomainError):
    """Raised when an order cannot be found."""


class InvalidStatusTransitionError(DomainError):
    """Raised when an order status transition is not allowed."""


class UserAlreadyExistsError(DomainError):
    """Raised when attempting to register a user with an email that already exists."""


class InvalidCredentialsError(DomainError):
    """Raised when authentication credentials are invalid."""
