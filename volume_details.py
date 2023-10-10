import openstack
from openstack.exceptions import ResourceNotFound


def get_volume(volume_id):
    conn = openstack.connect()

    volume = conn.block_storage.get_volume(volume_id)

    return volume


def get_user_from_id(user_id):
    conn = openstack.connect()
    user = conn.identity.get_user(user_id)
    return user


def get_project_by_id(project_id):
    conn = openstack.connect()

    return conn.identity.get_project(project_id)


def get_volume_attachment(volume_id):
    conn = openstack.connect()

    attachments = conn.block_storage.get_volume(volume_id).attachments

    if not attachments:
        return {
            "server_id": None,
            "attachment_id": None,
            "host_name": None,
            "device": None
        }

    attachment = attachments[0]

    return attachment


def get_server_by_id(server_id):
    conn = openstack.connect()
    server = conn.compute.get_server(server_id)
    return server


def get_volume_details(volume_id):
    volume_details = {
        "volume_id": volume_id,
        "volume_host": None,
        "volume_name": None,
        "user_name": None,
        "user_email": None,
        "project_name": None,
        "attachment_server_id": None,
        "attachment_server_name": None,
        "attachment_host_name": None,
        "attachment_device": None
    }
    try:
        volume = get_volume(volume_id)
        volume_details["volume_host"] = volume.host
        volume_details["volume_name"] = volume.name

        user = get_user_from_id(volume.user_id)
        volume_details["user_name"] = user.name
        volume_details["user_email"] = user.email

        project = get_project_by_id(volume.project_id)
        volume_details["project_name"] = project.name

        attachment = get_volume_attachment(volume_id)
        server = None
        server_details = {
            "name": None,
        }

        volume_details["attachment_server_id"] = attachment["server_id"]
        volume_details["attachment_host_name"] = attachment["host_name"]
        volume_details["attachment_device"] = attachment["device"]

        if attachment["server_id"]:
            server = get_server_by_id(attachment["server_id"])

        if server:
            server_details = {
                "name": server.name
            }
        volume_details["attachment_server_name"] = server_details["name"]
    except ResourceNotFound:
        pass

    return volume_details
