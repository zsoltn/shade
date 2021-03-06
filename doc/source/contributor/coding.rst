********************************
Shade Developer Coding Standards
********************************

In the beginning, there were no guidelines. And it was good. But that
didn't last long. As more and more people added more and more code,
we realized that we needed a set of coding standards to make sure that
the shade API at least *attempted* to display some form of consistency.

Thus, these coding standards/guidelines were developed. Note that not
all of shade adheres to these standards just yet. Some older code has
not been updated because we need to maintain backward compatibility.
Some of it just hasn't been changed yet. But be clear, all new code
*must* adhere to these guidelines.

Below are the patterns that we expect Shade developers to follow.

Release Notes
=============

Shade uses `reno <http://docs.openstack.org/developer/reno/>`_ for
managing its release notes. A new release note should be added to
your contribution anytime you add new API calls, fix significant bugs,
add new functionality or parameters to existing API calls, or make any
other significant changes to the code base that we should draw attention
to for the user base.

It is *not* necessary to add release notes for minor fixes, such as
correction of documentation typos, minor code cleanup or reorganization,
or any other change that a user would not notice through normal usage.

API Methods
===========

- When an API call acts on a resource that has both a unique ID and a
  name, that API call should accept either identifier with a name_or_id
  parameter.

- All resources should adhere to the get/list/search interface that
  control retrieval of those resources. E.g., `get_image()`, `list_images()`,
  `search_images()`.

- Resources should have `create_RESOURCE()`, `delete_RESOURCE()`,
  `update_RESOURCE()` API methods (as it makes sense).

- For those methods that should behave differently for omitted or None-valued
  parameters, use the `_utils.valid_kwargs` decorator. Notably: all Neutron
  `update_*` functions.

- Deleting a resource should return True if the delete succeeded, or False
  if the resource was not found.

Exceptions
==========

All underlying client exceptions must be captured and converted to an
`OpenStackCloudException` or one of its derivatives.

REST Calls
============

All interactions with the cloud should be done with direct REST using
the appropriate `keystoneauth1.adapter.Adapter`. See Glance and Swift
calls for examples.

Returned Resources
==================

Complex objects returned to the caller must be a `munch.Munch` type. The
`shade._adapter.Adapter` class makes resources into `munch.Munch`.

All objects should be normalized. It is shade's purpose in life to make
OpenStack consistent for end users, and this means not trusting the clouds
to return consistent objects. There should be a normalize function in
`shade/_normalize.py` that is applied to objects before returning them to
the user. See :doc:`../user/model` for further details on object model requirements.

Fields should not be in the normalization contract if we cannot commit to
providing them to all users.

Fields should be renamed in normalization to be consistent with
the rest of shade. For instance, nothing in shade exposes the legacy OpenStack
concept of "tenant" to a user, but instead uses "project" even if the
cloud uses tenant.

Nova vs. Neutron
================

- Recognize that not all cloud providers support Neutron, so never
  assume it will be present. If a task can be handled by either
  Neutron or Nova, code it to be handled by either.

- For methods that accept either a Nova pool or Neutron network, the
  parameter should just refer to the network, but documentation of it
  should explain about the pool. See: `create_floating_ip()` and
  `available_floating_ip()` methods.

Tests
=====

- New API methods *must* have unit tests!

- New unit tests should only mock at the REST layer using `requests_mock`.
  Any mocking of shade itself or of legacy client libraries should be
  considered legacy and to be avoided.

- Functional tests should be added, when possible.

- In functional tests, always use unique names (for resources that have this
  attribute) and use it for clean up (see next point).

- In functional tests, always define cleanup functions to delete data added
  by your test, should something go wrong. Data removal should be wrapped in
  a try except block and try to delete as many entries added by the test as
  possible.
