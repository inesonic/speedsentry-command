======================================
Inesonic SpeedSentry Command Line Tool
======================================
The Inesonic SpeedSentry Command Line Tool is a small suite of Python
scripts you can use to control the SpeedSentry backend infrastructure.  The
command line tool includes a large selection of sub-commands.

You can use the ``--help`` switch to obtain basic help.  You can use the
``help`` command to obtain detailed help on specific sub-commands.

The tool expects a file called `.speedsentry_config.json` in your home
directory which contains secrets needed to control the SpeedSentry DBC.

This project also includes a ``rebalance`` script used to rebalance loading
between polling servers as well as a ``rollup_requester`` script used to
trigger rollup emails using a rollup server that can be supported with the
SpeedSentry DBC.  At this time, Inesonic has not released the source code for
the rollup server; however, the server infrastructure if fairly trivial to
implement, if needed, based on what's already supplied.


Licensing
=========
This code is dual licensed under:

* The Inesonic Commercial License

* The GNU Public License, version 3.0.
