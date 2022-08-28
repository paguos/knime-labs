import logging
import knime_extension as knext

from step import PenguinStep
from config import PenguinGender, PenguinSpecies

LOGGER = logging.getLogger(__name__)


@knext.node(
    name="Penguin (Palmer Archipelago)",
    node_type=knext.NodeType.SOURCE,
    icon_path="resources/penguin.png",
    category="/community"
)
@knext.output_table(
    name="Output Data",
    description="The collected data from the different penguins datasets."
)
class PenguinNode:
    """
    A node that fetches the data penguin data from the palmer archipelago data sets.

    The node uses data from the following publications:

    1. https://doi.org/10.6073/pasta/2b1cff60f81640f182433d23e68541ce

    2. https://doi.org/10.6073/pasta/409c808f8fc9899d02401bdb04580af7

    3. https://doi.org/10.6073/pasta/2b1cff60f81640f182433d23e68541ce

    Data are available by CC-0 license in accordance with the Palmer Station LTER Data Policy
    and the LTER Data Access Policy for Type I data.
    """

    configure = []

    penguin_gender = knext.StringParameter(
        "Gender",
        "The penguin gender to select",
        PenguinGender.ALL.name,
        enum=[en.name for en in PenguinGender]
    )

    penguin_species = knext.StringParameter(
        "Species",
        "The penguin species to select",
        PenguinSpecies.ALL.name,
        enum=[en.name for en in PenguinSpecies]
    )

    def configure(self, configure_context):
        pass

    def execute(self, exec_context):
        step = PenguinStep(gender=self.penguin_gender,
                           species=self.penguin_species)
        return knext.Table.from_pandas(step.execute())
