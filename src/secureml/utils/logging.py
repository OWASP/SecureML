"""Structured logging for SecureML with security event tracking"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import json


class SecureMLLogger:
    """
    Structured logger with security event tracking

    Provides comprehensive logging with special handling for:
    - Security events (signing, verification)
    - Audit trails
    - Performance metrics
    - Error tracking
    """

    def __init__(
        self,
        name: str = "secureml",
        level: int = logging.INFO,
        log_file: Optional[Path] = None,
        enable_audit: bool = False,
    ):
        """
        Initialize SecureML logger

        Args:
            name: Logger name
            level: Logging level
            log_file: Optional file path for logs
            enable_audit: Enable audit trail logging
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.enable_audit = enable_audit

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Audit log file
        if enable_audit:
            self.audit_log = log_file.parent / "audit.log" if log_file else Path("audit.log")

    def security_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        level: str = "INFO"
    ) -> None:
        """
        Log a security event

        Args:
            event_type: Type of security event (signing, verification, etc.)
            details: Event details
            level: Log level
        """
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details,
        }

        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(f"SECURITY EVENT: {event_type} - {json.dumps(details)}")

        if self.enable_audit:
            self._write_audit_log(event_data)

    def _write_audit_log(self, event_data: Dict[str, Any]) -> None:
        """Write to audit log file"""
        with open(self.audit_log, "a") as f:
            f.write(json.dumps(event_data) + "\n")

    def info(self, msg: str, **kwargs: Any) -> None:
        """Log info message"""
        self.logger.info(msg, **kwargs)

    def warning(self, msg: str, **kwargs: Any) -> None:
        """Log warning message"""
        self.logger.warning(msg, **kwargs)

    def error(self, msg: str, **kwargs: Any) -> None:
        """Log error message"""
        self.logger.error(msg, **kwargs)

    def debug(self, msg: str, **kwargs: Any) -> None:
        """Log debug message"""
        self.logger.debug(msg, **kwargs)


# Global logger instance
_logger: Optional[SecureMLLogger] = None


def get_logger(
    name: str = "secureml",
    level: int = logging.INFO,
    **kwargs: Any
) -> SecureMLLogger:
    """Get or create global logger instance"""
    global _logger
    if _logger is None:
        _logger = SecureMLLogger(name=name, level=level, **kwargs)
    return _logger
