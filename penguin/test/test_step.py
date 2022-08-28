import pandas as pd
import pytest
import tempfile as tpf

from unittest import mock

from node.step import PenguinStep


TEST_IDS = [1, 2]
TEST_GENDERS = ['MALE', 'FEMALE']


# Fixtures

@pytest.fixture
def mocked_content():
    data = {'test_id': TEST_IDS, 'Sex': TEST_GENDERS}
    with tpf.TemporaryFile() as file:
        df = pd.DataFrame(data=data)
        df.to_csv(file)
        file.seek(0)
        yield file.read()


@pytest.fixture
def get_request(mocked_content):
    with mock.patch("requests.get") as requests_mock:
        type(requests_mock.return_value).content = mock.PropertyMock(
            return_value=mocked_content)
        yield requests_mock

# Tests


def test_complete_execute(get_request):
    step = PenguinStep(gender="ALL", species="ALL")
    df = step.execute()

    # Verify it calls the correct URI
    get_request.assert_has_calls([
        mock.call(step.URI_ADELIE),
        mock.call(step.URI_CHINSTRAP),
        mock.call(step.URI_GENTOO)
    ])

    # Verify that the content was retrieved 3 times
    assert df["test_id"].tolist() == TEST_IDS * 3
    assert df["Sex"].tolist() == TEST_GENDERS * 3


@pytest.mark.parametrize("test_species,called_uri", [
    ("ADELIE", PenguinStep.URI_ADELIE),
    ("CHINSTRAP", PenguinStep.URI_CHINSTRAP),
    ("GENTOO", PenguinStep.URI_GENTOO)]
)
def test_single_species(test_species, called_uri, get_request):
    step = PenguinStep(gender="ALL", species=test_species)
    df = step.execute()

    # Verify it calls the correct URI
    get_request.assert_called_once_with(called_uri)

    # Verify that the content was retrieved once
    assert df["test_id"].tolist() == TEST_IDS
    assert df["Sex"].tolist() == TEST_GENDERS


@pytest.mark.parametrize("test_gender", TEST_GENDERS)
def test_filter_by_gender(test_gender, get_request):
    step = PenguinStep(gender=test_gender, species="ALL")
    df = step.execute()

    # Verify it calls the correct URI
    get_request.assert_has_calls([
        mock.call(step.URI_ADELIE),
        mock.call(step.URI_CHINSTRAP),
        mock.call(step.URI_GENTOO)
    ])

    # Verify that the gender filter the results
    assert df["Sex"].tolist() == [test_gender] * 3
