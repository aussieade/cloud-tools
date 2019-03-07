#
# Filename: os_keystone_utils.py
# Author: Ade <aussieade@gmail.com>
#
"""openstack keystone utility functions"""

from __future__ import print_function

from keystoneclient.exceptions import NotFound
from prettytable import PrettyTable


def get_projects_module(keystone):
    """get correct project module name"""
    if keystone.version == 'v3':
        return keystone.projects
    else:
        return keystone.tenants


def get_project(keystone, name_or_id):
    """get project by name or id"""
    projects = get_projects_module(keystone)
    try:
        project = projects.get(name_or_id)
    except NotFound:
        project = projects.find(name=name_or_id)
    return project


def get_user(keystone, name_or_id):
    """get user by name or id"""
    try:
        user = keystone.users.get(name_or_id)
    except NotFound:
        user = keystone.users.find(name=name_or_id)
    return user


def get_users(keystone, project):
    """get user objects for all users in project"""
    users = []
    users_ra = get_members(keystone, project)
    for user in users_ra:
        users.append(get_user(keystone, user))
    return users


def get_members(keystone, project):
    """get member/roles of a project

    :return: {userid: { username, [projectname, ...] } for each user
    """
    role_assignments = keystone.role_assignments.list(project=project.id,
                                                      include_names=True)
    users = {}
    for ra in role_assignments:

        if ra.user['id'] in users:
            users[ra.user['id']]['roles'].append(ra.role['name'])
        else:
            users[ra.user['id']] = {}
            users[ra.user['id']]['name'] = ra.user['name']
            users[ra.user['id']]['roles'] = [ra.role['name']]
    return users


def print_members(keystone, project):
    """pretty print project users and role assignments"""
    table = PrettyTable(["ID", "Username", "Roles"])

    users = get_members(keystone, project)

    for user_id, attrs in users.items():
        table.add_row([user_id, attrs['name'], ", ".join(attrs['roles'])])
    print("Members of %s (%s):" % (project.name, project.id))
    print(str(table))


def get_role(keystone, name):
    """get role object"""
    try:
        role = keystone.roles.list(name=name)
    except NotFound:
        role = None
    return role[0]
