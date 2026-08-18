import os
import sys
from pathlib import Path
import time
from dataclasses import dataclass
import csv
from IPython.display import clear_output
from IPython.display import display
import ipywidgets as widgets

import kbio.kbio_types as KBIO
from kbio.c_utils import c_is_64b
from kbio.kbio_api import KBIO_api
from kbio.kbio_tech import ECC_parm


from kbio.kbio_tech import get_info_data
from kbio.kbio_tech import make_ecc_parm
from kbio.kbio_tech import make_ecc_parms
from kbio.utils import exception_brief
from kbio.tech_types import TECH_ID
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def experiment_warning(instrument, running=True, warning_widget=None):
    """
    Create an HTML warning or completion message for an ongoing experiment.

    Parameters
    ----------
    instrument : str
        Name or identifier of the instrument shown in the message.
    running : bool, optional
        If True, display a red "experiment running" warning. If False, display
        a green completion message.
    warning_widget : ipywidgets.HTML | None, optional
        Existing widget to update. A new ``ipywidgets.HTML`` widget is created
        when None.

    Returns
    -------
    ipywidgets.HTML
        Widget containing the formatted warning or completion HTML.
    """
    if running:
        value = f"""
        <div style="
            background-color:#ffcccc;
            border:3px solid red;
            padding:20px;
            font-size:24px;
            font-weight:bold;
        ">
        WARNING: EXPERIMENT RUNNING<br><br>
        Instrument: <span style="color:blue">{instrument}</span>
        </div>
        """
    else:
        value = f"""
        <div style="
            background-color:#ccffcc;
            border:3px solid green;
            padding:20px;
            font-size:24px;
            font-weight:bold;
        ">
        Experiment finished<br><br>
        Instrument: <span style="color:blue">{instrument}</span>
        </div>
        """

    if warning_widget is None:
        warning_widget = widgets.HTML()

    warning_widget.value = value
    return warning_widget


def get_exp_data(api, data, board_type, data_out, index=0):
    """
    Parse raw experiment records and append parsed values into data_out.

    Parameters
    ----------
    api : kbio.kbio_api.KBIO_api
        KBIO API instance used to convert raw channel words into physical values.
    data : tuple
        Raw experiment tuple of the form ``(current_values, data_info, data_record)``.
    board_type : int
        Numeric board type identifier used by the KBIO API converter.
    data_out : dict
        Output dictionary created by ``create_data_out``. Parsed values are
        appended to matching technique sections.
    index : int, optional
        Technique index or record counter inserted into each parsed row.

    Returns
    -------
    dict
        The updated ``data_out`` dictionary with parsed rows appended.
    """
    current_values, data_info, data_record = data
    if len(data_record) > 0:
        ix = 0
        for _ in range(data_info.NbRows):
            if data_info.TechniqueID == 100:
                tech_name = "OCV"
                inx = ix + data_info.NbCols
                t_high, t_low, *row = data_record[ix:inx]

                t_rel = (t_high << 32) + t_low
                t = current_values.TimeBase * t_rel
                Ewe = api.ConvertChannelNumericIntoSingle(row[0], board_type)
                # time = current_values.ElapsedTime
                parsed_row = {
                    "time/s": t,
                    "startTime/s": data_info.StartTime,
                    "Ewe/V": Ewe,
                    "Tech": index,
                    "Loop": data_info.loop,
                }
                # print(vmp3)
                if len(row) == 2:
                    Ece = api.ConvertChannelNumericIntoSingle(row[1], board_type)
                    parsed_row["Ece/V"] = Ece
                for var in parsed_row.keys():
                    data_out["OCV"][var].append(parsed_row[var])

            elif data_info.TechniqueID == 101:
                inx = ix + data_info.NbCols
                t_high, t_low, *row = data_record[ix:inx]

                nb_words = len(row)
                if nb_words != 3:
                    raise RuntimeError(f"CA : unexpected record length ({nb_words})")
                Ewe = api.ConvertChannelNumericIntoSingle(row[0], board_type)
                Iwe = api.ConvertChannelNumericIntoSingle(row[1], board_type)
                cycle = row[2]

                #         # compute timestamp in seconds
                t_rel = (t_high << 32) + t_low
                t = current_values.TimeBase * t_rel
                parsed_row = {
                    "time/s": t,
                    "startTime/s": data_info.StartTime,
                    "Ewe/V": Ewe,
                    "I/mA": Iwe,
                    "cycle number": cycle,
                    "Tech": index,
                    "Loop": data_info.loop,
                }
                for var in parsed_row.keys():
                    data_out["CA"][var].append(parsed_row[var])

            elif data_info.TechniqueID == 102:
                inx = ix + data_info.NbCols
                t_high, t_low, *row = data_record[ix:inx]

                nb_words = len(row)
                if nb_words != 3:
                    raise RuntimeError(f"CP : unexpected record length ({nb_words})")
                Ewe = api.ConvertChannelNumericIntoSingle(row[0], board_type)
                Iwe = api.ConvertChannelNumericIntoSingle(row[1], board_type)
                cycle = row[2]
                #         # compute timestamp in seconds
                t_rel = (t_high << 32) + t_low
                t = current_values.TimeBase * t_rel
                parsed_row = {
                    "time/s": t,
                    "startTime/s": data_info.StartTime,
                    "Ewe/V": Ewe,
                    "I/mA": Iwe,
                    "cycle number": cycle,
                    "Tech": index,
                    "Loop": data_info.loop,
                }
                for var in parsed_row.keys():
                    data_out["CP"][var].append(parsed_row[var])

            elif data_info.TechniqueID == 103:
                inx = ix + data_info.NbCols
                t_high, t_low, *row = data_record[ix:inx]

                nb_words = len(row)
                # if nb_words != 4:
                # raise RuntimeError(f"CV : unexpected record length ({nb_words})")

                if len(row) == 4:
                    Ece = api.ConvertChannelNumericIntoSingle(row[0], board_type)
                    Ewe = api.ConvertChannelNumericIntoSingle(row[2], board_type)
                    Iwe = api.ConvertChannelNumericIntoSingle(row[1], board_type)
                    cycle = row[3]
                else:
                    Ewe = api.ConvertChannelNumericIntoSingle(row[1], board_type)
                    Iwe = api.ConvertChannelNumericIntoSingle(row[0], board_type)
                    cycle = row[2]

                t_rel = (t_high << 32) + t_low
                t = current_values.TimeBase * t_rel
                parsed_row = {
                    "time/s": t,
                    "startTime/s": data_info.StartTime,
                    "Ewe/V": Ewe,
                    "I/mA": Iwe,
                    "cycle number": cycle,
                    "Tech": index,
                }
                if len(row) == 4:
                    parsed_row["Ece/V"] = Ece
                for var in parsed_row.keys():
                    data_out["CV"][var].append(parsed_row[var])

            elif data_info.TechniqueID == 104:
                inx = ix + data_info.NbCols

                # t_high, t_low, *row = data_record[ix:inx]
                row = data_record[ix:inx]

                if data_info.NbCols == 4:
                    t_high, t_low, *row = row
                    Ewe = api.ConvertChannelNumericIntoSingle(row[0], board_type)
                    Iwe = api.ConvertChannelNumericIntoSingle(row[1], board_type)
                    # compute timestamp in seconds
                    t_rel = (t_high << 32) + t_low
                    t = current_values.TimeBase * t_rel
                    parsed_row = {
                        "time/s": t,
                        "startTime/s": data_info.StartTime,
                        "Ewe/V": Ewe,
                        "I/mA": Iwe,
                        "Tech": index,
                        "Loop": data_info.loop,
                    }
                    for var in parsed_row.keys():
                        data_out["PEIS_CA"][var].append(parsed_row[var])
                else:
                    # nb_words = len(row)
                    freq = api.ConvertChannelNumericIntoSingle(row[0], board_type)
                    Eamp = api.ConvertChannelNumericIntoSingle(row[1], board_type)
                    Iamp = api.ConvertChannelNumericIntoSingle(row[2], board_type)
                    phase = api.ConvertChannelNumericIntoSingle(row[3], board_type)
                    time = api.ConvertChannelNumericIntoSingle(row[13], board_type)
                    I = api.ConvertChannelNumericIntoSingle(row[5], board_type)
                    Ewe = api.ConvertChannelNumericIntoSingle(row[4], board_type)
                    Ecamp = api.ConvertChannelNumericIntoSingle(row[7], board_type)
                    Icamp = api.ConvertChannelNumericIntoSingle(row[8], board_type)
                    cphase = api.ConvertChannelNumericIntoSingle(row[9], board_type)
                    Ece = api.ConvertChannelNumericIntoSingle(row[10], board_type)
                    Re = Eamp / Iamp * np.cos(phase)
                    Im = Eamp / Iamp * np.sin(phase)

                    Rec = Ecamp / Icamp * np.cos(cphase)
                    Imc = Ecamp / Icamp * np.sin(cphase)
                    # print(Re,Im)
                    parsed_row = {
                        "time/s": time,
                        "startTime/s": data_info.StartTime,
                        "Ewe/V": Ewe,
                        "Ece/V": Ece,
                        "I/mA": I,
                        "freq/Hz": freq,
                        "Re(Z)/Ohm": Re,
                        "-Im(Z)/Ohm": -Im,
                        "Re(Zce)/Ohm": Rec,
                        "-Im(Zce)/Ohm": -Imc,
                        "Tech": index,
                        "Loop": data_info.loop,
                    }
                    for var in parsed_row.keys():
                        data_out["PEIS"][var].append(parsed_row[var])
            #     else:
            #         # besides the previous 2 known techniques, this is provided
            #         # to show a raw dump of the record
            #         inx = ix + data_info.NbCols
            #         row = data_record[ix:inx]
            #         parsed_row = [f"0x{word:08X}" for word in row]
            ix = inx
    return data_out


def connect_potentiostat(
    address="192.168.0.99",
    channel=1,
    load_firmware=False,
    path=r"D:\Science\Automation\EC-Lab Development Package\lib",
):
    """Connect to a potentiostat using the kbio EcLab API.

    This helper is based on example code delivered together with the kbio
    library. It resolves the EcLib DLL path, connects to the instrument,
    detects the board type, optionally loads firmware, and verifies that the
    channel kernel is loaded. It also prints which .ecc files should be used
    for the detected board type and selected technique family.

    Parameters:
        address (str): Instrument network address. Defaults to "192.168.0.99".
        channel (int): Channel number to connect. Defaults to 1.
        load_firmware (bool): Whether to load firmware after connecting.
        path (str): Default local path to the EcLab library folder.

    Returns:
        tuple: (api, id_) where api is the KBIO_api instance and id_ is the
            device connection identifier.
    """
    binary_path = os.environ.get(
        "ECLIB_DIR",
        path,
    )
    force_load_firmware = True

    if c_is_64b:
        DLL_file = "EClib64.dll"
    else:
        DLL_file = "EClib.dll"

    DLL_path = f"{binary_path}{os.sep}{DLL_file}"

    api = KBIO_api(DLL_path)
    version = api.GetLibVersion()
    print(f"> EcLib version: {version}")
    print()

    # BL_Connect
    id_, device_info = api.Connect(address)
    print(f"> device[{address}] info :")
    print(device_info)
    print()

    # based on board_type, determine firmware filenames
    board_type = api.GetChannelBoardType(id_, channel)
    match board_type:
        case KBIO.BOARD_TYPE.ESSENTIAL.value:
            firmware_path = "kernel.bin"
            fpga_path = "Vmp_ii_0437_a6.xlx"
            print("> Board type detected: ESSENTIAL")
            print("Use technique.ecc files")
        case KBIO.BOARD_TYPE.PREMIUM.value:
            firmware_path = "kernel4.bin"
            fpga_path = "vmp_iv_0395_aa.xlx"
            print("> Board type detected: PREMIUM")
            print("Use technique4.ecc files")
        case KBIO.BOARD_TYPE.DIGICORE.value:
            firmware_path = "kernel.bin"
            fpga_path = ""
            print("> Board type detected: DIGICORE")
            print("Use technique5.ecc files")
        case _:
            print("> Board type detection failed")
            sys.exit(-1)

    if load_firmware:
        # Load firmware
        print(f"> Loading {firmware_path} ...")
        channel_map = api.channel_map({channel})
        api.LoadFirmware(
            id_,
            channel_map,
            firmware=firmware_path,
            fpga=fpga_path,
            force=force_load_firmware,
        )
        print("> ... firmware loaded")
        print()

    # BL_GetChannelInfos
    channel_info = api.GetChannelInfo(id_, channel)
    print(f"> Channel {channel} info :")
    print(channel_info)
    print()

    if not channel_info.is_kernel_loaded:
        print("> kernel must be loaded in order to run the experiment")
        sys.exit(-1)
    print(f"Potentiostat {address} successfully connected! You can load procedures!")
    return api, id_


def plot_results(data_out_all, techniques=["OCV"], index=1):
    """
    Create summary plots for one or more electrochemical technique results.

    Parameters
    ----------
    data_out_all : dict | list[dict]
        Single result dictionary or list of result dictionaries produced by
        ``create_data_out`` / ``get_exp_data``.
    techniques : list[str], optional
        Techniques to include in the plot, such as ``["OCV"]``, ``["CA"]``,
        ``["PEIS"]``, or ``["CV"]``.
    index : int, optional
        Unused plot index placeholder for future multi-panel support.

    Returns
    -------
    matplotlib.figure.Figure
        Figure containing the generated subplot(s).
    """
    if isinstance(data_out_all, dict):
        data_out_all = [data_out_all]

    # Determine which plots to create
    plot_voltage = False  # for voltage vs time (OCV and CP combined)
    plot_current = False  # for current vs time (CA and PEIS combined)
    plot_impedance = False  # for PEIS impedance plot
    plot_cv = False  # current vs voltage for CV

    if "OCV" in techniques or "CP" in techniques or "CV" in techniques:
        plot_voltage = True
    if "CA" in techniques or "PEIS" in techniques:
        plot_current = True
        plot_voltage = True  # CA and PEIS also have voltage vs time
    if "PEIS" in techniques:
        plot_impedance = True
        plot_voltage = True
    if "CV" in techniques:
        plot_cv = True
        plot_voltage = True

    # Count subplots needed
    plots = 0
    if plot_current:
        plots += 1
    if plot_voltage:
        plots += 1
    if plot_impedance:
        plots += 1
    if plot_cv:
        plots += 1
    fig, axes = plt.subplots(1, plots, figsize=(5 * plots, 4))
    # If only one plot, axes is not an array
    if plots == 1:
        axes = [axes]

    cmap = plt.get_cmap("rainbow")
    colors = cmap(np.linspace(0, 1, len(data_out_all)))

    ax_idx = 0

    if plot_current:
        ax = axes[ax_idx]
        for data_out, color in zip(data_out_all, colors):
            # CA current
            if "CA" in techniques and "I/mA" in data_out["CA"]:
                ax.plot(
                    np.array(data_out["CA"]["time/s"])
                    + np.array(data_out["CA"]["startTime/s"]),
                    data_out["CA"]["I/mA"],
                    ":",
                    c=color,
                )
            # PEIS current
            if "PEIS" in techniques and "I/mA" in data_out["PEIS"]:
                ax.plot(
                    data_out["PEIS"]["time/s"], data_out["PEIS"]["I/mA"], "x", c=color
                )
        ax.set_title("Current vs Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Current (mA)")
        ax.set_ylim(bottom=0)
        ax_idx += 1

    if plot_voltage:
        ax = axes[ax_idx]
        for data_out, color in zip(data_out_all, colors):
            # OCV voltage
            if "OCV" in techniques and "Ewe/V" in data_out["OCV"]:
                ax.plot(
                    np.array(data_out["OCV"]["time/s"])
                    + np.array(data_out["OCV"]["startTime/s"]),
                    data_out["OCV"]["Ewe/V"],
                    "-",
                    c=color,
                    label="OCV",
                )
            if "PEIS" in techniques and "Ewe/V" in data_out["PEIS"]:
                ax.plot(
                    data_out["PEIS"]["time/s"],
                    data_out["PEIS"]["Ewe/V"],
                    "-",
                    c=color,
                    label="OCV",
                )
            # CV voltage
            if "CV" in techniques and "Ewe/V" in data_out["CV"]:
                ax.plot(
                    data_out["CV"]["time/s"],
                    data_out["CV"]["Ewe/V"],
                    "-",
                    c=color,
                    label="CV",
                )
            # CP voltage
            if "CP" in techniques and "Ewe/V" in data_out["CP"]:
                ax.plot(
                    np.array(data_out["CP"]["time/s"])
                    + np.array(data_out["CP"]["startTime/s"]),
                    data_out["CP"]["Ewe/V"],
                    "--",
                    c=color,
                    label="CP",
                )
            if "CA" in techniques and "Ewe/V" in data_out["CA"]:
                ax.plot(
                    np.array(data_out["CA"]["time/s"])
                    + np.array(data_out["CA"]["startTime/s"]),
                    data_out["CA"]["Ewe/V"],
                    ":",
                    c=color,
                    label="CA",
                )
        ax.set_title("Voltage vs Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V)")
        ax_idx += 1

    if plot_impedance:
        ax = axes[ax_idx]
        for data_out, color in zip(data_out_all, colors):
            if "PEIS" in techniques:
                ax.plot(
                    data_out["PEIS"]["Re(Z)/Ohm"],
                    data_out["PEIS"]["-Im(Z)/Ohm"],
                    "-",
                    c=color,
                )
        ax.set_title("Impedance")
        ax.set_xlabel("Z' (Ohm)")
        ax.set_ylabel("-Z'' (Ohm)")
        ax.set_aspect("equal")
        ax_idx += 1

    if plot_cv:
        ax = axes[ax_idx]
        for data_out, color in zip(data_out_all, colors):
            if "CV" in techniques:
                if "Ewe/V" in data_out["CV"] and "I/mA" in data_out["CV"]:
                    ax.plot(
                        data_out["CV"]["Ewe/V"], data_out["CV"]["I/mA"], "-", c=color
                    )
        ax.set_title("CV: Current vs Voltage")
        ax.set_xlabel("Voltage (V)")
        ax.set_ylabel("Current (mA)")
        ax_idx += 1

    plt.tight_layout()
    return fig


def create_data_out(techniques, PEIS_time=False):
    data_out = dict()
    if "PEIS" in techniques:
        data_out["PEIS"] = {
            "time/s": [],
            "Ewe/V": [],
            "Ece/V": [],
            "I/mA": [],
            "freq/Hz": [],
            "Re(Z)/Ohm": [],
            "-Im(Z)/Ohm": [],
            "Re(Zce)/Ohm": [],
            "-Im(Zce)/Ohm": [],
            "Loop": [],
            "Tech": [],
            "startTime/s": [],
        }
        if PEIS_time:
            data_out["PEIS_CA"] = {
                "time/s": [],
                "Ewe/V": [],
                "I/mA": [],
                "Loop": [],
                "Tech": [],
                "startTime/s": [],
            }
    if "CA" in techniques:
        data_out["CA"] = {
            "time/s": [],
            "Ewe/V": [],
            "I/mA": [],
            "cycle number": [],
            "Loop": [],
            "Tech": [],
            "startTime/s": [],
        }
    if "CP" in techniques:
        data_out["CP"] = {
            "time/s": [],
            "Ewe/V": [],
            "I/mA": [],
            "cycle number": [],
            "Loop": [],
            "Tech": [],
            "startTime/s": [],
        }
    if "OCV" in techniques:
        data_out["OCV"] = {
            "time/s": [],
            "Ewe/V": [],
            "Ece/V": [],
            "Tech": [],
            "Loop": [],
            "startTime/s": [],
        }
    if "CV" in techniques:
        data_out["CV"] = {
            "time/s": [],
            "Ewe/V": [],
            "Ece/V": [],
            "I/mA": [],
            "cycle number": [],
            "Tech": [],
            "Loop": [],
            "startTime/s": [],
        }

    return data_out


def create_unique_filename(folder_path, base_filename):
    """
    Given a folder path and a base filename, find all files in the folder
    containing the base filename as a substring, extract an index number,
    and create a new filename with an incremented index to avoid overwriting.

    Example:
        base_filename = "measurement"
        existing files: measurement_1.csv, measurement_2.csv
        returns: measurement_3.csv

    Parameters:
        folder_path (str): Path to the folder
        base_filename (str): The base filename to look for in existing files

    Returns:
        str: The full path of the new unique filename
    """
    import re

    if not os.path.isdir(folder_path):
        raise ValueError(
            f"Folder path {folder_path} does not exist or is not a directory"
        )

    # List all files containing base_filename as substring
    existing_files = [
        f
        for f in os.listdir(folder_path)
        if base_filename in f and os.path.isfile(os.path.join(folder_path, f))
    ]

    # Regex pattern to find digits following base_filename and an underscore
    pattern = re.compile(re.escape(base_filename) + r"_([0-9]+)")

    indices = []
    for f in existing_files:
        match = pattern.search(f)
        if match:
            try:
                indices.append(int(match.group(1)))
            except ValueError:
                pass

    # Determine next index
    next_index = max(indices) + 1 if indices else 1

    # Try to preserve file extension from base_filename if any
    base_name, ext = os.path.splitext(base_filename)
    if ext:
        new_filename = f"{base_name}_{next_index}{ext}"
    else:
        # If no extension, try to get extension of the first existing file,
        # or default to .csv
        ext = ".csv"
        if existing_files:
            _, ext_found = os.path.splitext(existing_files[0])
            if ext_found:
                ext = ext_found
        new_filename = f"{base_filename}_{next_index}{ext}"

    return os.path.join(folder_path, new_filename)


def print_matching_files(
    output_folder: str | Path, output_file: str
) -> list[Path]:
    """Print all files in the folder whose names contain the output_file substring.

    Parameters:
        output_folder (str | Path): Folder to search.
        output_file (str): Substring to match inside filenames.

    Returns:
        list[Path]: Paths of matching files.
    """
    output_folder = Path(output_folder)
    if not output_folder.exists() or not output_folder.is_dir():
        raise ValueError(
            f"Folder path {output_folder} does not exist or is not a directory"
        )

    matching_files = [
        path
        for path in output_folder.iterdir()
        if path.is_file() and output_file in path.name
    ]

    if not matching_files:
        print(f"No files found in {output_folder} containing {output_file!r}")
    else:
        print(f"Files in {output_folder} containing {output_file!r}:")
        for path in sorted(matching_files):
            print(path.name)

    # return matching_files


def save_data(
    data_out: dict,
    output_folder: str | Path,
    output_file: str = "",
    *,
    extension: str = ".txt",
    delimiter: str = "\t",
    include_header: bool = True,
    include_index: bool = False,
    mode: str = "a",  # "a" append, "w" overwrite
    encoding: str = "utf-8",
    float_format: str | None = None,
) -> list[Path]:
    """
    Save each entry in data_out to a separate delimited text file.

    Each file name is: {output_file}{key}{extension}

    Parameters
    ----------
    data_out : dict
        Mapping of technique names to row data dictionaries. Each key is used
        to create a separate output file.
    output_folder : str | Path
        Directory where output files will be written. The directory is created
        automatically if it does not exist.
    output_file : str, optional
        Prefix added to each output file name. The default is an empty string.
    extension : str, optional
        File extension to use for output files, such as ".txt" or ".csv".
        A leading dot is added automatically when missing.
    delimiter : str, optional
        Column separator used when writing delimited text files. Defaults to
        a tab character.
    include_header : bool, optional
        Whether to write column headers. If ``mode`` is "a" and the file
        already exists, headers are only written for the first write.
    include_index : bool, optional
        Whether to include the DataFrame index as the first column in the
        output file.
    mode : str, optional
        File write mode. Use "a" to append to existing files or "w" to
        overwrite files.
    encoding : str, optional
        Character encoding used when writing files.
    float_format : str | None, optional
        Format string for floating point numbers, passed through to
        ``pandas.DataFrame.to_csv``.

    Returns
    -------
    list[Path]
        List of Paths for the written output files.
    """
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    if not extension.startswith("."):
        extension = "." + extension

    written_files = []

    for key, value in data_out.items():
        df = pd.DataFrame(value)
        file_out = output_folder / f"{output_file}{key}{extension}"

        file_exists = file_out.exists()
        write_header = include_header and (mode == "w" or not file_exists)

        df.to_csv(
            file_out,
            sep=delimiter,
            mode=mode,
            header=write_header,
            index=include_index,
            encoding=encoding,
            float_format=float_format,
        )

        written_files.append(file_out)

    return written_files
