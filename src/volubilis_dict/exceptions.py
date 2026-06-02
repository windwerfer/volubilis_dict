"""Custom exceptions for the dictionary processor."""


class DictionaryProcessorError(Exception):
    """Base exception for dictionary processing errors."""
    pass


class ConfigurationError(DictionaryProcessorError):
    """Raised when configuration is invalid."""
    pass


class FileProcessingError(DictionaryProcessorError):
    """Raised when file processing fails."""
    pass


class ExcelProcessingError(DictionaryProcessorError):
    """Raised when Excel file processing fails."""
    pass


class ValidationError(DictionaryProcessorError):
    """Raised when data validation fails."""
    pass