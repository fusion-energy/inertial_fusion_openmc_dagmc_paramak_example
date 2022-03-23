import openmc
import math

# Names of material tags can be found with the command line tool
# mbsize -ll dagmc.h5m | grep 'NAME = mat:'


mat_vacuum_vessel = openmc.Material(name="mat_vacuum_vessel")
mat_vacuum_vessel.add_element("Fe", 1, "ao")
mat_vacuum_vessel.set_density("g/cm3", 7.7)

mat_upper_blanket = openmc.Material(name="mat_upper_blanket")
mat_upper_blanket.add_element("Li", 1, "ao")
mat_upper_blanket.set_density("g/cm3", 0.5)

mat_lower_blanket = openmc.Material(name="mat_lower_blanket")
mat_lower_blanket.add_element("Li", 1, "ao")
mat_lower_blanket.set_density("g/cm3", 0.5)

mat_lower_vacuum_vessel = openmc.Material(name="mat_lower_vacuum_vessel")
mat_lower_vacuum_vessel.add_element("Fe", 1, "ao")
mat_lower_vacuum_vessel.set_density("g/cm3", 7.7)

mat_upper_vacuum_vessel = openmc.Material(name="mat_upper_vacuum_vessel")
mat_upper_vacuum_vessel.add_element("Fe", 1, "ao")
mat_upper_vacuum_vessel.set_density("g/cm3", 7.7)

mat_blanket = openmc.Material(name="mat_blanket")
mat_blanket.add_element("Li", 1, "ao")
mat_blanket.set_density("g/cm3", 0.5)

materials = openmc.Materials(
    [
        mat_vacuum_vessel,
        mat_upper_blanket,
        mat_lower_blanket,
        mat_lower_vacuum_vessel,
        mat_upper_vacuum_vessel,
        mat_blanket
    ]
)

dag_univ = openmc.DAGMCUniverse("dagmc.h5m")

vac_surf = openmc.Sphere(r=10000, surface_id=9999, boundary_type="vacuum")

region = -vac_surf

containing_cell = openmc.Cell(cell_id=9999, region=region, fill=dag_univ)
geometry = openmc.Geometry(root=[containing_cell])

my_source = openmc.Source()
my_source.space = openmc.stats.Point((0, 0, 0))
my_source.angle = openmc.stats.Isotropic()
my_source.energy = openmc.stats.Discrete([14e6], [1])

settings = openmc.Settings()
settings.batches = 10
settings.inactive = 0
settings.particles = 100000
settings.run_mode = "fixed source"
settings.source = my_source

tally = openmc.Tally(name="TBR")
tally.scores = ["(n,Xt)"]  # this catch all neutron induced tritium producing reactions
tally.filters = [openmc.MaterialFilter(mat_blanket)]

mesh = openmc.RegularMesh()
mesh.dimension = [100, 100, 100]
mesh.lower_left = [-200, -200, -300]  # x,y,z coordinates
mesh.upper_right = [200, 200, 300]  # x,y,z coordinates

mesh_filter = openmc.MeshFilter(mesh)
mesh_tally = openmc.Tally(name='tbr_on_mesh')
mesh_tally.filters = [mesh_filter]
mesh_tally.scores = ['(n,Xt)']

tallies = openmc.Tallies([tally, mesh_tally])

my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)

statepoint_file = my_model.run()
