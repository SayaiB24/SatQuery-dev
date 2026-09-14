import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from fastapi import UploadFile
from backend.app.config import SESSIONS_DIR
from backend.app.schemas.api_models import AnalyzeResponse


class StorageService:
    def __init__(self):
        self._session_cache: Dict[str, AnalyzeResponse] = {}

    def get_session_dir(self, session_id: str) -> Path:
        session_dir = SESSIONS_DIR / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        (session_dir / "inputs").mkdir(exist_ok=True)
        (session_dir / "evidence").mkdir(exist_ok=True)
        return session_dir

    async def save_uploaded_files(
        self, session_id: str, files: List[UploadFile]
    ) -> List[Dict[str, str]]:
        session_dir = self.get_session_dir(session_id)
        inputs_dir = session_dir / "inputs"
        saved_files = []

        for idx, file in enumerate(files):
            ext = file.filename.split(".")[-1] if "." in file.filename else "bin"
            file_path = inputs_dir / f"image_{idx + 1}_{file.filename}"

            # Calculate content hash while saving
            hasher = hashlib.sha256()
            with open(file_path, "wb") as f:
                content = await file.read()
                hasher.update(content)
                f.write(content)

            saved_files.append({
                "filename": file.filename,
                "path": str(file_path),
                "content_hash": hasher.hexdigest(),
                "size_bytes": len(content),
            })

        return saved_files

    def store_session_response(self, session_id: str, response: AnalyzeResponse) -> None:
        self._session_cache[session_id] = response
        # Also persist to disk for durability
        session_dir = self.get_session_dir(session_id)
        dump_path = session_dir / "response.json"
        with open(dump_path, "w", encoding="utf-8") as f:
            f.write(response.model_dump_json(by_alias=True, indent=2))

    def get_session_response(self, session_id: str) -> Optional[AnalyzeResponse]:
        if session_id in self._session_cache:
            return self._session_cache[session_id]

        dump_path = SESSIONS_DIR / session_id / "response.json"
        if dump_path.exists():
            with open(dump_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                res = AnalyzeResponse.model_validate(data)
                self._session_cache[session_id] = res
                return res
        return None


storage_service = StorageService()
