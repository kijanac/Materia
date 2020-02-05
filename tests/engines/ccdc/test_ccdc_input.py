import materia
import unittest.mock as mock


def test_ccdc_input_write():
    ccdc_code = """print('This is test code.')"""

    mock_open = mock.mock_open()
    mock_expand = mock.MagicMock(side_effect=lambda s: s)

    with mock.patch("builtins.open", mock_open):
        with mock.patch("materia.expand", mock_expand):
            materia.CCDCInput(ccdc_code).write("/mock/path")

    mock_expand.assert_called_once_with("/mock/path")
    mock_open.assert_called_once_with("/mock/path", "w")
    mock_open().write.assert_called_once_with("print('This is test code.')")
