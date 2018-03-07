Why Enquiries?
==============

It seems like every other question on StackOverflow
is how to deal with user input.
It's usually something like
"I want the user to keep choosing until they choose a valid option."
and the problem is generally something like they're checking

.. code-block:: python

 if user_input == 'yes' or 'Yes':
     # do stuff

and it's always coming back True.
A simple enough mistake for someone new to Python to make.
The answer is generally to convert to lower case and check once
or to check if a set contains the value entered.

Either

.. code-block:: python

   if user_input.lower() == 'yes':
       # do stuff

or

.. code-block:: python

   if user_input in {'yes', 'Yes', 'y'}:
       # do stuff

Then the user has to have some kind of loop so that the user can be asked
repeatedly until an acceptable answer is given.
Both of these solutions will work, and everyone goes on their merry way
until the next quetion comes along.

But what happens if you have a list of things and you want the user to choose one?
This should be a fairly simple task but you end up with another loop and a
whole string of if statements.
Or you introduce a mapping.
Enter '1' for 'Option A' etc.

.. code-block:: python

   options = ['Option A', 'Option B', 'Option C']
   accepted = False
   while not accepted:
       print('Please choose an option')
       for i, opt in enumerate(options, 1):
          print('{}: {}'.format(i, option))
       user_input = input('Choose: ')
       try:
           user_choice = int(user_input)
       except ValueError:
           print('{} is not a valid value'.format(user_input))
           continue
       if not 0 < user_choice <= len(options):
           print('Value {} is not a valid choice'.format(user_choice))
           continue
       else:
           accepted = True
           option = options[user_choice]
   # Use option


Sure it works but you end up with a huge amount of boiler plate.
It's also ugly. If the user enters an incorrect value,
the whole prompt gets printed again.
The choice that the user made is hidden amonst the rest of the output.

After a while of seeing these problems I came across the same problem
in my own code and found myself going through the exact same steps.
Adding the same loops, extracting bits here and there into new functions
and methods that just pushed the problem around without really solving it.
When you want the user to choose one of several things,
you don't want to have to deal with input validation.
There are only <x> things,
just pick one.

That was the next problem. What if they don't have to pick one?
What if you want them to pick 2?
Now you loop from above is embedded in another loop that splits and strips
and converts and is generally doing everything other than the stuff you're
actually trying to do.

*There has to be a better way*

Enter enquiries.

All of the boilerplate is removed - as for any other library -
but also the selection is made interactive.
The end user uses the arrow keys to select from the options.
No typing in choices.
No string matching.
No chains of if/else blocks.

Just pass a list of options and get the chosen option as a return value.

.. code-block:: python

   import enquiries

   options = ['Option A', 'Option B', 'Option C']
   choice = enquiries.choose('Pick an option', options)

The prompt is interactive using the arrow keys to select the option directly.

It is just as easy to choose multiple options from a list as well

Acknowledgments
---------------

This package has very few dependencies, but I would like to thank
Thomas Ballinger both for his excellent
`Curtsies <https://github.com/bpython/curtsies>`_
library that this uses and for his talk on
`Terminal Whispering <https://www.youtube.com/watch?v=rSnMoClPH2E>`_
for explaining the non-standard use of the terminal in a clear way.
