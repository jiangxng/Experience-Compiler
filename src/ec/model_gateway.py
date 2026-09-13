from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol,Mapping
@dataclass(frozen=True,slots=True)
class ModelRequest:
    task:str; system_context:str; user_context:str; max_output_tokens:int=4096
@dataclass(frozen=True,slots=True)
class ModelResponse:
    model_id:str; text:str; usage:Mapping[str,int]; finish_reason:str
class ModelProvider(Protocol):
    @property
    def model_id(self)->str: ...
    def complete(self,request:ModelRequest)->ModelResponse: ...
class DeterministicReferenceModel:
    model_id="reference/deterministic-v1"
    def complete(self,request):
        return ModelResponse(self.model_id,f"[REFERENCE] task={request.task}; context accepted",{"input_tokens":len(request.user_context)//4,"output_tokens":12},"stop")
class ModelGateway:
    def __init__(self,providers): self.providers={p.model_id:p for p in providers}
    def complete(self,model_id,request): return self.providers[model_id].complete(request)
