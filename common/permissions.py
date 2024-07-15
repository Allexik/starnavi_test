from rest_framework import permissions


def get_relation_permission(relation_checker):
    class RelationPermission(permissions.BasePermission):

        def has_object_permission(self, request, view, obj):
            if request.user.is_superuser:
                return True
            return relation_checker(obj, request.user, request, view)

    return RelationPermission


IsOwner = get_relation_permission(
    lambda obj, user, *args: obj.user == user
)


IsOwnerOrReadOnly = get_relation_permission(
    lambda obj, user, request, *args: (
        request.method in permissions.SAFE_METHODS or
        obj.user == user
    )
)
