from __future__ import annotations
from dataclasses import dataclass
from urllib.request import Request,urlopen
from urllib.parse import urlparse
from ec.research_v2 import SourceDocument
class HttpTextAcquisitionProvider:
    """Explicit-URL reference acquisition adapter. It is not a crawler and does not bypass access controls."""
    def __init__(self,urls,timeout=10,max_bytes=2_000_000,user_agent="EC-Research/0.8"):
        self.urls=tuple(urls); self.timeout=timeout; self.max_bytes=max_bytes; self.user_agent=user_agent
    def acquire(self,query):
        out=[]
        for uri in self.urls:
            req=Request(uri,headers={"User-Agent":self.user_agent})
            with urlopen(req,timeout=self.timeout) as r:
                body=r.read(self.max_bytes+1)
                if len(body)>self.max_bytes: raise ValueError("source exceeds configured acquisition limit")
                ctype=r.headers.get_content_type()
                if not (ctype.startswith("text/") or ctype in ("application/json","application/xml")): continue
                text=body.decode(r.headers.get_content_charset() or "utf-8",errors="replace")
                out.append(SourceDocument(uri,urlparse(uri).netloc,text,"web",.5))
        return tuple(out)
