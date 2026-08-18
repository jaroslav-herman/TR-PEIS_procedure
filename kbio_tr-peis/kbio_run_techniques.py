from kbio.kbio_tech import ECC_parm
from kbio.kbio_tech import make_ecc_parm
from kbio.kbio_tech import make_ecc_parms


def PEIS_params(
    api,
    vs_init=False,
    Initial_Voltage_step=1.44,
    step_duration=0,
    record_dt=1,
    record_dE=1,
    Final_frequency=100,
    Initial_frequency=100,
    Lin_Log=False,
    Amplitude=0.005,
    Frequency_number=1,
    Average_N_times=1,
    Correction=False,
    Wait_for_steady=0.1,
    I_range=11,
):
    """
    Create ECC parameters for a Potentiostatic Electrochemical Impedance Spectroscopy (PEIS) technique.

    Parameters
    ----------
    api : object
        API object used by `make_ecc_parm`/`make_ecc_parms` to construct parameters.
    vs_init : bool, optional
        Whether the step is relative to the initial voltage (default False). ECC name: 'vs_initial'.
    Initial_Voltage_step : float, optional
        Starting voltage step in volts (default 1.44). ECC name: 'Initial_Voltage_step'.
    step_duration : float, optional
        Duration of the voltage step in seconds (default 0). ECC name: 'Duration_step'.
    record_dt : float, optional
        Time interval for recording in seconds (default 1). ECC name: 'Record_every_dT'.
    record_dE : float, optional
        Voltage increment for recording in volts (default 1). ECC name: 'Record_every_dI'.
    Final_frequency : float, optional
        Final frequency for the sweep in Hz (default 100). ECC name: 'Final_frequency'.
    Initial_frequency : float, optional
        Initial frequency for the sweep in Hz (default 100). ECC name: 'Initial_frequency'.
    Lin_Log : bool, optional
        Linear/log sweep flag (default False). ECC name: 'sweep'.
    Amplitude : float, optional
        AC amplitude in volts (default 0.005). ECC name: 'Amplitude_Voltage'.
    Frequency_number : int, optional
        Number of frequencies (default 1). ECC name: 'Frequency_number'.
    Average_N_times : int, optional
        Averaging count (default 1). ECC name: 'Average_N_times'.
    Correction : bool, optional
        Apply correction flag (default False). ECC name: 'Correction'.
    Wait_for_steady : float, optional
        Seconds to wait for steady state (default 0.1). ECC name: 'Wait_for_steady'.
    I_range : int, optional
        Current range index (default 11). ECC name: 'I_Range'.

    Returns
    -------
    list
        ECC parameter list constructed by `make_ecc_parms` and ready to pass to the instrument API.

    Example
    -------
    >>> ecc_params = PEIS_params(api, Initial_Voltage_step=1.44, Amplitude=0.005)
    """

    p_voltage = make_ecc_parm(
        api, ECC_parm("Initial_Voltage_step", float), Initial_Voltage_step
    )
    p_step_dur = make_ecc_parm(api, ECC_parm("Duration_step", float), step_duration)
    p_vs_init = make_ecc_parm(api, ECC_parm("vs_initial", bool), vs_init)
    p_record_dt = make_ecc_parm(api, ECC_parm("Record_every_dT", float), record_dt)
    p_record_dE = make_ecc_parm(api, ECC_parm("Record_every_dI", float), record_dE)
    p_ff = make_ecc_parm(api, ECC_parm("Final_frequency", float), Final_frequency)
    p_fi = make_ecc_parm(api, ECC_parm("Initial_frequency", float), Initial_frequency)
    p_linlog = make_ecc_parm(api, ECC_parm("sweep", bool), Lin_Log)
    p_ampl = make_ecc_parm(api, ECC_parm("Amplitude_Voltage", float), Amplitude)
    p_f_numbers = make_ecc_parm(
        api, ECC_parm("Frequency_number", int), Frequency_number
    )
    p_avg = make_ecc_parm(api, ECC_parm("Average_N_times", int), Average_N_times)
    p_correction = make_ecc_parm(api, ECC_parm("Correction", bool), Correction)
    p_steady = make_ecc_parm(api, ECC_parm("Wait_for_steady", float), Wait_for_steady)
    p_I_range = make_ecc_parm(api, ECC_parm("I_Range", int), I_range)

    ecc_parms = make_ecc_parms(
        api,
        p_voltage,
        p_step_dur,
        p_vs_init,
        p_record_dt,
        p_record_dE,
        p_ff,
        p_fi,
        p_linlog,
        p_ampl,
        p_f_numbers,
        p_avg,
        p_correction,
        p_steady,
        p_I_range,
    )
    return ecc_parms


def OCV_params(
    api, Rest_time_T=30, Record_every_dE=0.05, Record_every_dT=0.1, I_range=5, E_range=3
):
    """
    Create OCV (Open Circuit Voltage) parameters.

    Parameters
    ----------
    api : object
        API object used to make ECC parameters.
    Rest_time_T : float, optional
        Rest duration in seconds (default is 30).
    Record_every_dE : float, optional
        Record every dE in Volts (default is 0.05).
    Record_every_dT : float, optional
        Record every dT in seconds (default is 0.1).
    I_range : int, optional
        Current range (default is 5).
    E_range : int, optional
        Voltage range (default is 3).

    Returns
    -------
    ecc_parms : list
        List of ECC parameters constructed for the OCV technique.
    """
    p_time = make_ecc_parm(api, ECC_parm("Rest_time_T", float), Rest_time_T)
    p_record_dE = make_ecc_parm(
        api, ECC_parm("Record_every_dE", float), Record_every_dE
    )
    p_record_dT = make_ecc_parm(
        api, ECC_parm("Record_every_dT", float), Record_every_dT
    )
    p_erange = make_ecc_parm(api, ECC_parm("E_Range", int), E_range)
    p_irange = make_ecc_parm(api, ECC_parm("I_Range", int), I_range)
    ecc_parms = make_ecc_parms(
        api, p_time, p_record_dE, p_record_dT, p_erange, p_irange
    )
    return ecc_parms


def CA_params(
    api,
    Voltage_step=1.42,
    vs_init=False,
    Duration_step=30,
    Step_number=-1,
    Record_every_dT=0.1,
    Record_every_dI=1,
    N_cycles=0,
    I_range=11,
    E_range=3,
):
    """
    Create CA (Chronoamperometry) parameters.
    Parameters
    ----------
    api : object
        API object used to make ECC parameters.
    Voltage_step : float or list of floats, optional
        Voltage step value(s) in Volts (default is 1.42).
    vs_init : bool or list of bools, optional
        Voltage step vs initial one flag(s) (default is False).
    Duration_step : float or list of floats, optional
        Duration for each step in seconds (default is 30).
    Step_number : int, optional
        Number of steps that are run minus 1, e.g. when only first three steps are run, it should be 2 (default is -1).
    Record_every_dT : float, optional
        Record every time interval in seconds (default is 0.1).
    Record_every_dI : float, optional
        Record every current change in Amperes (default is 1).
    N_cycles : int, optional
        Number of times the technique is repeated (default is 0).
    I_range : int, optional
        Current range (default is 11).
    E_range : int, optional
        Voltage range (default is 3).

    Returns
    -------
    list
        List of ECC parameters constructed for the CA technique.
    """

    p_steps = list()
    idx = 0
    if type(Voltage_step) == float or type(Voltage_step) == int:
        Voltage_step = [Voltage_step]
        vs_init = [vs_init]
        Duration_step = [Duration_step]

    Step_number = Step_number if Step_number >= 0 else len(Voltage_step) - 1

    for vs_init_, Voltage_step_, Duration_step_ in zip(
        vs_init, Voltage_step, Duration_step
    ):
        parm = make_ecc_parm(api, ECC_parm("Voltage_step", float), Voltage_step_, idx)
        p_steps.append(parm)
        parm = make_ecc_parm(api, ECC_parm("Duration_step", float), Duration_step_, idx)
        p_steps.append(parm)
        parm = make_ecc_parm(api, ECC_parm("vs_initial", bool), vs_init_, idx)
        p_steps.append(parm)
        idx += 1

    p_record_dt = make_ecc_parm(
        api, ECC_parm("Record_every_dT", float), Record_every_dT
    )
    p_record_dI = make_ecc_parm(
        api, ECC_parm("Record_every_dI", float), Record_every_dI
    )
    p_number = make_ecc_parm(api, ECC_parm("Step_number", int), Step_number)
    p_cycles = make_ecc_parm(api, ECC_parm("N_Cycles", int), N_cycles)
    p_I_range = make_ecc_parm(api, ECC_parm("I_Range", int), I_range)
    p_E_range = make_ecc_parm(api, ECC_parm("E_Range", int), E_range)
    # make the technique parameter array
    ecc_parms = make_ecc_parms(
        api,
        *p_steps,
        p_record_dt,
        p_record_dI,
        p_number,
        p_cycles,
        p_I_range,
        p_E_range
    )
    return ecc_parms


def CV_params(
    api,
    vs_initial=[False, False, False, False, False],
    Voltage_step=[1.5, 0.3, 1.5, 1.5, 1.5],
    Scan_Rate=[0.2, 0.2, 0.2, 0.2, 0.2],
    Scan_number=2,
    Record_every_dE=0.01,
    Average_over_dE=True,
    N_Cycles=0,
    Begin_measuring_I=1,
    End_measuring_I=1,
    I_range=11,
    E_range=3,
):
    """
    Create CV (Cyclic Voltammetry) technique ECC parameters.

    Parameters
    ----------
    api : object
        API object used by `make_ecc_parm`/`make_ecc_parms` to construct parameters.
    vs_initial : list[bool] or bool, optional
        Flags indicating whether each step is relative to the initial voltage (defaults to five False values). ECC name: 'vs_initial'.
    Voltage_step : list[float] or float, optional
        Voltage step values in volts for each segment (default [1.5, 0.3, 1.5, 1.5, 1.5]). ECC name: 'Voltage_step'.
    Scan_Rate : list[float] or float, optional
        Scan rates in V/s for each segment (default [0.2,...]). ECC name: 'Scan_Rate'.
    Scan_number : int, optional
        Number of scans per segment (default 2). ECC name: 'Scan_number'.
    Record_every_dE : float, optional
        Voltage increment for recording in volts (default 0.01). ECC name: 'Record_every_dE'.
    Average_over_dE : bool, optional
        Whether to average measurements over dE intervals (default True). ECC name: 'Average_over_dE'.
    N_Cycles : int, optional
        Number of times the full CV sequence is repeated (default 0). ECC name: 'N_Cycles'.
    Begin_measuring_I : float, optional
        Fraction of the step at which to begin measuring current (0..1, default 1). ECC name: 'Begin_measuring_I'.
    End_measuring_I : float, optional
        Fraction of the step at which to stop measuring current (0..1, default 1). ECC name: 'End_measuring_I'.
    I_range : int, optional
        Current range index (default 11). ECC name: 'I_Range'.
    E_range : int, optional
        Voltage range index (default 3). ECC name: 'E_Range'.

    Returns
    -------
    list
        ECC parameter list constructed by `make_ecc_parms` suitable for passing to the instrument API.

    Example
    -------
    >>> ecc_params = CV_params(api, Voltage_step=[1.5, 0.3], Scan_Rate=[0.2, 0.2])
    """

    # dictionary of CV parameters (non exhaustive but aligned with documentation)
    CV_parms = {
        "vs_initial": ECC_parm("vs_initial", bool),
        "Voltage_step": ECC_parm("Voltage_step", float),
        "Scan_Rate": ECC_parm("Scan_Rate", float),  # V/s or array depending API
        "Scan_number": ECC_parm("Scan_number", int),
        "Record_every_dE": ECC_parm("Record_every_dE", float),
        "Average_over_dE": ECC_parm("Average_over_dE", bool),
        "N_Cycles": ECC_parm("N_Cycles", int),
        "Begin_measuring_I": ECC_parm("Begin_measuring_I", float),  # 0..1
        "End_measuring_I": ECC_parm("End_measuring_I", float),  # 0..1
        "I_range": ECC_parm("I_Range", int),
        "E_range": ECC_parm("E_Range", int),
    }

    p_steps = list()
    idx = 0
    for vs_initial_, Voltage_step_, Scan_Rate_ in zip(
        vs_initial, Voltage_step, Scan_Rate
    ):
        parm = make_ecc_parm(api, CV_parms["vs_initial"], vs_initial_, idx)
        p_steps.append(parm)
        parm = make_ecc_parm(api, CV_parms["Voltage_step"], Voltage_step_, idx)
        p_steps.append(parm)
        parm = make_ecc_parm(api, CV_parms["Scan_Rate"], Scan_Rate_, idx)
        p_steps.append(parm)
        idx += 1

    p_scan_number = make_ecc_parm(api, CV_parms["Scan_number"], Scan_number)
    p_record_dE = make_ecc_parm(api, CV_parms["Record_every_dE"], Record_every_dE)
    p_avg_dE = make_ecc_parm(api, CV_parms["Average_over_dE"], Average_over_dE)
    p_cycles = make_ecc_parm(api, CV_parms["N_Cycles"], N_Cycles)
    p_begin_I = make_ecc_parm(api, CV_parms["Begin_measuring_I"], Begin_measuring_I)
    p_end_I = make_ecc_parm(api, CV_parms["End_measuring_I"], End_measuring_I)
    p_I_range = make_ecc_parm(api, CV_parms["I_range"], I_range)
    p_E_range = make_ecc_parm(api, CV_parms["E_range"], E_range)

    # --- assemble technique parameters ---
    ecc_parms = make_ecc_parms(
        api,
        *p_steps,
        p_scan_number,
        p_record_dE,
        p_avg_dE,
        p_cycles,
        p_begin_I,
        p_end_I,
        p_I_range,
        p_E_range
    )

    return ecc_parms


def CP_params(
    api,
    Current_step=[0.001, 0.002, 0.0005],
    Duration_step=[2, 1, 3],
    vs_init=[False, False, True],
    step_number=-1,
    Record_every_dT=0.1,
    Record_every_dE=0.01,
    N_Cycles=1,
    I_range=11,
):
    """
    Create CP (Chronopotentiometry) parameters.
    Parameters
    ----------
    api : object
        API object used to make ECC parameters.
    Current_step : float or list of floats, optional
        Current step value(s) in Amperes (default is 0.001).
    vs_init : bool or list of bools, optional
        Current step vs initial one flag(s) (default is False).
    Duration_step : float or list of floats, optional
        Duration for each step in seconds (default is 30).
    Step_number : int, optional
        Number of steps that are run minus 1, e.g. when only first three steps are run, it should be 2 (default is -1).
    Record_every_dT : float, optional
        Record every time interval in seconds (default is 0.1).
    Record_every_dI : float, optional
        Record every current change in Amperes (default is 1).
    N_cycles : int, optional
        Number of times the technique is repeated (default is 0).
    I_range : int, optional
        Current range (default is 11).
    E_range : int, optional
        Voltage range (default is 3).

    Returns
    -------
    list
        List of ECC parameters constructed for the CA technique.
    """

    p_steps = list()
    idx = 0
    if isinstance(Current_step, (float, int)):
        Current_step = [Current_step]
        vs_init = [vs_init]
        Duration_step = [Duration_step]

    step_number = step_number if step_number >= 0 else len(Current_step) - 1

    for vs_init_, Current_step_, Duration_step_ in zip(
        vs_init, Current_step, Duration_step
    ):
        parm = make_ecc_parm(api, ECC_parm("Current_step", float), Current_step_, idx)
        p_steps.append(parm)
        parm = make_ecc_parm(api, ECC_parm("Duration_step", float), Duration_step_, idx)
        p_steps.append(parm)
        parm = make_ecc_parm(api, ECC_parm("vs_initial", bool), vs_init_, idx)
        p_steps.append(parm)
        idx += 1

    p_nb_steps = make_ecc_parm(api, ECC_parm("Step_number", int), step_number)
    p_record_dt = make_ecc_parm(
        api, ECC_parm("Record_every_dT", float), Record_every_dT
    )
    p_record_dE = make_ecc_parm(
        api, ECC_parm("Record_every_dE", float), Record_every_dE
    )
    p_repeat = make_ecc_parm(api, ECC_parm("N_Cycles", int), N_Cycles)
    p_I_range = make_ecc_parm(api, ECC_parm("I_Range", int), I_range)
    ecc_parms = make_ecc_parms(
        api, *p_steps, p_nb_steps, p_record_dt, p_record_dE, p_I_range, p_repeat
    )
    return ecc_parms


def LOOP_params(api, loop_N_times=0, protocol_number=0):
    """
    Create ECC parameters for a LOOP technique.

    Parameters
    ----------
    api : object
        API object used by `make_ecc_parm`/`make_ecc_parms` to construct
        parameters.
    loop_N_times : int, optional
        Number of loop repetitions (default 0). ECC name: 'loop_N_times'.
    protocol_number : int, optional
        Protocol index/number to loop back to. The first technique has number 0. (default 0). ECC name:
        'protocol_number'.

    Returns
    -------
    list
        ECC parameter list constructed by `make_ecc_parms` and ready to pass
        to the instrument API.

    Example
    -------
    >>> ecc_params = LOOP_params(api, loop_N_times=3, protocol_number=1)
    """
    # dictionary of LOOP parameters
    LOOP_parms = {
        "loop_N_times": ECC_parm("loop_N_times", int),
        "protocol_number": ECC_parm("protocol_number", int),
    }
    p_number = make_ecc_parm(api, LOOP_parms["loop_N_times"], loop_N_times)
    p_technique = make_ecc_parm(api, LOOP_parms["protocol_number"], protocol_number)
    ecc_parms = make_ecc_parms(api, p_number, p_technique)
    return ecc_parms
