.. _security_policy_for_bugs:

========================
Security policy for bugs
========================

Receiving Security Updates 
========================== 

The Pylons team have set up a mailing list at wsgi-security-announce@googlegroups.com to which any security vulnerabilities that affect Pylons will be announced. Anyone wishing to be notified of vulnerabilities in Pylons should subscribe to this list. Security announcements will only be made once a solution to the problem has been discovered. 

Reporting Security Issues 
========================= 

Please report security issues by email to both the lead developers of Pylons at the following addresses: 

ben\ 
|at|\ 
groovie.org 

security\ 
|at|\ 
3aims.com 

Please DO NOT announce the vulnerability to any mailing lists or on the ticket system because we would not want any malicious person to be aware of the problem before a solution is available. 

In the event of a confirmed vulnerability in Pylons itself, we will take the following actions: 

* Acknowledge to the reporter that we've received the report and that a fix is forthcoming. We'll give a rough timeline and ask the reporter to keep the issue confidential until we announce it. 
* Halt all other development as long as is needed to develop a fix, including patches against the current release. 
* Publicly announce the vulnerability and the fix as soon as it is available to the WSGI security list at wsgi-security-announce@googlegroups.com. 

This will probably mean a new release of Pylons, but in some cases it may simply be the release of documentation explaining how to avoid the vulnerability. 

In the event of a confirmed vulnerability in one of the components that Pylons uses, we will take the following actions: 

* Acknowledge to the reporter that we've received the report and ask the reporter to keep the issue confidential until we announce it. 
* Contact the developer or maintainer of the package containing the vulnerability. 
* If the developer or maintainer fails to release a new version in a reasonable time-scale and the vulnerability is serious we will either create documentation explaining how to avoid the problem or as a last resort, create a patched version. 
* Publicly announce the vulnerability and the fix as soon as it is available to the WSGI security list at wsgi-security-announce@googlegroups.com. 

Minimising Risk 
=============== 

* Only use official production versions of Pylons released publicly on the `Python Package Index <http://python.org/pypi>`_. 
* Only use stable releases of third party software not development, alpha, beta or release candidate code. 
* Do not assume that related software is of the same quality as Pylons itself, even if Pylons users frequently make use of it. 
* Subscribe to the wsgi-security-announce@googlegroups.com mailing list to be informed of security issues and their solutions. 

.. |at| image:: _static/at.png 
