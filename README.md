# University of Waterloo Git Site

This site is based off the Django framework using Python 3.

## Gitolite

1. Add `LOCAL_CODE => "$rc{GL_ADMIN_BASE}/local",` to the rc file.
2. Add `POST_COMPILE => ['django'],` to the rc file.
3. Add `POST_CREATE => ['django'],` to the rc file.
4. Add `local/hooks/common/post_receive`, it should call the `gitolitehook`
   command.
5. Add `local/triggers/django`, it should call the `gitolitetrigger` command.
6. Add `include "django/*.conf"` to to `conf/gitolite.conf`.

Below is an example script to call the `gitolitehook` command.

    #!/bin/bash
    python /srv/git/site/manage.py gitolitehook $@

## CAS

The CAS module based off [django-cas](https://bitbucket.org/cpcc/django-cas/).
This code is licensed under an MIT license. It is currently up-to-date with
`47d19f3a871fa744dabe884758f90fff6ba135d5`.

## License

Except where noted, all code is licensed under GPL v3.
