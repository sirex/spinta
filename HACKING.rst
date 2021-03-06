.. default-role:: literal

Development environment
=======================

You can use docker-compose to run dependant services for spinta development::

   docker-compose up -d

If migrations are not applied, spinta will crash. To launch migrations::

   env/bin/spinta migrate

You can run the app using::

   make run


Diretory tree
=============

::

   spinta/
      config/
         components.py
         commands.py
      backends/
         postgresql/
            commands.py
            services.py
         mongo/
            commands.py
            services.py
         commands.py
         services.py
      manifest/
         components.py
         commands.py
      types/
         components.py
         commands.py
      validation/
         commands.py
      commands.py

Components
==========

Inheritance::

   Store

   Config
   BackendConfig

   Manifest

   Node
      Model
      Project
         ProjectModel
         ProjectProperty
      Dataset
         DatasetModel
         DatasetProperty
      Owner

   Backend
      Python
      PostgreSQL
      MongoDB

   Type
      Integer
      String
      Number
      ForeignKey
      PrimaryKey

   EnvVars

   File
      EnvFile
      CfgFile
      YmlFile


Composition::

   Store

      config                              (Config)

         commands[]                       (str)

         backends
            [default]                     (BackendConfig)
               type                       (str)
               dsn                        (str)

         manifests:
            [default]
               path                       (pathlib.Path)

         ignore[]                         (str)

         debug                            (bool)

      backends
         [backend]                        (Backend)

      manifests
         [ns]                             (Manifest)
            path                          (pathlib.Path)
            objects

               ['model']
                  [object]                (Model)
                     properties
                        [property]        (Property)
                           type           (Type)

               ['project']
                  [object]                (Project)
                     objects
                        [object]          (ProjectModel)
                           properties
                              [property]  (ProjectProperty)

               ['dataset']
                  [object]                (Dataset)
                     objects
                        [object]          (Object)
                           properties
                              [property]  (Property)
                                 type     (Type)

               ['owner']
                  [object]                (Owner)

   Node
      parent                              (Node)
      manifest                            (Manifest)

   Type
      name                                (str)

   EnvVars
      environ

   File
      path


Testing
=======

Authorization
-------------

Here is example how to test endpoints with authorization:


.. code-block:: python

   def test(app):
      app.authorize(['spinta_model_action'])
      resp = app.get('/some/endpoint')
      assert resp.status_code == 200

When `app.authorize` is called, client
`tests/config/clients/baa448a8-205c-4faa-a048-a10e4b32a136.yml` credentials are
are used to create access token and this access token is added as
`Authorization: Bearer {token}` header to all requests.

If `app.authorize` is called without any arguments, scopes are taken from
client YAML file. If scopes are given, then the given scopes are used, even if
client's YAML file does not have those scopes.

Access token is created using `tests/config/keys/private.json` key and
validated using `tests/config/keys/public.json` key.

Additional clients can be created using this command::

   spinta client add -p tests/config/clients

But currently `app.authorize` does not support using another client, currently
only `baa448a8-205c-4faa-a048-a10e4b32a136` is always used, but that can be
easly changed if needed.
