import os

import pymel
import pyblish.api

import alembic_export


class ExtractAlembic(pyblish.api.InstancePlugin):
    """Superclass for exporting alembic files."""

    order = pyblish.api.ExtractorOrder
    optional = True
    hosts = ["maya"]
    targets = ["process.local"]
    families = ["cache", "camera", "geometry"]
    label = "Alembic"

    def process(self, instance):

        # Validate whether we can strip namespaces.
        stripNamespaces = 0
        root_names = []
        for node in instance.data["nodes"]:
            if node.name().split(":")[-1] not in root_names:
                root_names.append(node.name().split(":")[-1])
            else:
                self.log.warning(
                    "Can't strip namespaces, because of conflicting root "
                    "names. Nodes will be renamed."
                )
                stripNamespaces = -1

        # Get frame range
        frame_start = int(pymel.core.playbackOptions(q=True, min=True))
        frame_end = int(pymel.core.playbackOptions(q=True, max=True))

        # Ensure output directory exists.
        path = os.path.dirname(instance.data["output_path"])
        if not os.path.exists(path):
            os.makedirs(path)

        # Turn off viewport updating while exporting.
        pymel.core.general.refresh(suspend=True)
        try:
            alembic_export.export(
                instance.data["output_path"],
                frameRange=[[frame_start, frame_end]],
                root=root_names,
                stripNamespaces=stripNamespaces,
                uvWrite=True,
                worldSpace=True,
                wholeFrameGeo=True,
                eulerFilter=True,
                writeVisibility=True
            )
        except Exception as e:
            raise e
        pymel.core.general.refresh(suspend=False)
