import openmc
from openmc_mesh_tally_to_vtk import write_mesh_tally_to_vtk


# open the results file
sp = openmc.StatePoint('statepoint.10.h5')

# access the tally using pandas dataframes
tbr_tally = sp.get_tally(name='TBR')
df = tbr_tally.get_pandas_dataframe()

tbr_tally_result = df['mean'].sum()
tbr_tally_std_dev = df['std. dev.'].sum()

# print results
print('The tritium breeding ratio was found, TBR = ', tbr_tally_result)
print('Standard deviation on the tbr tally is ', tbr_tally_std_dev)

tbr_mesh_tally = sp.get_tally(name='tbr_on_mesh')

write_mesh_tally_to_vtk(
    tally=tbr_mesh_tally,
    filename = "vtk_file_from_openmc_mesh.vtk",
)