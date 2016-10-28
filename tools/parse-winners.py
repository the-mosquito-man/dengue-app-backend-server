import json
from breeding.models import Source
from users.models import UserProfile

userprofile_filter = UserProfile.objects.filter(is_signup=True)
winner_list = list()
for userprofile in userprofile_filter:
    source_count = Source.objects.filter(userprofile=userprofile,
                                         qualified_status='已通過').count()
    if source_count < 3:
        continue

    winner_dict = {'uid': str(userprofile.user_uuid),
                   'name': userprofile.name,
                   'phone': userprofile.phone}
    winner_list.append(winner_dict)

with open('winners.json', 'w') as myfile:
    json.dump(winner_list, myfile, ensure_ascii=False, indent=4)
