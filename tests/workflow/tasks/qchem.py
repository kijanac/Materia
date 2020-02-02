import materia
import textwrap
import unittest.mock as mock


def test_qchem_rttddft():
    settings = materia.Settings(
        dt=0.02,
        Stabilize=0,
        TCLOn=0,
        MaxIter=100,
        ApplyImpulse=1,
        ApplyCw=0,
        FieldFreq=0.7,
        Tau=0.07,
        FieldAmplitude=0.001,
        ExDir=1.0,
        EyDir=1.0,
        EzDir=1.0,
        Print=0,
        StatusEvery=10,
        SaveDipoles=1,
        DipolesEvery=2,
        SavePopulations=0,
        SaveFockEnergies=0,
        WriteDensities=0,
        SaveEvery=500,
        FourierEvery=5000,
        MMUT=1,
        LFLPPC=0,
    )

    out_str = textwrap.dedent(
        """                                 dt=0.02
                                 Stabilize=0
                                 TCLOn=0
                                 MaxIter=100
                                 ApplyImpulse=1
                                 ApplyCw=0
                                 FieldFreq=0.7
                                 Tau=0.07
                                 FieldAmplitude=0.001
                                 ExDir=1.0
                                 EyDir=1.0
                                 EzDir=1.0
                                 Print=0
                                 StatusEvery=10
                                 SaveDipoles=1
                                 DipolesEvery=2
                                 SavePopulations=0
                                 SaveFockEnergies=0
                                 WriteDensities=0
                                 SaveEvery=500
                                 FourierEvery=5000
                                 MMUT=1
                                 LFLPPC=0"""
    )
    # FIXME: make this test work on Windows using pathlib

    mock_open = mock.mock_open()
    mock_expand_path = mock.MagicMock(side_effect=lambda s: s)
    mock_os_makedirs = mock.MagicMock(side_effect=lambda s: s)

    with mock.patch("builtins.open", mock_open):
        with mock.patch("os.makedirs", mock_os_makedirs):
            materia.WriteQChemTDSCF(
                settings=settings, work_directory="/mock/path/to/dir"
            ).run()

        # mock_expand_path.assert_called_once_with("/mock/path")
    mock_os_makedirs.assert_called_once_with("/mock/path/to/dir")
    mock_open.assert_called_once_with("/mock/path/to/dir/TDSCF.prm", "w")
    mock_open().write.assert_called_once_with(out_str)


def test_write_qchem_tdscf():
    settings = materia.Settings(
        dt=0.02,
        Stabilize=0,
        TCLOn=0,
        MaxIter=100,
        ApplyImpulse=1,
        ApplyCw=0,
        FieldFreq=0.7,
        Tau=0.07,
        FieldAmplitude=0.001,
        ExDir=1.0,
        EyDir=1.0,
        EzDir=1.0,
        Print=0,
        StatusEvery=10,
        SaveDipoles=1,
        DipolesEvery=2,
        SavePopulations=0,
        SaveFockEnergies=0,
        WriteDensities=0,
        SaveEvery=500,
        FourierEvery=5000,
        MMUT=1,
        LFLPPC=0,
    )

    out_str = textwrap.dedent(
        """                                 dt=0.02
                                 Stabilize=0
                                 TCLOn=0
                                 MaxIter=100
                                 ApplyImpulse=1
                                 ApplyCw=0
                                 FieldFreq=0.7
                                 Tau=0.07
                                 FieldAmplitude=0.001
                                 ExDir=1.0
                                 EyDir=1.0
                                 EzDir=1.0
                                 Print=0
                                 StatusEvery=10
                                 SaveDipoles=1
                                 DipolesEvery=2
                                 SavePopulations=0
                                 SaveFockEnergies=0
                                 WriteDensities=0
                                 SaveEvery=500
                                 FourierEvery=5000
                                 MMUT=1
                                 LFLPPC=0"""
    )
    # FIXME: make this test work on Windows using pathlib

    mock_open = mock.mock_open()
    mock_expand_path = mock.MagicMock(side_effect=lambda s: s)
    mock_os_makedirs = mock.MagicMock(side_effect=lambda s: s)

    with mock.patch("builtins.open", mock_open):
        with mock.patch("os.makedirs", mock_os_makedirs):
            materia.WriteQChemTDSCF(
                settings=settings, work_directory="/mock/path/to/dir"
            ).run()

        # mock_expand_path.assert_called_once_with("/mock/path")
    mock_os_makedirs.assert_called_once_with("/mock/path/to/dir")
    mock_open.assert_called_once_with("/mock/path/to/dir/TDSCF.prm", "w")
    mock_open().write.assert_called_once_with(out_str)
