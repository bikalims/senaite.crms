## senaite.crms

### Overview

`senaite.crms` extends **Senaite** (the modern core of Bika LIMS) with 

It
- Adds a function to send labmanagers emails of looming Reference Sample expiry
- The 'Alert date' can be configured
- Adds Reference Samples item to the Setup

### Requirements

- **Senaite** (recommended latest version) or **Ingwe Bika LIMS 4**

### Installation

#### Using Buildout (Classic Plone/Senaite)

Add the following to your `buildout.cfg`:

cfg
[buildout]
eggs =
    ...
    senaite.crms

Then run:
Bashbin/buildout

#### Docker (Recommended for Ingwe Bika LIMS 4)

Add senaite.crms to your custom add-ons list in the Docker-based Ingwe Bika distribution.

### License
This project is licensed under the GNU General Public License v2.0 (GPL-2.0).

### Support & Professional Services
[Bika Lab Systems](www.bikalabs.com) offers professional implementation, training, custom development, and support for senaite.samplepointlocations.

Website: [https://www.bikalims.org](https://www.bikalims.org)
Email: info@bikalims.org (or contact Lemoene directly)

Made with ❤️ in Cape Town, South Africa
