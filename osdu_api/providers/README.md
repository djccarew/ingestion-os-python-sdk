Providers folder structure.
```
providers
│   README.md
│   {blob_storage, ..., types}.py   
│
└───gcp
│   │   gcp_blob_storage_client.py
│   │   ...
│   
└───aws
    │   ...
```
In the base folder there are the following base classes:
`types.py`: Stores all the interfaces that could be implemented by cloud providers.
`factory.py` Provides a mechanism to register and retrieve cloud specific implementations using a class decorator @ProviderFactory.register. A registry per interface is required, if a new interface is implemented a new registry should be added.
`constants.py` Reusable constants.
`exceptions.py` Provider specific exceptions should be thrown here and bubble up all the way up.
All interfaces will require a **wrapper module** that registers specific implementations and provides a factory method. Examples of wrapper modules are: `blob_storage.py` and `credentials.py`. Please pay attention to the import section as it's required that all modules that implement an interface to be imported here so they can be registered.

Adding a new implementation.
1. Create a module (e.g., gcp_blob_storage_client.py) under the cloud provider subfolder. Within the module, create a class that inherits from given base interface and decorate it with @ProviderFactory.register(`CLOUD_PROVIDER_NAME_CONSTANT`)
2. Add an import in the **wrapper module** of the interface (e.g., blob_storage.py -> from providerds.gcp.gcp_blob_storage_client.py) to register the new implementation. You may optionally modify the factory method if the initialization of the new implemented class needs some customatization. Just don't bubble up customatization as factory method should be transparent for all clients.

Adding a new interface.
1. Add interface to types.py.
2. Add a new registry to ProvidersFactory.py and modify register logic to take into account new type. Add a new get method for the new type.
3. Add the new implementation.

