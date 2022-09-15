import itertools
import json

import jinja2

from airtext.controllers.twilio_webhooks.parser import MessageCommand, MessageData
from airtext.models.member import Member
from airtext.views.base import View


class BodyTemplates:
    INCOMING: str = """
FROM {{ number }} {% if name %}@{{ name }}{% endif %}
\n{{ body }}
"""

    TO: str = """
FROM @airtext
{% set len1 = contacts|length -%}
{% set len2 = group_contacts|length -%}
{% if contacts|length > 0 or groups|length > 0 %}
👻 Successfully sent {{ len1 + len2 }} message(s).
{% for group in groups %}
🟢👥 #{{ group['name'] -}}
{% endfor %}
{% for contact in contacts -%}
🟢👤 {{ contact['number'] }} {% if contact.get('name') %}@{{ contact.get('name') }}{% endif -%}
{% endfor %}
{% endif -%}
{% if contact_errors|length > 0 -%}
🔕 Something went wrong sending message(s) to the following:
{% for group in group_errors %}
🔴👥 #{{ group['name'] -}}
{% endfor %}
{% for contact in contact_errors -%}
🔴👤 {% if contact.number %}{{ contact.number }} {% endif %}{% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
{% for contact in group_contact_errors -%}
🔴👤 {% if contact.number %}{{ contact.number }} {% endif %}{% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
It's either these are invalid phone numbers, groups, or the contacts have unsubscribed.
{% endif %}
"""
    CREATE: str = """
FROM @airtext
{% if contacts|length > 0 or groups|length > 0 %}
🎉 Nice! Successfully created {{ groups|length }} new group(s) and {{ contacts|length }} new contact(s).
{% for group in groups %}
🟢👥 #{{ group.name -}}
{% endfor -%}
{% for contact in contacts %}
🟢👤 {{ contact.number }} {% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
{% endif -%}
{% if contact_errors|length > 0 or group_errors|length > 0 %}
👀 We had issues creating the following {{ group_errors|length }} groups(s) and {{ contact_errors|length }} contacts(s):
{% for group in group_errors %}
🔴👥 #{{ group.name -}}
{% endfor -%}
{% for contact in contact_errors %}
🔴👤 {% if contact.number %}{{ contact.number }} {% endif %}{% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
\nIt's likely that these already exist.
{% endif %}
💡 You can find a contact or group by using the 'GET' command!
""".strip()

    GET: str = """
FROM @airtext
{% if contacts|length > 0 or groups|length > 0 %}
🔎 Looks like we found {{ contacts|length }} contact(s) in {{ groups|length }} group(s):
{% for contact in contacts %}
🟢👤 {{ contact.number }} {% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
{% endif -%}
{% if contact_errors|length > 0 or group_errors|length > 0 %}
👀 We had issues finding the following {{ contact_errors|length }} contact(s) and {{ group_errors|length }} groups(s):
{% for group in group_errors %}
🔴👥 #{{ group.name -}}
{% endfor -%}
{% for contact in contact_errors %}
🔴👤 {% if contact.number %}{{ contact.number }} {% endif %}{% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
\nThese groups and/or contacts probably don't exist. Have you created them?
{% endif %}
💡 You can create a contact or group by using the 'CREATE' command!
""".strip()

    UPDATE: str = """
FROM @airtext
{% if contacts|length > 0 %}
✨ We were able to update {{ contacts|length }} contact(s):
{% for contact in contacts %}
🟢👤 {{ contact.number }} ↪ @{{ contact.name -}}
{% endfor %}
{% endif -%}
{% if contact_errors|length > 0 or group_errors|length > 0 %}
🛠 We had issues updating the following {{ contact_errors|length }} contact(s):
{% for contact in contact_errors %}
🔴👤 {% if contact.number %}{{ contact.number }} {% endif %}{% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
\nEither these contacts do not exist, or the name you chose is already taken in your contact list.
{% endif %}
💡 You can create a contact by using the 'CREATE' command!
\n🌟 You can find a contact by using the 'GET' command!
""".strip()

    DELETE: str = """
FROM @airtext
{% if contacts|length > 0 or groups|length > 0 %}
🗑 We deleted {{ groups|length }} group(s) and {{ contacts|length }} contact(s).
{% for group in groups %}
🟢👥 #{{ group.name -}}
{% endfor -%}
{% for contact in contacts %}
🟢👤 {% if contact.number %}{{ contact.number }} {% endif %}{% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
{% endif -%}
{% if contact_errors|length > 0 or group_errors|length > 0 %}
🙅‍♂️ We were unable to delete the following {{ group_errors|length }} groups(s) and {{ contact_errors|length }} contacts(s):
{% for group in group_errors %}
🔴👥 #{{ group.name -}}
{% endfor -%}
{% for contact in contact_errors %}
🔴👤 {% if contact.number %}{{ contact.number }} {% endif %}{% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
\nProbably because these groups and contacts don't exist. Were they ever created?
{% endif %}
💡 You can find a contact or group by using the 'GET' command!
""".strip()

    ADD: str = """
FROM @airtext
{% if group_contacts|length > 0 %}
⚡️ Sweet! Added {{ group_contacts|length }} contacts(s) to #{{ group.name }}.
{% for contact in group_contacts %}
🟢👤 {{ contact.number }} {% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
{% endif -%}
{% if group_contact_errors|length > 0 -%}
{% if group_errors|length > 0 %}
🙀 It seems as though the group you provided does not exist.
{% else %}
🙊 We had issues adding the following {{ group_contact_errors|length }} contact(s) to #{{ group.name }}:
{% for contact in group_contact_errors %}
🔴👤 {% if contact.number %}{{ contact.number }} {% endif %}{% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
\nIt's likely that these contacts already exist in the group.
{% endif -%}
{% endif %}
💡 You can find a group by using the 'GET' command!
""".strip()

    REMOVE: str = """
FROM @airtext
{% if group_contacts|length > 0 %}
✌️ Ok! Removed {{ group_contacts|length }} contacts(s) from #{{ group.name }}.
{% for contact in group_contacts %}
🟢👤 {{ contact.number }} {% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
{% endif -%}
{% if group_contact_errors|length > 0 -%}
{% if group_errors|length > 0 %}
🙀 It seems as though the group you provided does not exist.
{% else %}
🙊 We had issues removing the following {{ group_contact_errors|length }} contact(s) to #{{ group.name }}:
{% for contact in group_contact_errors %}
🔴👤 {% if contact.number %}{{ contact.number }} {% endif %}{% if contact.name %}@{{ contact.name }}{% endif -%}
{% endfor %}
\nIt's likely that these contacts don't exist in the group.
{% endif -%}
{% endif %}
💡 You can find a group by using the 'GET' command!
""".strip()

    ERROR: str = """
FROM @airtext
\n🚨 ERROR: {{ error_message }}
\nThese are all the valid commands:
⚪️ TO: sends a message to contact(s) or group(s)
\nExample:
```
TO #all
Hey dude, whats up?
```
or
```
TO @mitch,9997774444,#my-group
Yoooo
```
\n🔴 CREATE: creates contact(s) or group(s)
\nExample:
```
CREATE 9997774444 @some-name, #my-group, 8887776666
```
\n🟠 GET: gets contact(s) or group(s)
\nExample:
```
GET 9997774444 @some-name, #my-group, 8887776666
```
\n🟡 UPDATE: updates contact(s)
\nExample:
```
UPDATE 8887776666 @other-name
```
\n🟢 DELETE: deletes contact(s) or group(s)
\nExample:
```
DELETE 8887776666 @other-name
```
or
```
UPDATE #my-group
```
\n🔵 ADD: adds contact(s) to a single group
\nExample:
```
ADD @some-name,8887776666 #my-group
```
\n🟣 REMOVE: removes contact(s) from a single group
\nExample:
```
REMOVE @some-name,8887776666 #my-group
```
""".strip()


class Body(object):
    def __init__(self, template: BodyTemplates):
        environment = jinja2.Environment()
        self.template = environment.from_string(template)

    def format(self, **kwargs):
        return self.template.render(**kwargs)


class Incoming(View):
    """Handles incoming message end-user result."""

    def __init__(self, member: Member, message: MessageData):
        super().__init__(member=member, request=message)

    def send(self):
        """Sends a message and stores record."""
        contact = self.api.contacts.get_by_number_and_member_id(
            number=self.request.from_number, member_id=self.member.id
        )
        number = contact.number if contact else self.request.from_number
        name = contact.name if contact else None

        body = Body(template=BodyTemplates.INCOMING).format(
            number=number,
            name=name,
            body=self.request.body,
        )
        self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.request.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.request.command,
            contacts=json.dumps([dict(x) for x in self.request.contacts]),
            groups=json.dumps([dict(x) for x in self.request.groups]),
            body_content=self.request.body,
            error=self.request.error,
            error_message=self.request.error_message,
        )


class Outgoing(View):
    """Handles outgoing message from member."""

    def __init__(self, member: Member, message: MessageData):
        super().__init__(member=member, request=message)

    def run_to_command(self):

        # bug: make it so it works with body

        contacts = []
        contact_errors = []
        for request_contact in self.request.contacts:
            if not request_contact.number:
                try:
                    contact = self.api.contacts.get_by_name_and_member_id(
                        name=request_contact.name,
                        member_id=self.member.id,
                    )
                    self.api.messages.create(
                        to_number=contact.number,
                        from_number=self.member.proxy_number,
                        body=self.request.body_content,  # this is parsed text here
                        media_url=self.request.media_url,
                        proxy_number=self.member.proxy_number,
                        member_id=self.member.id,
                        command=self.request.command,
                        contacts=json.dumps([dict(x) for x in self.request.contacts]),
                        groups=json.dumps([dict(x) for x in self.request.groups]),
                        body_content=self.request.body,
                        error=self.request.error,
                        error_message=self.request.error_message,
                    )
                    contacts.append(contact.to_dict())
                except Exception as e:
                    contact_errors.append(dict(request_contact))
            else:
                try:
                    self.api.messages.create(
                        to_number=request_contact.number,
                        from_number=self.member.proxy_number,
                        body=self.request.body_content,  # this is parsed text here
                        media_url=self.request.media_url,
                        proxy_number=self.member.proxy_number,
                        member_id=self.member.id,
                        command=self.request.command,
                        contacts=json.dumps([dict(x) for x in self.request.contacts]),
                        groups=json.dumps([dict(x) for x in self.request.groups]),
                        body_content=self.request.body,
                        error=self.request.error,
                        error_message=self.request.error_message,
                    )
                    contacts.append(dict(request_contact))
                except Exception as e:
                    contact_errors.append(dict(request_contact))

        groups = []
        group_errors = []
        group_contacts = []
        group_contact_errors = []
        for request_group in self.request.groups:
            result = self.api.group_contacts.get_by_group_name_and_member_id(
                group_name=request_group.name,
                member_id=self.member.id,
            )
            if not len(result) > 0:
                group_errors.append(dict(request_group))
            else:
                groups.append(dict(request_group))

            for group_contact in result:
                try:
                    self.api.messages.create(
                        to_number=group_contact.number,
                        from_number=self.member.proxy_number,
                        body=self.request.body_content,  # this is parsed text here
                        media_url=self.request.media_url,
                        proxy_number=self.member.proxy_number,
                        member_id=self.member.id,
                        command=self.request.command,
                        contacts=json.dumps([dict(x) for x in self.request.contacts]),
                        groups=json.dumps([dict(x) for x in self.request.groups]),
                        body_content=self.request.body,
                        error=self.request.error,
                        error_message=self.request.error_message,
                    )
                    group_contacts.append(group_contact.to_dict())
                except Exception as e:
                    group_contact_errors.append(group_contact.to_dict())

        print("Contacts", contacts)
        print("Contact errors", contact_errors)
        print("Groups", groups)
        print("Group errors", group_errors)
        print("Group contacts", group_contacts)
        print("Group contact errors", group_contact_errors)

        body = Body(template=BodyTemplates.TO).format(
            contacts=contacts,
            contact_errors=contact_errors,
            groups=groups,
            group_errors=group_errors,
            group_contacts=group_contacts,
            group_contact_errors=group_contact_errors,
        )
        self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.request.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.request.command,
            contacts=json.dumps([dict(x) for x in self.request.contacts]),
            groups=json.dumps([dict(x) for x in self.request.groups]),
            body_content=self.request.body_content,
            error=self.request.error,
            error_message=self.request.error_message,
        )

        return

    def run_create_command(self):
        """Runs an `CREATE` command via message controller."""
        contacts = []
        contact_errors = []
        for request_contact in self.request.contacts:
            try:
                contact = self.api.contacts.create(
                    number=request_contact.number,
                    member_id=self.member.id,
                    name=request_contact.name,
                )
                group = self.api.groups.get_by_name_and_member_id(
                    name="all",
                    member_id=self.member.id
                )
                group_contact = self.api.group_contacts.create(
                    contact_id=contact.id,
                    group_id=group.id
                )
                contacts.append(contact)
            except Exception as e:
                contact_errors.append(request_contact)

        groups = []
        group_errors = []
        for request_group in self.request.groups:
            try:
                group = self.api.groups.create(
                    name=request_group.name,
                    member_id=self.member.id,
                )
                groups.append(group)
            except Exception as e:
                group_errors.append(request_group)

        print("Contacts", contacts)
        print("Contact errors", contact_errors)
        print("Groups", groups)
        print("Group errors", group_errors)

        body = Body(template=BodyTemplates.CREATE).format(
            contacts=contacts,
            contact_errors=contact_errors,
            groups=groups,
            group_errors=group_errors,
        )
        self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.request.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.request.command,
            contacts=json.dumps([dict(x) for x in self.request.contacts]),
            groups=json.dumps([dict(x) for x in self.request.groups]),
            body_content=self.request.body_content,
            error=self.request.error,
            error_message=self.request.error_message,
        )

        return

    def run_get_command(self):

        contacts = []
        contact_errors = []
        for request_contact in self.request.contacts:
            try:
                contact = self.api.contacts.get_by_number_or_name_and_member_id(
                    number=request_contact.number,
                    name=request_contact.name,
                    member_id=self.member.id,
                )
                if contact:
                    contacts.append(contact)
                else:
                    contact_errors.append(request_contact)
            except Exception as e:
                contact_errors.append(request_contact)

        groups = []
        group_errors = []
        for request_group in self.request.groups:
            try:
                group_contacts = (
                    self.api.group_contacts.get_by_group_name_and_member_id(
                        group_name=request_group.name,
                        member_id=self.member.id,
                    )
                )
                if len(group_contacts) > 0:
                    contacts.extend(group_contacts)
                    groups.append(request_group)
                else:
                    group_errors.append(request_group)
            except Exception as e:
                group_errors.append(request_group)

        print("Contacts", contacts)
        print("Contact errors", contact_errors)
        print("Groups", groups)
        print("Group errors", group_errors)

        body = Body(template=BodyTemplates.GET).format(
            contacts=contacts,
            contact_errors=contact_errors,
            groups=groups,
            group_errors=group_errors,
        )
        self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.request.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.request.command,
            contacts=json.dumps([dict(x) for x in self.request.contacts]),
            groups=json.dumps([dict(x) for x in self.request.groups]),
            body_content=self.request.body_content,
            error=self.request.error,
            error_message=self.request.error_message,
        )

        return

    def run_update_command(self):

        contacts = []
        contact_errors = []
        for request_contact in self.request.contacts:
            if not request_contact.number:
                pass
            else:
                try:
                    contact = self.api.contacts.update(
                        number=request_contact.number,
                        member_id=self.member.id,
                        name=request_contact.name,
                    )
                    contacts.append(contact)
                except Exception as e:
                    contact_errors.append(request_contact)

        print("Contacts", contacts)
        print("Contact errors", contact_errors)

        body = Body(template=BodyTemplates.UPDATE).format(
            contacts=contacts,
            contact_errors=contact_errors,
        )
        self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.request.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.request.command,
            contacts=json.dumps([dict(x) for x in self.request.contacts]),
            groups=json.dumps([dict(x) for x in self.request.groups]),
            body_content=self.request.body_content,
            error=self.request.error,
            error_message=self.request.error_message,
        )

        return

    def run_delete_command(self):

        contacts = []
        contact_errors = []
        for request_contact in self.request.contacts:
            try:
                contact = self.api.contacts.delete(
                    number=request_contact.number,
                    name=request_contact.name,
                    member_id=self.member.id,
                )
                contacts.append(contact)
            except Exception as e:
                contact_errors.append(request_contact)

        groups = []
        group_errors = []
        for request_group in self.request.groups:
            try:
                group = self.api.groups.delete(
                    name=request_group.name,
                    member_id=self.member.id,
                )
                groups.append(group)
            except Exception as e:
                group_errors.append(request_group)

        print("Contacts", contacts)
        print("Contact errors", contact_errors)
        print("Groups", groups)
        print("Group errors", group_errors)

        body = Body(template=BodyTemplates.DELETE).format(
            contacts=contacts,
            contact_errors=contact_errors,
            groups=groups,
            group_errors=group_errors,
        )
        self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.request.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.request.command,
            contacts=json.dumps([dict(x) for x in self.request.contacts]),
            groups=json.dumps([dict(x) for x in self.request.groups]),
            body_content=self.request.body_content,
            error=self.request.error,
            error_message=self.request.error_message,
        )

        return

    def run_add_command(self):

        group_errors = []
        group = self.api.groups.get_by_name_and_member_id(
            name=self.request.groups[0].name,
            member_id=self.member.id,
        )
        if not group:
            group_errors.append(self.request.groups[0])

        group_contacts = []
        group_contact_errors = []
        for request_contact in self.request.contacts:
            try:
                contact = self.api.contacts.create_if_not_exists(
                    number=request_contact.number,
                    name=request_contact.name,
                    member_id=self.member.id,
                )
                # bug here: need to add to #all if created
                group_contact = self.api.group_contacts.create(
                    group_id=group.id,
                    contact_id=contact.id,
                )
                group_contacts.append(contact)
            except Exception as e:
                group_contact_errors.append(request_contact)

        print("Group", group)
        print("Group errors", group_errors)
        print("Group contacts", group_contacts)
        print("Group contact errors", group_contact_errors)

        body = Body(template=BodyTemplates.ADD).format(
            group=group,
            group_errors=group_errors,
            group_contacts=group_contacts,
            group_contact_errors=group_contact_errors,
        )
        self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.request.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.request.command,
            contacts=json.dumps([dict(x) for x in self.request.contacts]),
            groups=json.dumps([dict(x) for x in self.request.groups]),
            body_content=self.request.body_content,
            error=self.request.error,
            error_message=self.request.error_message,
        )

    def run_remove_command(self):

        group_errors = []
        group = self.api.groups.get_by_name_and_member_id(
            name=self.request.groups[0].name,
            member_id=self.member.id,
        )
        if not group:
            group_errors.append(self.request.groups[0])

        group_contacts = []
        group_contact_errors = []
        for request_contact in self.request.contacts:
            try:
                contact = self.api.contacts.get_by_number_or_name_and_member_id(
                    number=request_contact.number,
                    name=request_contact.name,
                    member_id=self.member.id,
                )
                group_contact = self.api.group_contacts.de;ete(
                    group_id=group.id,
                    contact_id=contact.id,
                )
                group_contacts.append(contact)
            except Exception as e:
                group_contact_errors.append(request_contact)

        print("Group", group)
        print("Group errors", group_errors)
        print("Group contacts", group_contacts)
        print("Group contact errors", group_contact_errors)

        body = Body(template=BodyTemplates.REMOVE).format(
            group=group,
            group_errors=group_errors,
            group_contacts=group_contacts,
            group_contact_errors=group_contact_errors,
        )
        self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.request.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.request.command,
            contacts=json.dumps([dict(x) for x in self.request.contacts]),
            groups=json.dumps([dict(x) for x in self.request.groups]),
            body_content=self.request.body_content,
            error=self.request.error,
            error_message=self.request.error_message,
        )


    def run_error(self, **kwargs):

        print("Error", self.request.error_message)

        body = Body(template=BodyTemplates.ERROR).format(
            error_message=self.request.error_message
        )
        self.api.messages.create(
            to_number=self.member.number,
            from_number=self.member.proxy_number,
            body=body,
            media_url=self.request.media_url,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.request.command,
            contacts=json.dumps([dict(x) for x in self.request.contacts]),
            groups=json.dumps([dict(x) for x in self.request.groups]),
            body_content=self.request.body_content,
            error=self.request.error,
            error_message=self.request.error_message,
        )

        return

    def send(self):
        """Sends a message and stores record."""
        if self.request.error:
            self.run_error()
        elif self.request.command == MessageCommand.TO:
            self.run_to_command()
        elif self.request.command == MessageCommand.CREATE:
            self.run_create_command()
        elif self.request.command == MessageCommand.GET:
            self.run_get_command()
        elif self.request.command == MessageCommand.UPDATE:
            self.run_update_command()
        elif self.request.command == MessageCommand.DELETE:
            self.run_delete_command()
        elif self.request.command == MessageCommand.ADD:
            self.run_add_command()
        elif self.request.command == MessageCommand.REMOVE:
            self.run_remove_command()
