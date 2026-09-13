from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class AuthorizationDecision:
    allowed:bool; reason:str
class ScopeAuthorizer:
    def can_read(self,record_scope,*,tenant_id,user_id=None):
        if record_scope.kind.value in ("public","licensed","global-learned","industry"):return AuthorizationDecision(True,"shared governed scope")
        if record_scope.tenant_id and record_scope.tenant_id!=tenant_id:return AuthorizationDecision(False,"cross-tenant access denied")
        if record_scope.kind.value=="user" and record_scope.key!=user_id:return AuthorizationDecision(False,"user-private scope denied")
        return AuthorizationDecision(True,"scope permitted")
