
This example simulates a simplfied model of an inertial confinement fusion reactor.
A CAD model is made and automatically converted to a DAGMC geometry that is then used in OpenMC for a neutronics simulation.
The neutronics simulation obtains the tritium breeding ratio and a 3D map of tritium production

-![CAD geometry image](https://github.com/Shimwell/fusion_example_for_openmc_using_paramak/blob/main/reactor.png?raw=true)
-![DAGMC model image](https://github.com/Shimwell/fusion_example_for_openmc_using_paramak/blob/main/reactor.png?raw=true)
-![Mesh Tally result](https://github.com/Shimwell/fusion_example_for_openmc_using_paramak/blob/main/reactor.png?raw=true)


Making the DAGMC model.

First make an environment for the model preparation
```
conda create --name paramak_env python=3.9
conda activate paramak_env
conda install -c fusion-energy -c cadquery -c conda-forge paramak
pip install jupyter_cadquery
```

Then run the script for making the DAGMC model.
```bash
python 1_creation_of_dagmc_geometry.py
```

Optionally you can inspect the DAGMC file at this stage by converting the h5m file to a vtk file and opening this with [Paraview](https://www.paraview.org/)
```
mbconvert dagmc.h5m dagmc.vtk
paraview dagmc.vtk
```


Simulating the model in OpenMC.

First make an environment for simulation.

```
conda create --name openmc_dagmc_env python=3.9
conda activate openmc_dagmc_env
conda install -c conda-forge openmc
pip install openmc_mesh_tally_to_vtk
```

Then run the simulation which will produce a statepoint.10.h5 file that contains the simulation outputs
```bash
python 2_run_openmc_dagmc_simulation.py
```

Then run the post processing script that should output the Tritium Breeding Ratio to the terminal and make a VTK showing the neutron interactions resulting in tritium production
```bash
python 3_extract_results.py
```

Open up the VTK file with paraview
```bash
paraview tritium_production_map.vtk
```
