from .models import Source

def run(output_file_path):
    data = Source.objects.filter(qualified_status='已通過')

    output_str_list = list()
    for item in data:
        if item.userprofile.phone == '':
            continue

        source_user_name = item.userprofile.name
        source_user_phone = item.userprofile.phone
        source_modified_address = item.modified_address
        source_description = item.description
        output_str_item = "%s\t%s\t%s\t%s" % \
            (source_user_name, source_user_phone, source_modified_address, source_description)
        output_str_list.append(output_str_item)

    output_str = '\n'.join(output_str_list)
    with open(output_file_path, 'w') as myfile:
        myfile.write(output_str)
