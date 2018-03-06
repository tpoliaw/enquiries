Quickstart
==========

Before you start
----------------

Requirements
~~~~~~~~~~~~

Enquiries requires Python 3. Python 2 is not supported and there are no
plans for it to be.

It also requires the curses library so is restricted to POSIX systems.

Installation
~~~~~~~~~~~~
Installation via ``pip`` is easiest.


.. code-block:: shell

    pip install enquiries
    # or
    python -m pip install enquiries


.. note::

    According to `this tweet <https://twitter.com/raymondh/status/968634031842603008>`_
    (a core Python developer)

    ``python -m pip install enquiries``

    Can be more reliable as it ensures you are installing to the correct python
    version

To install directly from source (to get nightly/master versions)

.. code-block:: shell

   python -m pip install git+https://gitlab.com/facingBackwards/enquiries.git#egg=enquiries

----


Usage
-----

Enquiries is a very simple package currently containing only three functions.

.. code-block:: python

   >>> import enquiries
   >>> dir(enquiries)
   # ignoring __private__ attributes
   ['choose', 'confirm', 'freetext']

Multiple Choice
~~~~~~~~~~~~~~~

Multiple choice is offered through the ``choose`` method.

.. code-block:: python

   >>> options = ['Option %d' %i for i in range(10)]
   >>> choice = choose('Prompt for the user', options)
   >>> print (choice)
   Option 3
   >>>

No awkward loops, no boilerplate or validation, just clear and expressive.
The prompt appears and is then cleared after the selection has been made
keeping the terminal clear.

There are also keyword arguments to enable accepting multiple options,
to pass alternative display values etc

Confirm
~~~~~~~

Getting a True/False value is available from the ``confirm`` choice

.. code-block:: python

   >>> proceed = confirm('Do you want to do the thing?')
   >>> print(proceed)
   True
   >>>

Additional settings are available to change the keys for yes/no,
set the default choice etc.

Freetext
~~~~~~~~

Freetext input is available through the ``freetext`` function.
This method is an extension of the builtin ``input`` method.

There is no validation done on the text but it adds basic readline
type controls, ``Ctrl-a``, ``Ctrl-e`` etc.

.. code-block:: python

   >>> user_input = freetext('Enter some text')

