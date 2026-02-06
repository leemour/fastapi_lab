from invoke import Collection

from tasks import routes

# Create the namespace for tasks
ns = Collection()
ns.add_collection(Collection.from_module(routes), name="routes")
