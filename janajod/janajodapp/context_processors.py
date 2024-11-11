
from .models import CommitteeMember

def committee_members_processor(request):
    committee_members = CommitteeMember.objects.all()
    return {'committee_members': committee_members}
