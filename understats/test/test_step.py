
from node.step import UnderstatsLeagueStep


def test_execute():
    step = UnderstatsLeagueStep("EPL", "2019")
    df = step.execute()

    expected_rows = 20
    expected_columns = [
        'Team', 'M', 'W', 'D', 'L', 'G', 'GA', 'PTS', 'xG', 'NPxG',
        'xGA', 'NPxGA', 'NPxGD', 'PPDA', 'OPPDA', 'DC', 'ODC', 'xPTS'
    ]

    assert df.shape == (expected_rows, len(expected_columns))
    assert expected_columns == list(df.columns)
