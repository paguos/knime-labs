import logging
import knime_extension as knext

import utils
from config import UnderstatCompetition
from step import UnderstatCompetitionStep

LOGGER = logging.getLogger(__name__)


@knext.node(
    name="Understat's Competition",
    node_type=knext.NodeType.SOURCE,
    icon_path="resources/football-award.png",
    category="/community"
)
@knext.output_table(
    name="Output Data",
    description="The collected data for a league in a specified season."
)
class UnderstatCompetitionNode:
    """

    """

    configure = []

    league = knext.StringParameter(
        "Competition",
        "The league's name (e.g. EPL, La Liga, Serie A, Bundesliga, Ligue 1)",
        UnderstatCompetition.EPL.name,
        enum=[en.value for en in UnderstatCompetition]
    )

    season = knext.IntParameter(
        "Season",
        "The league's season (e.g. 2019, 2020)",
        utils.current_season(),
        min_value=2014
    )

    def configure(self, configure_context):
        pass

    def execute(self, exec_context):
        step = UnderstatCompetitionStep(league=self.league,
                                        season=self.season)
        return knext.Table.from_pandas(step.execute())
