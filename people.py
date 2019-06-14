from datetime import datetime
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
PEOPLE = {}


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]


def read_one(last_name):
    """
    This function responds to a request for /api/people/{last_name}
    with one matching person from people
    :param last_name:   last name of person to find
    :return:        person matching last name
    """
    # Does the person exist in people?
    if last_name in PEOPLE:
        person = PEOPLE.get(last_name)

    # otherwise, nope, not found
    else:
        abort(
            404, "Person with last name {last_name} not found".format(last_name=last_name)
        )

    return person


def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    last_name = person.get("last_name", None)
    first_name = person.get("first_name", None)

    # Does the person exist already?
    if last_name not in PEOPLE and last_name is not None:
        PEOPLE[last_name] = {
            "last_name": last_name,
            "first_name": first_name,
            "timestamp": get_timestamp(),
        }
        return make_response(
            "{last_name} successfully created".format(last_name=last_name), 201
        )

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Peron with last name {last_name} already exists".format(last_name=last_name),
        )


def update(last_name, person):
    """
    This function updates an existing person in the people structure
    :param last_name:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    # Does the person exist in people?
    if last_name in PEOPLE:
        PEOPLE[last_name]["first_name"] = person.get("first_name")
        PEOPLE[last_name]["timestamp"] = get_timestamp()

        return PEOPLE[last_name]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Person with last name {last_name} not found".format(last_name=last_name)
        )


def delete(last_name):
    """
    This function deletes a person from the people structure
    :param last_name:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    if last_name in PEOPLE:
        del PEOPLE[last_name]
        return make_response(
            "{last_name} successfully deleted".format(last_name=last_name), 200
        )

    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Person with last name {last_name} not found".format(last_name=last_name)
        )
