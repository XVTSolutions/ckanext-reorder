from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-reorder',
	version=version,
	description="",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='George Sattler',
	author_email='georgesattler at xvt.com.au',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.reorder'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	reorder=ckanext.reorder.plugin:ReorderPlugin
	""",
)
