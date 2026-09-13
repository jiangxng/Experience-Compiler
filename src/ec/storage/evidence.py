from __future__ import annotations
import hashlib, json
from pathlib import Path
class FileEvidenceArchive:
    """Content-addressed immutable evidence archive for development/reference deployments."""
    def __init__(self, root):
        self.root=Path(root); (self.root/"objects").mkdir(parents=True,exist_ok=True)
    def put(self,content:bytes,*,media_type:str,source_uri:str)->str:
        digest=hashlib.sha256(content).hexdigest(); p=self.root/"objects"/digest[:2]/digest
        p.parent.mkdir(parents=True,exist_ok=True)
        if not p.exists(): p.write_bytes(content)
        meta=p.with_suffix(".json")
        if not meta.exists(): meta.write_text(json.dumps({"sha256":digest,"media_type":media_type,"source_uri":source_uri},indent=2))
        return digest
    def get(self,evidence_id:str)->bytes:
        return (self.root/"objects"/evidence_id[:2]/evidence_id).read_bytes()
