.. KicadModTree documentation master file, created by
   sphinx-quickstart on Sun Feb 19 20:08:44 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to KicadModTree's documentation!
========================================

KicadModTree is a framework which allows standalone creation KiCAD footprint.


Overview
========

This framework is mainly based on the idea of scripted CAD systems (for example OpenSCAD). This means, everything is a node, and can be structured like a tree.
In other words, you can group parts of the footprint, and translate them in any way you want. Also cloning & co. is no Problem anymore because of this concept.

To be able to create custom Nodes, I separated the system in two parts. Base nodes, which represents simple structures and also be used by KiCAD itself,
and specialized nodes which alter the behaviour of base nodes (for example positioning), or represent a specialized usage of base nodes (for example RectLine).

When you serialize your footprint, the serialize command only has to handle base nodes, because all other nodes are based upon the base nodes.
This allows us to write specialized nodes without worrying about the FileHandlers or other core systems.
You simply create you special node, and the framework knows how to handle it seamlessly.


Datastructures
==============

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   KicadModTree


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
