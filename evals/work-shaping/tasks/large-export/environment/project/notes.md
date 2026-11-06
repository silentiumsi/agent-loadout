support_export is an internal handler and is not exposed to customers. Auth middleware supplies request.tenant_id. Store enforces the tenant filter passed by callers. There are no background workers.
