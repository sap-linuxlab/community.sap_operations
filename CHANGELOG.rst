======================================
Community SAP_OPERATIONS Release Notes
======================================

.. contents:: Topics

v2.0.0
======

Release Summary
---------------

Complete redesign and rework of all Ansible Roles in Collection.

Minor Changes
-------------

- collection - Remove non-SAP roles and obsolete roles (https://github.com/sap-linuxlab/community.sap_operations/pull/43)
- collection - Prepare for release 2.0.0 and housekeeping (https://github.com/sap-linuxlab/community.sap_operations/pull/55)
- sap_profile_update - Complete redesign and rework (https://github.com/sap-linuxlab/community.sap_operations/pull/47)
- sap_control - Complete redesign and rework (https://github.com/sap-linuxlab/community.sap_operations/pull/48)
- sap_hana_backint - Complete redesign and rework (https://github.com/sap-linuxlab/community.sap_operations/pull/50)
- sap_rfc - Deprecate the role and update linting to ignore it (https://github.com/sap-linuxlab/community.sap_operations/pull/51)
- sap_hana_sr_takeover - Complete redesign and rework (https://github.com/sap-linuxlab/community.sap_operations/pull/52)

Bugfixes
--------

- sap_facts - Fix issue 31 by adding restart parameter (https://github.com/sap-linuxlab/community.sap_operations/pull/54)


v1.0.0
======

Release Summary
---------------

Re-release under 1.0.0 to conform with Galaxy version requirements.


v0.9.2
======

Release Summary
---------------

Improvements to sap_control role and various bug fixes.

Minor Changes
-------------

- Stage changes to main by @rainerleber (https://github.com/sap-linuxlab/community.sap_operations/pull/32)

Bugfixes
--------

- sap_facts.sh - ps print only executable with path by @jhohwieler (https://github.com/sap-linuxlab/community.sap_operations/pull/28)
- solution to issue#25 by @crweller (https://github.com/sap-linuxlab/community.sap_operations/pull/27)
- Replace ansible.builtin.pause with ansible.builtin.wait_for by @jhohwieler (https://github.com/sap-linuxlab/community.sap_operations/pull/29)


v0.9.1
======

Release Summary
---------------

Improvements to sap_rfc role and various bug fixes.


v0.9.0
======

Release Summary
---------------

Initial release of the community.sap_operations Ansible Collection.
