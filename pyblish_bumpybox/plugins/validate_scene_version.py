import os

import pyblish.api


class ValidateSceneVersion(pyblish.api.ContextPlugin):
    """ Validates the existence of version number on the scene. """

    order = pyblish.api.ValidatorOrder
    label = "Scene Version"
    optional = True

    def process(self, context):

        name, ext = os.path.splitext(context.data("currentFile"))
        failure_message = (
            'Could not find a version number in the scene name. Please add '
            'v[number] to the scene name, for example: "{0}_v001{1}".'
        ).format(name, ext)
        assert "version" in context.data, failure_message
