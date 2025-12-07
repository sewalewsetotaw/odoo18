# Odoo

[![Build Status](https://runbot.odoo.com/runbot/badge/flat/1/master.svg)](https://runbot.odoo.com/runbot)
[![Tech Doc](https://img.shields.io/badge/master-docs-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/documentation/master)
[![Help](https://img.shields.io/badge/master-help-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/forum/help-1)
[![Nightly Builds](https://img.shields.io/badge/master-nightly-875A7B.svg?style=flat&colorA=8F8F8F)](https://nightly.odoo.com/)

Odoo is a suite of web based open source business apps.

The main Odoo Apps include an [Open Source CRM](https://www.odoo.com/page/crm),
[Website Builder](https://www.odoo.com/app/website),
[eCommerce](https://www.odoo.com/app/ecommerce),
[Warehouse Management](https://www.odoo.com/app/inventory),
[Project Management](https://www.odoo.com/app/project),
[Billing & Accounting](https://www.odoo.com/app/accounting),
[Point of Sale](https://www.odoo.com/app/point-of-sale-shop),
[Human Resources](https://www.odoo.com/app/employees),
[Marketing](https://www.odoo.com/app/social-marketing),
[Manufacturing](https://www.odoo.com/app/manufacturing),
[...](https://www.odoo.com/)

Odoo Apps can be used as stand-alone applications, but they also integrate seamlessly so you get a full-featured [Open Source ERP](https://www.odoo.com) when you install several Apps.

---

This repository contains **the full Odoo 18 source code**, **the custom modules** along with a **Docker Compose setup** for deployment.

### Included Modules

- **`property_management`**  
  A module for managing properties, tenants, leases, and rent payments.

- **`school_management`**  
  A module for managing schools, students, classes, teachers, attendance, and reports.

### Deployment Configuration

- **`docker-compose.yaml`**  
  Configuration for running Odoo in Docker containers.


---

## Deployment with Docker

To clone and run this project:

    # Clone the repo
    git clone https://github.com/sewalewsetotaw/odoo18.git
    cd odoo18

    # Start Odoo in Docker
    docker-compose up -d


## Access Odoo

Open your browser:

👉 http://localhost:8088

## Install Custom Modules

Inside Odoo:

- Enable **Developer Mode**

- Go to **Apps** → **Update Apps List**

- Search and install:

       - property_management

       - school_management

## Using These Modules in an Existing Odoo Installation

1. Copy the modules into your Odoo custom addons directory:

        cp -r property_management /path/to/odoo/custom/addons/
        cp -r school_management /path/to/odoo/custom/addons/

2. Then in Odoo:

- Enable **Developer Mode**

- Go to **Apps** → **Update Apps List**

- Search and install:

       - property_management

       - school_management
