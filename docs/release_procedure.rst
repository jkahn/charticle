Release checklist
-----------------

- Run the :program:`tox` tests.

Land the current version
^^^^^^^^^^^^^^^^^^^^^^^^

- update ``CHANGELOG.rst``

- update ``__version__`` in ``src/charticle/__init__.py``  to have new
  version number.

- run :program:`tox` again.

- commit changes to local git. repo

- :program:`git` tag with current ``v{v}``

- ``git push origin v{v}`` to make sure the tag has shipped to github.

  
Create the next launch version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  
- checkout a new branch named ``v{v+1}.dev``.

- update ``__version__`` in ``charticle/__init__.py`` to ``v{v+1}.dev``
  and ``CHANGELOG.rst`` to ``v{v+1} (unreleased)``.

- commit these changes to the new branch.

- push the new branch to github (``git push --set-upstream origin v{v+1}-dev``).

Ship the tag to PyPI and advance ``master``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :program:`git` ``checkout`` the v{v} tag.

- Ship to PyPI with ``tox -e pypi``

- ``git checkout master && git merge --ff-only v{v}``

- ``git push origin master``

- (:program:`git` checkout the v{v+1}-dev branch again.)
