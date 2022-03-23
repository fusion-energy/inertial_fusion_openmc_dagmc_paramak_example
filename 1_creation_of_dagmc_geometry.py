import paramak

# makes a mode of a reactor with a rotation angle of 360 and default parameters elsewhere
# Link to a full list of parameters https://paramak.readthedocs.io/en/main/examples.html#flfsystemcodereactor
my_reactor = paramak.FlfSystemCodeReactor(rotation_angle=360)

# creates a dagmc h5m file of the geometry with material tags automatically assigned
my_reactor.export_dagmc_h5m(filename="dagmc.h5m", min_mesh_size=5, max_mesh_size=20)

# exports the model to a html file that can be opened with an internet browser
my_reactor.export_html_3d(filename="dagmc.html")
