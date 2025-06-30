from prefect.blocks.core import Block

class EnterpriseDataLakeWindows(Block):
    environment: str
    source: str
    path: str
    object_name: str
    account_lookup: dict

    account_lookup = {
        'prd': 'stdatalakerawdprod001'
    }

    def upload(self):
        init = f'''
        use schema PREFECT_POC_{self.environment}.{self.source}
        '''

        stage = f'''
            create stage if not exists {self.path.replace('/', '_')}
            url = 'azure://{self.account_lookup[self.environment]}.blob.core.windows.net/{self.path}/'
            credentials=(azure_sas_token='')
        '''

        copy_command = f'''
            copy into {self.object_name}
            from @object_name {self.object_name}
        '''

EnterpriseDataLakeWindows.register_type_and_schema()