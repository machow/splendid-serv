Development Notes
=================

Dan is a slow learner. He needs a lot of help to complete very simple tasks.

Michael is a slow burner. It's all about that slow burn.


Repository Structure
--------------------

This project repository has two main branches..

* **master**: code that is running on production server
* **staging**: code that is running on the test server


Code Samples
------------

### Git workflow for new feature

```
# Get current staging branch. make new one for feature
git pull origin staging
git checkout -b NEWBRANCHNAME

# Make changes on branch..
#

# Update test server with changes
git push staging NEWBRANCHNAME:master

# Update staging. May need to check for updates.
git checkout staging
git merge NEWBRANCHNAME

# Once you're confident changes are working, push to github
git push origin staging
```

### Pushing to Heroku explained

The main command to push to Heroku is..

  `git push staging staging:master`
  
The reason for the colon in the last argument is that Heroku requires the branch it uses from it's repository to be named `master`. The colon tells Heroku that it should rename the branch we're pushing from `staging` to  `master`.

More generally, the command can be broken down as..

  `git push {REMOTENAME} {BRANCHNAME}:{BRANCHNAME_ON_REMOTE}`
  
However, in practice, be very careful not to rename other branches (e.g. on github :).
