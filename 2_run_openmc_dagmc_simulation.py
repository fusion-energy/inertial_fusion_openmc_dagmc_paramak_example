import openmc
import openmc_data_downloader as odd


# Names of material tags can be found with the command line tool
# mbsize -ll dagmc.h5m | grep 'NAME = mat:'

mat_vacuum_vessel = openmc.Material(name="vacuum_vessel")
mat_vacuum_vessel.add_element("Fe", 1, "ao")
mat_vacuum_vessel.set_density("g/cm3", 7.7)

mat_upper_blanket = openmc.Material(name="upper_blanket")
mat_upper_blanket.add_element("Li", 1, "ao")
mat_upper_blanket.set_density("g/cm3", 0.5)

mat_lower_blanket = openmc.Material(name="lower_blanket")
mat_lower_blanket.add_element("Li", 1, "ao")
mat_lower_blanket.set_density("g/cm3", 0.5)

mat_lower_vacuum_vessel = openmc.Material(name="lower_vacuum_vessel")
mat_lower_vacuum_vessel.add_element("Fe", 1, "ao")
mat_lower_vacuum_vessel.set_density("g/cm3", 7.7)

mat_upper_vacuum_vessel = openmc.Material(name="upper_vacuum_vessel")
mat_upper_vacuum_vessel.add_element("Fe", 1, "ao")
mat_upper_vacuum_vessel.set_density("g/cm3", 7.7)

mat_blanket = openmc.Material(name="blanket")
mat_blanket.add_element("Li", 1, "ao")
mat_blanket.set_density("g/cm3", 0.5)

materials = openmc.Materials(
    [
        mat_vacuum_vessel,
        mat_upper_blanket,
        mat_lower_blanket,
        mat_lower_vacuum_vessel,
        mat_upper_vacuum_vessel,
        mat_blanket,
    ]
)

#downloads the nuclear data and sets the openmc_cross_sections environmental variable
odd.just_in_time_library_generator(
    libraries='ENDFB-7.1-NNDC',
    materials=materials
)

# makes use of the dagmc geometry
dag_univ = openmc.DAGMCUniverse("dagmc.h5m")

# creates an edge of universe boundary
vac_surf = openmc.Sphere(r=10000, surface_id=9999, boundary_type="vacuum")

# specifies the region as below the universe boundary
region = -vac_surf

# creates a cell from the region and fills the cell with the dagmc geometry
containing_cell = openmc.Cell(cell_id=9999, region=region, fill=dag_univ)

geometry = openmc.Geometry(root=[containing_cell])

# creates a simple isotropic neutron source in the center with 14MeV neutrons
my_source = openmc.Source()
my_source.space = openmc.stats.Point((0, 0, 0))
my_source.angle = openmc.stats.Isotropic()
my_source.energy = openmc.stats.Discrete([14e6], [1])

# specifies the simulation computational intensity
settings = openmc.Settings()
settings.batches = 10
settings.particles = 100000
settings.inactive = 0
settings.run_mode = "fixed source"
settings.source = my_source

# adds a tally to record the number of tritium producing reactions in cells containing the blanket material
cell_tally = openmc.Tally(name="TBR")
cell_tally.scores = [
    "(n,Xt)"
]  # this catch all neutron induced tritium producing reactions
cell_tally.filters = [openmc.MaterialFilter(mat_blanket)]

# creates a mesh that covers the geometry
mesh = openmc.RegularMesh()
mesh.dimension = [100, 100, 100]
mesh.lower_left = [-200, -200, -300]  # x,y,z coordinates
mesh.upper_right = [200, 200, 300]  # x,y,z coordinates

# makes a mesh tally using the previously created mesh and records tritium production on the mesh
mesh_tally = openmc.Tally(name="tbr_on_mesh")
mesh_filter = openmc.MeshFilter(mesh)
mesh_tally.filters = [mesh_filter]
mesh_tally.scores = ["(n,Xt)"]

# groups the two tallies
tallies = openmc.Tallies([cell_tally, mesh_tally])

# builds the openmc model
my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)

# starts the simulation
statepoint_file = my_model.run()
