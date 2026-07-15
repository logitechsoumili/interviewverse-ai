import json
import logging
import time
from typing import Any, Dict, Optional

logger = logging.getLogger("interviewverse.ai")

class StructuredLogger:
    """A wrapper for standard logging that outputs messages and context as structured JSON.
    
    Ensures that sensitive information (prompts, responses, keys, history) is never logged.
    """
    
    SENSITIVE_KEYS = {
        "prompt",
        "system_prompt",
        "user_prompt",
        "response",
        "response_text",
        "text",
        "api_key",
        "gemini_api_key",
        "history",
        "contents",
        "messages",
    }

    @classmethod
    def _sanitize(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively sanitizes dictionary elements to strip sensitive keys."""
        sanitized = {}
        for k, v in data.items():
            if k.lower() in cls.SENSITIVE_KEYS:
                continue
            if isinstance(v, dict):
                sanitized[k] = cls._sanitize(v)
            else:
                sanitized[k] = v
        return sanitized

    @classmethod
    def _format(cls, level: str, message: str, extra: Optional[Dict[str, Any]] = None) -> str:
        """Formats the log message and metadata into a JSON string."""
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": level,
            "message": message,
        }
        if extra:
            sanitized_extra = cls._sanitize(extra)
            log_entry["context"] = sanitized_extra
        return json.dumps(log_entry)

    @classmethod
    def info(cls, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Logs structured message at INFO level."""
        if logger.isEnabledFor(logging.INFO):
            logger.info(cls._format("INFO", message, extra))

    @classmethod
    def warning(cls, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Logs structured message at WARNING level."""
        if logger.isEnabledFor(logging.WARNING):
            logger.warning(cls._format("WARNING", message, extra))

    @classmethod
    def error(cls, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Logs structured message at ERROR level."""
        if logger.isEnabledFor(logging.ERROR):
            logger.error(cls._format("ERROR", message, extra))
