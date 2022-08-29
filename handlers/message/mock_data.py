from urllib.parse import urlencode

# ADD contact(s)
add_number = urlencode(
    {"Body": "ADD +19086162014"}
)
add_number_name = urlencode(
    {"Body": "ADD 9086162014 @Mitch"}
)
add numbers = urlencode(
    {"Body": "ADD 9086162014,8881119999"}
)
add_combos = urlencode(
    {"Body": "ADD 9086162013,8881119999 @John"}
)

# ADD group(s)
add_group = urlencode(
    {"Body": "ADD #MyGroup"}
)
add_groups = urlencode(
    {"Body": "ADD #MyGroup,#MySecondGroup"}
)

# GET contact
get_contact_1 = urlencode(
    {"Body": "GET 9086162014"}
)
get_contact_2 = urlencode(
    {"Body": "GET @Mitch"}
)

# GET group
get_group = urlencode(
    {"Body": "GET #MyGroup"}
)

# UPDATE contact
update_contact = urlencode(
    {"Body": "UPDATE 9086162014 @Mitch"}
)

# PUT contact into GROUP
put_contact = urlencode(
    {"Body": "PUT 9086162014 #MyGroup"}
)
put_contacts = urlencode(
    {"Body": "PUT 9086162014,@Mitch #MyGroup"}
)

# REMOVE contact from GROUP
remove_contact = urlencode(
    {"Body": "REMOVE 9086162014 #MyGroup"}
)
removes_contacts = urlencode(
    {"Body": "REMOVE 9086162014,@Mitch #MyGroup"}
)

# DELETE contact
delete_contact = urlencode(
    {"Body": "DELETE 9086162014"}
)
delete_contacts = urlencode(
    {"Body": "DELETE 9086162014,@Mitch"}
)

# Delete group
delete_group = urlencode(
    {"Body": "DELETE #MyGroup"}
)
delete_groups = urlencode(
    {"Body": "DELETE #MyGroup,#MySecondGroup"}
)

# send message
to_contact = urlencode(
    {"Body": "TO 9086162014\n\nyooo"}
)
to_contacts = urlencode(
    {"Body": "TO 9086162014,@Mitch\n\nyooo"}
)
to_group = urlencode(
    {"Body": "TO #MyGroup\n\nYooo"}
)
to_combo = urlencode(
    {"Body": "TO 9086162014,#MyGroup\n\nYooo"}
)



from src.airtext.controllers.parser import TextParser
from urllib.parse import urlencode, parse_qs

text = parse_qs(to_combo)['Body'][0]

parser = TextParser(text)
parser.parse(is_incoming=False)