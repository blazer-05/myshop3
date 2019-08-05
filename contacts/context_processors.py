from contacts.models import PrivacyPolicy


def privacy_policy(request):
    privacy_policy = PrivacyPolicy.objects.filter(is_active=True).last()
    return {'privacy_policy': privacy_policy}