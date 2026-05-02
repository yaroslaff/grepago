# GrepAgo

Grep log files by date in almost any format (e.g. 2h ago, last 1 day)

Currently supported formats are:
- CLF Common Log Format / Combined Log Format (apache2, nginx)
- isoformat first (postfix, syslog)

Example:
~~~
grepago 2d ~/tmp/log/mail/mail.log /var/log/mail/mail.log.1
~~~

will print records from both files for past 2 days from current moment.

### Installation
~~~
pipx install git+https://github.com/yaroslaff/grepago.git
~~~
