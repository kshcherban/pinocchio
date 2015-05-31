# pinocchio
r10k lightweight analogue

Script will populate your puppet modules directory with modules specified in puppetfile.  
Can get modules only from git repositories.  

## Usage

Create puppetfile with puppet modules configuration inside /etc/puppet/modules/

```
cdh4:
    git: github.com:kshcherban/puppet-cdh4
    ref: centos
wordpress:
    git: https://github.com:puppetlabs/puppetlabs-stdlib
    ref: master
dummy:
    git: git@bitbucket.org:kshcherban/dummy.git
    ref: private
```

Then run pinocchio
```
pinocchio.py /etc/puppet/modules/puppetfile.yaml
May 31 14:49:47 INFO: Cloning dummy into /etc/puppet/modules/dummy from git@bitbucket.org:kshcherban/dummy.git/private
May 31 14:49:47 INFO: Cloning wordpress into /etc/puppet/modules/wordpress from https://github.com:puppetlabs/puppetlabs-stdlib/master
May 31 14:49:47 INFO: Cloning cdh4 into /etc/puppet/modules/cdh4 from github.com:kshcherban/puppet-cdh4/centos
```

That's it. If you want to pull new changes to already cloned modules just rerun script.  
By default pinocchio uses 24 threds, if you want to change it, specify **-p** parameter.
