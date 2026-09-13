from __future__ import annotations
import json
from urllib.request import Request,urlopen
from ec.model_gateway import ModelRequest,ModelResponse
class OpenAICompatibleProvider:
    """Provider-neutral adapter for APIs implementing the common chat-completions shape."""
    def __init__(self,*,model_id,base_url,api_key,timeout=60):
        self._model_id=model_id; self.base_url=base_url.rstrip("/"); self.api_key=api_key; self.timeout=timeout
    @property
    def model_id(self): return self._model_id
    def complete(self,r:ModelRequest):
        payload=json.dumps({"model":self.model_id,"messages":[{"role":"system","content":r.system_context},{"role":"user","content":r.user_context}],"max_tokens":r.max_output_tokens}).encode()
        req=Request(self.base_url+"/chat/completions",data=payload,headers={"Content-Type":"application/json","Authorization":"Bearer "+self.api_key})
        with urlopen(req,timeout=self.timeout) as resp: data=json.loads(resp.read())
        usage=data.get("usage",{})
        return ModelResponse(self.model_id,data["choices"][0]["message"]["content"],
          {"input_tokens":usage.get("prompt_tokens",0),"output_tokens":usage.get("completion_tokens",0)},data["choices"][0].get("finish_reason","unknown"))
