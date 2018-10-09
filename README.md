# eduroam-test-web-based
Code for eduroam test via web based service

It is a service which emulates user connecting to the access point connected to the eduroam (http://eduroam.org) infrastructure. You can use your test accounts to test wheter your users will be able to authenticate with eduroam outside your institution.

## Requirement

* You have to your local RADIUS server connected to the eduroam.

## Instalation

* Store the script to /usr/lib/cgi-bin/
* Enable CGI scripts in Apache web server
* Configure apache to poin to the eduroam-test.cgi script, e.g.:

```
   ScriptAlias /eduroam-test/ /usr/lib/cgi-bin/
   <Directory /usr/lib/cgi-bin/>
	Options -Indexes -FollowSymLinks +ExecCGI
	Order allow,deny
	Allow from all

	SetHandler cgi-script
   </Directory>
```

* Configure RADIUS server IP and shared secret in the script

## Usage

* Just go to https://<your machine>/eduroam-test/eduroam-test.cgi
