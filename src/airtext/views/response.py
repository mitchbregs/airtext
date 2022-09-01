class IncomingResponse(object):
    ALL = "FROM {number} @{name}\n\n{body_content}"


class OutgoingResponse(object):
    __prehook__ = "FROM @airtext\n\n"

    AIRTEXT = __prehook__ + "About AIRTEXT..."
    ADD_CONTACT = __prehook__ + ("🎉 Added new contact!\n\n{number} @{name}")
    ADD_CONTACT_FAIL = __prehook__ + (
        "🤔 Hmmm, we could not add that contact for you. "
        "Are you sure it does not already exist?\n\n"
        "Try GET {number}."
    )
    GET_CONTACT = __prehook__ + (
        "Found the contact you were looking for! 😎\n\n{number} @{name}"
    )
    GET_CONTACT_FAIL = __prehook__ + (
        "🥸 We were not able to find that contact for you. "
        "Have you tried adding it?\n\n"
        "Try ADD {number}."
    )
    UPDATE_CONTACT = __prehook__ + ("✍️ Updated contact.\n\n{number} @{name}")
    UPDATE_CONTACT_FAIL = __prehook__ + (
        "Couldn't update contact. Are you sure it exists?\n\n" "Try GET {number}."
    )
    DELETE_CONTACT = __prehook__ + ("👻 Deleted contact.\n\n{number} @{name}")
    DELETE_CONTACT_FAIL = __prehook__ + (
        "😵‍💫 Something went wrong trying to delete that contact. "
        "Perhaps you may have not had it in your contact list.\n\n"
        "Try GET {number}."
    )
    COMMAND_NOT_FOUND = __prehook__ + (
        "You either did not provide a command 🤔, or the command you "
        "provided is invalid. 🙅\n\n"
        "The accepted commands are as follows:\n"
        "📲 TO\n"
        "📗 ADD\n"
        "🔎 GET\n"
        "🗑 DELETE\n"
        "📝 UPDATE\n"
    )
    NUMBER_NOT_FOUND = __prehook__ + (
        "The phone number you provided either does not exist or "
        "is not properly formatted. 📵\n\n"
        "Examples of valid phone number formats:\n"
        "⚪️ +19876543210\n"
        "🔴 19876543210\n"
        "🟠 9876543210\n"
        "🟡 +1 (987) 654-3210\n"
        "🟢 1 (987) 654-3210\n"
        "🔵 (987) 654-3210\n"
        "🟣 987.654.3210\n"
        "⚫️ 1.987.654.3210\n"
    )
    NAME_NOT_FOUND = __prehook__ + (
        "We could not find a name for your contact. 👤\n\n"
        "If you are trying to update a contact, make sure to include their @name.\n\n"
        "For example, UPDATE +19876543210 @JaneDoe."
    )
    BODY_NOT_FOUND = __prehook__ + (
        "🖇  We could not find any text or content to send.\n\n"
        "If you are sending a message to a contact, make sure to include a body of text or something!"
    )

    ERROR_MESSAGES = {
        "command-not-found": COMMAND_NOT_FOUND,
        "number-not-found": NUMBER_NOT_FOUND,
        "name-not-found": NAME_NOT_FOUND,
        "body-not-found": BODY_NOT_FOUND,
    }
