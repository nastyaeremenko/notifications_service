from worker.constants import ProviderType
from worker.provider.provider import EmailProvider, SmsProvider, MessangerProvider


class ProviderFactory:

    PROVIDER_MAPPER = {
        ProviderType.email: EmailProvider,
        ProviderType.sms: SmsProvider,
        ProviderType.messanger: MessangerProvider
    }

    def __init__(self, provider_type: ProviderType):
        self.provider_type = provider_type

    def get_provider(self):
        return self.PROVIDER_MAPPER[self.provider_type]()
