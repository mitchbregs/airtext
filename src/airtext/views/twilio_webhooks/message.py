import jinja2

from airtext.controllers.base import RequestCommand, RequestParserData
from airtext.models.member import Member
from airtext.views.base import View


class BodyTemplates:
    AIRTEXT: str = \
        """
        About @airtext...
        """
    ADD_CONTACT: str = \
"""
FROM @airtext
{% if contacts|length > 0 %}
🎉 Nice! Successfully added {{ contacts|length }} new contact(s).
{% for contact in contacts %}
🟢 {{ contact['number'] }} {% if contact.get('name') %}@{{ contact.get('name') }}{% endif -%}
{% endfor %}
{% endif -%}
{% if contact_errors|length > 0 %}
👀 We had issues adding the following {{ contact_errors|length }} contact(s):
{% for number, name in contact_errors %}
🔴 {{ number }} {% if name %}@{{ name }}{% endif -%}
{% endfor %}

It's likely that these contact numbers or names already exist.
{% endif %}
💡 You can find a contact by using the 'GET' command!
{% if groups|length > 0 %}
If you were trying to create a group, use the 'CREATE' command.
{% endif %}
""".strip()
    GET_CONTACT: str = \
"""
FROM @airtext
{% if contacts|length > 0 %}
🔎 Looks like we found {{ contacts|length }} contact(s):
{% for contact in contacts %}
🟢 {{ contact['number'] }} {% if contact.get('name') %}@{{ contact.get('name') }}{% endif -%}
{% endfor %}
{% endif -%}
{% set len1 = contact_number_errors|length -%}
{% set len2 = contact_name_errors|length -%}
{% if contact_number_errors|length > 0 %}
🙉 We were not able to find the following {{ len1 + len2 }} contact(s):
{% for number in contact_number_errors %}
🔴 {{ number }}
{% endfor -%}
{% for name in contact_name_errors %}
🔴 @{{ number }}
{% endfor %}
It seems that probably these contacts do not exist yet.
{% endif %}
📝 You can create a contact by using the 'ADD' command!
{% if groups|length > 0 %}
If you were trying to list the contacts of a group, use the 'LIST' command.
{% endif %}
""".strip()
    UPDATE_CONTACT: str = \
"""
FROM @airtext
{% if contacts|length > 0 %}
👍 We were able to update {{ contacts|length }} contact(s):
{% for contact in contacts %}
🟢 {{ contact['number'] }} @{{ contact['name'] -}}
{% endfor %}
{% endif -%}
{% if contact_errors|length > 0 %}
🙉 We couldn't update the following {{ contact_errors|length }} contact(s):
{% for number, name in contact_errors %}
🔴 {{ number }} {% if name %}@{{ name }}{% endif -%}
{% endfor %}

It's either these contacts do not exist yet or you did not provide names for numbers.

📙 For example, to update a contact: UPDATE 9086162014 @mitchbregs

📗 You can create a contact by using the 'ADD' command!
{% endif %}
{% if groups|length > 0 %}
If you were trying to create a group, use the 'CREATE' command.
{% endif %}
""".strip()
    DELETE: str = "DELETE"
    CREATE: str = "CREATE"
    PUT: str = "PUT"
    REMOVE: str = "REMOVE"


class Body(object):

    def __init__(self, template: BodyTemplates):
        environment = jinja2.Environment()
        self.template = environment.from_string(template)

    def format(self, **kwargs):
        return self.template.render(**kwargs)


class Incoming(View):
    """Handles incoming message end-user result."""

    def __init__(self, member: Member, message: RequestParserData):
        super().__init__(member=member, message=message)

    def send(self):
        """Sends a message and stores record."""
        contact = self.api.contacts.get_by_number_and_member_id(
            number=self.message.from_number, member_id=self.member.id
        )
        name = contact.name if contact else None

        self.api.messages.create(
            from_number=self.message.from_number,
            to_number=self.message.to_number,
            body_content=self.message.body_content,
            media_content=self.message.media_content,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=None,
            numbers=[
                self.member.number,
            ],
            names=[],
            groups=[],
            body=IncomingResponse.ALL.format(
                number=self.message.from_number,
                name=name,
                body_content=self.message.body_content,
            ),
            error=False,
            error_code=None,
        )



class Outgoing(View):
    """Handles outgoing message from member."""

    def __init__(self, member: Member, message: RequestParserData):
        super().__init__(member=member, message=message)

    def run_airtext_command(self):
        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.message.command,
            numbers=self.message.numbers,
            names=self.message.names,
            groups=self.message.groups,
            body=OutgoingResponse.AIRTEXT,
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def run_to_command(self):
        self.api.messages.create(
            from_number=self.message.from_number,
            to_number=self.message.to_number,
            body_content=self.message.body_content,
            media_content=self.message.media_content,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.message.command,
            numbers=self.message.numbers,
            names=self.message.names,
            groups=self.message.groups,
            body=self.message.body,
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def run_add_command(self):
        """Runs an `ADD` command via message controller."""
        tmp = set([x[0] for x in self.message.number_names])
        numbers = list(set(self.message.numbers) - tmp)
        number_names = (
            self.message.number_names +
            [(number, None) for number in numbers]
        )

        contacts = []
        contact_errors = []
        for number_name in number_names:
            try:
                contact = self.api.contacts.create(
                    number=number_name[0],
                    member_id=self.member.id,
                    name=number_name[1],
                )
                group = self.api.groups.get_by_name_and_member_id(
                    name="all",
                    member_id=self.member.id,
                )
                group_contact = self.api.group_contacts.create(
                    contact_id=contact.id,
                    group_id=group.id,
                )
                contacts.append(contact.to_dict())
            except Exception as e:
                contact_errors.append(number_name)

        body = (
            Body(template=BodyTemplates.ADD_CONTACT)
            .format(
                contacts=contacts,
                contact_errors=contact_errors,
                groups=self.message.groups,
            )
        )
        message = self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.message.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.message.command,
            numbers=self.message.numbers,
            names=self.message.names,
            number_names=self.message.number_names,
            groups=self.message.groups,
            body_content=self.message.body_content,
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def run_get_command(self):

        numbers = set(self.message.numbers)
        names = set(self.message.names)

        contacts = []
        contact_number_errors = []
        for number in numbers:
            try:
                contact = self.api.contacts.get_by_number_and_member_id(
                    number=number,
                    member_id=self.member.id,
                )
                contacts.append(contact.to_dict())
            except Exception as e:
                contact_number_errors.append(number)

        contact_name_errors = []
        for name in names:
            try:
                contact = self.api.contacts.get_by_name_and_member_id(
                    name=name,
                    member_id=self.member.id,
                )
                contacts.append(contact.to_dict())
            except Exception as e:
                contact_name_errors.append(name)

        body = (
            Body(template=BodyTemplates.GET_CONTACT)
            .format(
                contacts=contacts,
                contact_number_errors=contact_number_errors,
                contact_name_errors=contact_name_errors,
                groups=self.message.groups,
            )
        )
        message = self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.message.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.message.command,
            numbers=self.message.numbers,
            names=self.message.names,
            number_names=self.message.number_names,
            groups=self.message.groups,
            body_content=self.message.body_content,
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def run_update_command(self):
        tmp = set([x[0] for x in self.message.number_names])
        numbers = list(set(self.message.numbers) - tmp)
        number_nameless = [(number, None) for number in numbers]

        contacts = []
        contact_errors = []
        for number, name in self.message.number_names:
            try:
                contact = self.api.contacts.update(
                    number=number,
                    member_id=self.member.id,
                    name=name,
                )
                contacts.append(contact.to_dict())
            except Exception as e:
                contact_errors.append((number, name))

        contact_errors += number_nameless

        body = (
            Body(template=BodyTemplates.UPDATE_CONTACT)
            .format(
                contacts=contacts,
                contact_errors=contact_errors,
                groups=self.message.groups,
            )
        )
        message = self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.message.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.message.command,
            numbers=self.message.numbers,
            names=self.message.names,
            number_names=self.message.number_names,
            groups=self.message.groups,
            body_content=self.message.body_content,
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def run_delete_command(self):

        contact = self.api.contacts.get_by_number_and_member_id(
            number=self.message.number, member_id=self.member.id
        )

        is_deleted = self.api.contacts.delete_contact(
            number=self.message.number,
            member_id=self.member.id,
        )

        if contact and is_deleted:
            self.api.messages.create(
                proxy_number=self.member.proxy_number,
                to_number=self.member.number,
                member_id=self.member.id,
                command=self.message.command,
                number=self.message.number,
                name=contact.name,
                body=OutgoingResponse.DELETE_CONTACT.format(
                    number=self.message.number,
                    name=contact.name,
                ),
                error=self.message.error,
                error_code=self.message.error_code,
            )

            return

        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.message.command,
            number=self.message.number,
            name=self.message.name,
            body=OutgoingResponse.DELETE_CONTACT_FAIL.format(
                number=self.message.number,
                name=self.message.name,
            ),
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def run_error(self, **kwargs):
        print("-- ERROR --", self.message)

        # self.api.messages.create(
        #     proxy_number=self.member.proxy_number,
        #     to_number=self.member.number,
        #     member_id=self.member.id,
        #     command=self.message.command,
        #     number=self.message.number,
        #     name=self.message.name,
        #     body=OutgoingResponse.ERROR_MESSAGES[self.message.error_code],
        #     error=self.message.error,
        #     error_code=self.message.error_code,
        # )

        return

    def send(self):
        """Sends a message and stores record."""
        if self.message.error:
            self.run_error()
        elif self.message.command.upper() == RequestCommand.AIRTEXT:
            self.run_airtext_command()
        elif self.message.command.upper() == RequestCommand.TO:
            self.run_to_command()
        elif self.message.command.upper() == RequestCommand.ADD:
            self.run_add_command()
        elif self.message.command.upper() == RequestCommand.GET:
            self.run_get_command()
        elif self.message.command.upper() == RequestCommand.UPDATE:
            self.run_update_command()
        elif self.message.command.upper() == RequestCommand.DELETE:
            self.run_delete_command()
        elif self.message.command.upper() == RequestCommand.PUT:
            self.run_put_command()
        elif self.message.command.upper() == RequestCommand.REMOVE:
            self.run_remove_command()
        else:
            return False

        return True
