Contributing Checklist 
======================

Any kind of contribution is welcome. You can test the package, improve the documentation, add new features, fix bugs, and many more. For the current list of feature requests and bugs, please refer to the `issues page <https://gitlab-int.rc.fas.harvard.edu/rse/francesca_dominici/tools/getcensus/-/issues>`_ .

Here are the general steps to consider in contribution.

**Step 1**: Get a copy of the project or update your local repo and start a new branch

.. code-block:: console

    git clone https://gitlab-int.rc.fas.harvard.edu/rse/francesca_dominici/tools/getcensus.git

or if you already have the code, update your directory. It is very important to keep your local directory updated by the ``dev`` branch.  

.. code-block:: console

    git fetch --all
    git checkout origin/dev
    git pull
    git checkout -b new_branch

**Step 2**: Make modifications

In this step, you can choose a topic to contribute to and work on it. However, please make sure that you are working on one specific topic. For example, if you are working on polishing documentation, we do not expect to see any changes to the codebase. Mixing features make the review process extremely time-consuming.  It is acceptable to add or modify documents when you are adding new functionality to the code. However, those changes should be related only to that feature.

**Step 3**: Run unit tests (and doc test)

Make sure that your package passes all tests. [TODO: needs more details.]

**Step 4**: Update CHANGELOG.md

You need to update CHANGELOG.md file and add any required information to understand what has happened. 

**Step 5**: Submit a merge request

Please submit all merge requests to ``dev`` branch. The ``dev`` branch has the most recent implemented code. Please keep an eye on the ``dev`` branch and update your local branch accordingly. 


.. note::

    You can submit Merge Request earlier before completely finishing the implementation. This helps you get feedback from the group and run your code through CI to ensure that you are on the right path. 
