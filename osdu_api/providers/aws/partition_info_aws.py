class PartitionInfoAws():

    def __init__(self, id: str, tenant_id: str, resource_prefix: str, tenant_ssm_prefix: str):
        self.id = id
        self.tenant_id = tenant_id
        self.resource_prefix = resource_prefix
        self.tenant_ssm_prefix = tenant_ssm_prefix
