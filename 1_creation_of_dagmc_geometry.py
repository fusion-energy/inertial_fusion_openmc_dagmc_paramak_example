import paramak

# makes a mode of a submersion tokamak with default parameters
my_reactor = paramak.FlfSystemCodeReactor(rotation_angle=360)

# creates a dagmc geometry of the geometry.
my_reactor.export_dagmc_h5m(
    filename="dagmc.h5m", min_mesh_size=5, max_mesh_size=20
)

my_reactor.export_html_3d(filename="dagmc.html")