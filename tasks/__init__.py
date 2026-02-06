from invoke import Collection

from tasks import openapi, routes

# Create the namespace for tasks
ns = Collection()
ns.add_collection(Collection.from_module(routes), name="routes")
ns.add_collection(Collection.from_module(openapi), name="openapi")
