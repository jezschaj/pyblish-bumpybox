import pyblish.api


class ValidateDynamics(pyblish.api.InstancePlugin):
    """ Validates that the DOP path is set. """

    families = ["dynamics"]
    order = pyblish.api.ValidatorOrder
    label = "Dynamics"

    def process(self, instance):

        node = instance[0]

        msg = "No DOP path specified for node \"{0}\"."
        assert node.parm("doppath").eval(), msg.format(node.name())