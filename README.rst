==============
instagram_auth
==============

instagram_auth is a Django authentication backend

TODO Detailed documentation is at readthedocs.org.

Quick start
-----------

1. add ``instagram_auth`` to your ``INSTALLED_APPS`` setting like this

.. code-block::

  INSTALLED_APPS = [
      ...
      'instagram_auth',
  ]

2. Include instagram_auth URLconf in your project urls.py like this

.. code-block::

  url(r'^accounts/', include(instagram_auth.urls)),

3. Run ``python manage.py migrate`` to create instagram_auth models




