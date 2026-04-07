## Release checklist

- [ ] An automatic release candidate was generated in format `v{MAJOR.minor.patch}-rc{precandidate N}`.
- [ ] [TeamCity CI pipelines](https://dpcbuild.deltares.nl/project/Koswat_ContinuousIntegration) are successful for all python versions.
- [ ] Release (candidate) is approved
    - If bugs or improvements are found:
        - report them in separate issues,
        - create the __relevant__ issues in separate branches,
        - merge the __required__ issues for releasing back into `main`.
        - a subsequent release candidate bump will be done `v{MAJOR.minor.patch}-rc{precandidate N+1}`.
        - repeat this step until the release candidate is considered as accepted.
- [ ] release branch is updated with the latest changes of `master`.
   - Update your `release/title-for-your-release` branch with `master`.
- Once validation is correct you may proceed to publish the release or release candidate:
    - __Release candidates:__ should be done with a simple "Commit Merge".
        - Make sure that the commit message does not start with `release:`.
        - You can copy & paste the latest commit e.g.: `bump: version 0.17.0rc0 → 0.17.0rc1`.
    - __Releases:__ must be done with a __Squash and merge__ commit.
        - They __must__ follow the format: `{release_type}: {release title}`. 
        - A new tag and release will be made based on the merge commit.
