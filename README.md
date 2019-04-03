# Boxwise

Boxwise is an open-source web-app,
which makes it easy for organisations
to source, store and distribute
donated goods to people in need
in a fair and dignified way.

This is a new version of [the original Drop App used by Drop In The Ocean](https://www.drapenihavet.no/en/the-drop-app-2/). The [original app](https://bitbucket.org/wishingtree/themarket/src/master/) was limited to just managing a single organization. This is a rewrite to support multiple organizations on a centrally hosted system.

Check out [our webpage](https://www.boxwise.co) for more information!

## Contributing

We are always looking for help. Working on this project is an opportunity to use your skills to help thousands of refugees. [Our contributing guide](CONTRIBUTING.md) has more information.

Please also check out our [Code of Conduct](CODE_OF_CONDUCT.md)!

## Community

[We have a Slack for discussing development and to get support. Join the #dev and #support channel.](https://join.slack.com/t/boxwise/shared_invite/enQtMzE4NzExMjkxNTM2LTk0MzY2Mjg0MTY5ZmJjMjI1ODNmODZiNmJlNTAwM2Y4MmJkZDJjZWEyNzk0YTQyZGI0ZTYxMTc2NTgxNjk1ZTM)

## Setting up development environment

### Install boxwise-doodba

We created [a Boxwise dev-setup](https://github.com/boxwise/boxwise-doodba). It is based on a docker environment for development and production of odoo by Tecnativa. It should just be 5 commands and you are ready to go. You have to have [docker](https://docs.docker.com/install/) and docker-compose installed for this dev-setup.

### Optional settings which still need to be ticked manually

If [Issue #15](https://github.com/boxwise/boxwise_wms/issues/15) is not yet closed then enable the check-boxes related to in the issue in the odoo frontend in the settings / user rights menu by hand.

If you need to print / download pdfs you have to change the system parameter `web.base.url`. Docker is putting a network layer on top. Because of that odoo is assuming the wrong network address of itself and cannot find the pdf converter when you want to download reports. To solve this problem do the following:

    9.1 Run the command (The command only works if the server is running and if you have not renamed the git repo of boxwise-doodba. In that case you have to adjust the name of the odoo docker container in the command.)

        echo http://$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' boxwise-doodba_odoo_1):8069

    9.2 Save the result in the system parameter `ẁeb.base.url` through the odoo interface. Therefore, go to the menu

        Settings / Technical / Parameters / System Parameters

## Where to go from here?

If you want to check out the boxwise frontend - the fancy designs and form - go to

        localhost:11069/

If you want to see all the odoo bits - the odoo backend - go to

        localhost:11069/web?debug

The debug tag opens odoo in developer mode.

## Where to go from here?

If you want to check out the boxwise frontend - the fancy designs and form - go to

        localhost:11069/

If you want to see all the odoo bits - the odoo backend - go to

        localhost:11069/web?debug

## Useful Links

We are using the open source ERP system odoo as the base for Boxwise.

**First, here are some links about odoo itself:**

1. Dev doc:
https://www.odoo.com/documentation/11.0/index.html
2. Dev doc about creating a module:
https://www.odoo.com/documentation/11.0/howtos/backend.html
3. Books:
https://drive.google.com/drive/folders/1AB18OISimJ5jewCBXJuTi6EDVwd84lXW
4. odoo github
https://github.com/odoo
5. odoo code search to find all official modules
http://odoo-code-search.com/

**And the odoo community:**

1. OCA webpage
https://odoo-community.org/
2. OCA Contributing Guidelines
https://odoo-community.org/page/contributing
3. OCA github
https://github.com/OCA
4. OCA maintainer tools
https://github.com/OCA/maintainer-tools
5. OCA maintainer tools wiki
https://github.com/OCA/maintainer-tools/wiki
6. OCA module template
https://github.com/OCA/maintainer-tools/tree/master/template/module

**The odoo JS framework:**

1. Introduction video from odoo conference:
https://www.youtube.com/watch?v=H-iFhOh1tOE
2. JS Dev Doc:
https://www.odoo.com/documentation/11.0/reference/javascript_reference.html
3. JS Command Index:
https://www.odoo.com/documentation/11.0/reference/javascript_api.html
4. JS Quick ref:
https://www.odoo.com/documentation/11.0/reference/javascript_cheatsheet.html
