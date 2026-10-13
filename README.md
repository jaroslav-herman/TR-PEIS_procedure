# TR-PEIS procedure

Python notebook and helper package for measuring **time-resolved potentiodynamic
electrochemical impedance spectroscopy (TR-PEIS)** with Bio-Logic potentiostats.

Conventional EIS requires the system to remain stationary during the measurement,
which prevents its use for transient phenomena. The TR-PEIS procedure overcomes
this by recording individual isofrequency responses during repeated transient
events, each initiated from the same state. Interpolating these responses
reconstructs instantaneous impedance spectra with (sub-second) temporal
resolution, which can then be analyzed with standard EIS methods (distribution
of relaxation times, equivalent circuit fitting) while providing direct access
to the temporal evolution of the individual electrochemical processes.

The method is described in:

> Herman, J., Bouzek, K., Paušová, Š. — *Beyond Steady-State Limitations of
> Electrochemical Impedance Spectroscopy: Time-Resolved Decoupling of Transient
> Processes*
> Preprint: [10.5281/zenodo.22961107](https://doi.org/10.5281/zenodo.22961107)

The accompanying dataset is available at
[10.5281/zenodo.22961027](https://doi.org/10.5281/zenodo.22961027)
(currently under embargo, public release on October 1, 2028).

## Repository contents

| File / folder | Description |
| --- | --- |
| `TR-PEIS_procedure.ipynb` | Jupyter notebook that runs the full TR-PEIS experiment |
| `kbio_tr-peis/` | `kbio-tr-peis` Python package (imported as `kbio`) used by the notebook |
| `EC-Lab Development Package.pdf` | Bio-Logic EcLib API documentation |

## Requirements

- Windows (the Bio-Logic EcLib API is loaded from a Windows DLL,
  `EClib64.dll` for 64-bit Python or `EClib.dll` for 32-bit Python)
- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A Bio-Logic **EC-Lab Development Package** installation (the `lib` folder
  containing the EcLib DLL, firmware `kernel*.bin`/FPGA files, and the
  `.ecc` technique files)
- A Bio-Logic potentiostat reachable over the network (e.g. VMP3, SP- series)
- The appropriate `.ecc` technique files for your board type: `ocv.ecc`,
  `ca.ecc`, `peis.ecc`, and `loop.ecc` (or their `technique4.ecc` /
  `technique5.ecc` variants — the notebook prints the recommended set after
  connecting)

## Install with uv

From the repository root, run:

```powershell
uv sync
```

This creates a project environment, installs the local `kbio-tr-peis`
package (imported as `kbio`) and its notebook dependencies, and writes/updates
`uv.lock`.

Verify the installation without connecting to hardware:

```powershell
uv run python -c "import kbio.kbio_run, kbio.kbio_run_techniques; print('kbio import OK')"
```

Start Jupyter in that environment with:

```powershell
uv run jupyter notebook TR-PEIS_procedure.ipynb
```

Alternatively, register the environment as a Jupyter kernel:

```powershell
uv run python -m ipykernel install --user --name tr-peis --display-name "Python (TR-PEIS)"
```

Then select **Python (TR-PEIS)** in Jupyter.

## Configure EC-Lab

The notebook loads the EcLib DLL either from the `ECLIB_DIR` environment
variable or from the `path` argument of `connect_potentiostat()`. Set
`ECLIB_DIR` to the `lib` directory of your EC-Lab Development Package
installation before starting the notebook:

```powershell
$env:ECLIB_DIR = "C:\Path\To\EC-Lab Development Package\lib"
uv run jupyter notebook TR-PEIS_procedure.ipynb
```

The instrument must be connected to the network and switched on. The `.ecc`
technique files must be reachable by EC-Lab (they are resolved relative to the
DLL/lib directory).

## How to use the notebook

Run the cells top to bottom. Each step prints status information so you can
confirm the instrument state before continuing. The workflow is:

1. **Imports** – loads the `kbio` package helpers, NumPy, matplotlib and
   ipywidgets. No hardware connection happens here.

2. **Connect to the potentiostat** – set `address` (instrument IP) and
   `channel`, then call `connect_potentiostat()`. This loads the EcLab DLL,
   connects to the instrument, detects the board type, prints which `.ecc`
   files should be used for the detected board, optionally loads firmware
   (`load_firmware=True`), and checks that the channel kernel is loaded.
   The returned `api` object is used by all following cells.

3. **Define the experiment parameters**:
   - `voltage` – target cell voltage of the transient event
   - `voltage_time` – hold time at the set voltage for both CA and PEIS
   - `ocv_time` – open-circuit hold time used between CA and PEIS
   - `points_per_decade`, `f_start`, `f_end` – PEIS frequency sweep settings
     (one isofrequency PEIS run per frequency in `f_list`)
   - `randomize` – optionally shuffle the frequency order to avoid systematic
     sweep-ordering effects
   - `repeats` – maximum number of initial OCV/CA stabilization cycles
   - `stabilization_range` – relative current change (in %) between two
     subsequent cycles below which the system is considered stable
   - The technique parameter objects (`ca_params`, `ocv_params`, `peis_params`,
     `loop_params`) are created here and passed to the instrument API.

4. **Set output paths** – `output_folder` and the `output_file` base name
   (built automatically from voltage/timing parameters). The cell prints any
   existing files matching the base name so you can avoid overwriting previous
   measurements; `create_unique_filename()` appends a suffix when needed.

5. **Initial stabilization loops** – runs OCV/CA cycles and plots live data.
   The loop continues until the current stabilizes within
   `stabilization_range` or `repeats` cycles are reached. Data from the
   stabilization phase is saved separately (`..._init` files).

6. **TR-PEIS measurement** – for each frequency in `f_list`, a full
   transient event (OCV → voltage step → PEIS at that single frequency) is
   executed and the isofrequency response is recorded. Live plots track the
   progress; a warning widget signals instrument issues.

7. **Export** – the collected data are saved as tab-delimited text files
   (one per technique) in `output_folder` via `kbio.kbio_run.save_data()`,
   ready for post-processing (interpolation to instantaneous spectra, DRT,
   equivalent circuit fitting).

Importing the package does not connect to hardware. The notebook connects
only when the connection cell is executed, and drives the instrument only when
the stabilization/measurement cells are executed.

### Tips

- Review all experiment parameters (cell 3) before starting: the measurement
  cells start the instrument immediately.
- Check the printed board type and use the matching `.ecc` file set
  (`technique.ecc`/`technique4.ecc`/`technique5.ecc` families).
- If the connection fails, verify `ECLIB_DIR`, the instrument IP address, and
  that the channel kernel is loaded (load firmware with `load_firmware=True`
  on a freshly powered instrument).
- Output files append by default; change the `output_file` base name or use
  `create_unique_filename()` for a new experiment.

## License note

Some files in `kbio_tr-peis` originate from the Bio-Logic OEM package and are
subject to the OEM Package licence. Use and redistribute them only as allowed
by that licence.

## Funding

This publication was supported by the project “The Energy Conversion and
Storage,” funded as project No. CZ.02.01.01/00/22_008/0004617 by the Programme
Johannes Amos Comenius, call Excellent Research. JH acknowledges financial
support from the Grant Agency of Charles University in Prague (GAUK No. 333225)
and CERIC AEMWE project.
