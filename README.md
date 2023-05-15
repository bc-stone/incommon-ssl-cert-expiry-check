# incommon-ssl-cert-expiry-check
### Check the expiration dates of SSL certificates issued by InCommon Certificate Service
This script uses Hashicorp Vault along with a set of environment variables that must be present on the local system for storage and retrieval of secrets such as usernames, API keys, URLs, etc.

This repo contains a custom module entitled 'get_secrets.py' that should help to streamline the auth process somewhat. Details will need to be modified on a per-site basis.

Also in the repo are two additional custom modules named send_email.py and date_format.py.

The main script (ssl_cert_expiry_check.py) will query the InCommon Certificate Service API (using an account with sufficient privileges) for certificates in a specific organization that are due to expire within the next calendar month (length of time to check may be customized in date_format.py.)  Results are sent in tabular format as an email attachment to one or more recpients using a site-specific SMTP server.
