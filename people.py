from datetime import datetime
from flask import make_response, abort
from random import randint

RANDOM_RANGE_CAP = 9999  # upper cap for the pseudo-random number generator for id


def generateId():
    return (randint(0, RANDOM_RANGE_CAP))


# Data to serve over API
PEOPLE = {}


def read_all():
    """
    responds to a request for /api/profile
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from data
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]


def read_one(id):
    """
    responds to a request for /api/profile/{id}
    with one matching profile from people
    :param id:   id of profile to find
    :return:        profile matching username
    """
    # Check if profile exists in people
    if id in PEOPLE:
        profile = PEOPLE.get(id)

    # otherwise, not found
    else:
        abort(
            404, "profile with ID {id} not found".format(
                id=id)
        )

    return profile


def create(profile):
    """
    creates a new profile in the people structure
    based on the passed id in profile data
    :param profile:  profile to create in people structure
    :return:        201 on success, 406 on profile exists
    """
    last_name = profile.get("last_name", None)
    first_name = profile.get("first_name", None)
    username = profile.get("username", None)
    age = profile.get("age", None)
    id = generateId()

    # Check if the id exists already
    isIdUnique = False
    while(isIdUnique == False):
        # if id exists, generate a new Id
        if id in PEOPLE:
            id = generateId()
        else:
            isIdUnique = True

    PEOPLE[id] = {
        "last_name": last_name,
        "first_name": first_name,
        "username": username,
        "age": age,
        "id": id,
    }
    return make_response(
        "{username} successfully created".format(username=username), 201
    )


def update(profile):
    """
    updates an existing profile in the people structure
    :param profile:  profile to update
    :return:        updated profile structure
    """
    id = profile.get("id")
    # Check if profile exists in people
    if id in PEOPLE:
        # Update age and username only
        PEOPLE[id]["age"] = profile.get("age")
        PEOPLE[id]["username"] = profile.get("username")

        return PEOPLE[id]

    # otherwise, throw an error
    else:
        abort(
            404, "profile with Id {id} not found".format(
                id=id)
        )


def delete(id):
    """
    deletes a profile from the people structure
    :param id:   id of profile to delete
    :return:        200 on successful delete, 404 if not found
    """

    # Check if the profile exists
    if id in PEOPLE:
        username = PEOPLE[id]["username"]
        del PEOPLE[id]
        return make_response(
            "{id} with username {username} successfully deleted".format(
                id=id, username=username), 200
        )

    # Otherwise, profile to delete not found
    else:
        abort(
            404, "profile with id {id} not found".format(
                id=id)
        )
