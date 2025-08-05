# Needy

## inspiration

needy is an experiment about bringing together ideas from various di systems in python

key inspirations are

* pytest fixtures
* dishka
* svc
* morepath
* zope and the surrouding ecosystem
* fastapi

## intended features

* declarations of services/resources and their lifecycles
* scopes and their interactions (testing lifecycles vs application lifecylces - and interplay)
* parameterization and versatile mechanisms of keeping things alive (pytest parametrize with less teardown)
* sync/async usage -> async code, sync outside useage (any dependency that dynamically requests another should be ableto do that async as to ensure control is yielded to the system when obtaining another dependency)
* multiple resolvers/mechanisms to provide dependencies
  * svcs is the key example for something that explicitly avoids injection
  * fastapi/dishka use types and annotations to configure the resolution
  * pytest uses names and parameter values
  