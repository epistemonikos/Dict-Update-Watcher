import os
from setuptools import setup, find_packages
import subprocess


GIT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".git")
CURRENT_TAG = str(subprocess.check_output(['git', '--git-dir', GIT_PATH, 'tag'])).strip().split('\n')[-1]

setup(
    name='dict_update_watcher',
    version=CURRENT_TAG,
    description="",
    long_description="""
""",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Epistemonikos',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    tests_require=[
        'nose',
        'coverage',
    ],
    test_suite="tests",
    entry_points="""
    # -*- Entry points: -*-
    """,
)
