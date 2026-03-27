"""
Session persistence layer: File-based and Redis-compatible session storage.
Ensures sessions survive API restarts and support multiple instances.
"""

from __future__ import annotations

import json
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
import threading


class SessionStore:
    """Abstract session storage interface."""
    
    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError
    
    def set(self, session_id: str, data: Dict[str, Any], ttl_seconds: int = 3600) -> None:
        raise NotImplementedError
    
    def delete(self, session_id: str) -> None:
        raise NotImplementedError
    
    def cleanup_expired(self) -> int:
        """Remove expired sessions. Returns count deleted."""
        raise NotImplementedError


class FileSessionStore(SessionStore):
    """File-based persistent session storage."""
    
    def __init__(self, base_path: str = ".sessions"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self._lock = threading.RLock()
    
    def _get_session_path(self, session_id: str) -> Path:
        """Get path for a session file."""
        # Hash session_id for security
        safe_name = hashlib.sha256(session_id.encode()).hexdigest()[:16]
        return self.base_path / f"{safe_name}.json"
    
    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data."""
        with self._lock:
            path = self._get_session_path(session_id)
            if not path.exists():
                return None
            
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                
                # Check expiry
                if "expires_at" in data:
                    if datetime.fromisoformat(data["expires_at"]) < datetime.utcnow():
                        path.unlink()  # Delete expired session
                        return None
                
                return data.get("data")
            except (json.JSONDecodeError, IOError):
                return None
    
    def set(self, session_id: str, data: Dict[str, Any], ttl_seconds: int = 3600) -> None:
        """Store session data."""
        with self._lock:
            path = self._get_session_path(session_id)
            expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
            
            payload = {
                "session_id": session_id,
                "data": data,
                "expires_at": expires_at.isoformat(),
                "created_at": datetime.utcnow().isoformat(),
            }
            
            with open(path, "w") as f:
                json.dump(payload, f)
    
    def delete(self, session_id: str) -> None:
        """Delete session."""
        with self._lock:
            path = self._get_session_path(session_id)
            if path.exists():
                path.unlink()
    
    def cleanup_expired(self) -> int:
        """Remove expired sessions."""
        with self._lock:
            deleted = 0
            for session_file in self.base_path.glob("*.json"):
                try:
                    with open(session_file, "r") as f:
                        data = json.load(f)
                    
                    if "expires_at" in data:
                        if datetime.fromisoformat(data["expires_at"]) < datetime.utcnow():
                            session_file.unlink()
                            deleted += 1
                except (json.JSONDecodeError, IOError):
                    pass
            
            return deleted


class RedisSessionStore(SessionStore):
    """Redis-based session storage for distributed deployments."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        try:
            import redis
            self.redis = redis.from_url(redis_url)
            self.prefix = "session:"
        except ImportError:
            raise ImportError("redis-py is required for RedisSessionStore. Install with: pip install redis")
    
    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data."""
        try:
            data = self.redis.get(f"{self.prefix}{session_id}")
            if data:
                return json.loads(data)
            return None
        except Exception:
            return None
    
    def set(self, session_id: str, data: Dict[str, Any], ttl_seconds: int = 3600) -> None:
        """Store session data."""
        try:
            self.redis.setex(
                f"{self.prefix}{session_id}",
                ttl_seconds,
                json.dumps(data)
            )
        except Exception:
            pass
    
    def delete(self, session_id: str) -> None:
        """Delete session."""
        try:
            self.redis.delete(f"{self.prefix}{session_id}")
        except Exception:
            pass
    
    def cleanup_expired(self) -> int:
        """Redis handles expiry automatically. Returns 0."""
        return 0


def get_session_store(backend: str = "file", **kwargs) -> SessionStore:
    """Factory function to create session store."""
    if backend == "redis":
        return RedisSessionStore(**kwargs)
    elif backend == "file":
        return FileSessionStore(**kwargs)
    else:
        raise ValueError(f"Unknown session backend: {backend}")
