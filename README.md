# TR-PEIS procedure

This repository contains the `TR-PEIS_procedure.ipynb` notebook and the
`kbio-tr-peis` Python package used by it. The package is installed as `kbio`,
which is the import name used throughout the notebook.

## Requirements

- Windows (the Bio-Logic EcLib API uses the Windows DLL loader)
- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A Bio-Logic EcLab Development Package installation, including `EClib64.dll`
  (or `EClib.dll` for 32-bit Python)
- Access to the potentiostat and the required `.ecc` technique files

## Install with uv

From the repository root, run:

```powershell
uv sync
```

This creates a project environment, installs the local package and its
notebook dependencies, and writes/updates `uv.lock`.

Start Jupyter in that environment with:

```powershell
uv run jupyter notebook TR-PEIS_procedure.ipynb
```

Alternatively, register the environment as a Jupyter kernel:

```powershell
uv run python -m ipykernel install --user --name tr-peis --display-name "Python (TR-PEIS)"
```

Then select **Python (TR-PEIS)** in Jupyter.

## Configure EcLab

Set `ECLIB_DIR` to the directory containing the EcLab DLL before starting the
notebook. For example:

```powershell
$env:ECLIB_DIR = "C:\Path\To\EcLab Development Package\lib"
uv run jupyter notebook TR-PEIS_procedure.ipynb
```

The notebook also contains experiment-specific settings such as the
potentiostat address, output folder, voltage and timing parameters. Review
these values before running an experiment. The instrument must be connected,
and the appropriate `.ecc` files must be available to EcLab.

## Verify the installation

```powershell
uv run python -c "import kbio.kbio_run, kbio.kbio_run_techniques; print('kbio import OK')"
```

Importing the package does not connect to hardware. The notebook connects only
when its connection cell is executed.

## License note

Some files in `kbio-tr-peis` originate from the Bio-Logic OEM package and are
subject to the OEM Package licence. Use and redistribute them only as allowed
by that licence.
