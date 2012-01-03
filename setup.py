"""
Setup script for django-sld.

License
=======
Copyright 2011 David Zwarg <dzwarg@azavea.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os, sys
from setuptools import setup, Command

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

class RunTests(Command):
    description = "Run the django test suite."
    user_options = []
    extra_env = {} 
    extra_args = []

    def run(self):
        for env_name, env_value in self.extra_env.items():
            os.environ[env_name] = str(env_value)

        this_dir = os.getcwd()
        sys.path.append(this_dir)
        testproj_dir = os.path.join(this_dir, "djsld/tests")
        os.chdir(testproj_dir)
        sys.path.append(testproj_dir)
        from django.core.management import execute_manager
        os.environ["DJANGO_SETTINGS_MODULE"] = os.environ.get(
            "DJANGO_SETTINGS_MODULE", "settings")
        settings_file = os.environ["DJANGO_SETTINGS_MODULE"]
        settings_mod = __import__(settings_file, {}, {}, [''])
        prev_argv = list(sys.argv)
        try:
            sys.argv = [__file__, "test", "djsld-test"] + self.extra_args
            execute_manager(settings_mod, argv=sys.argv)
        finally:
            sys.argv = prev_argv

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

setup(
    name = "django-sld",
    version = "1.0.4",
    author = "David Zwarg",
    author_email = "dzwarg@azavea.com",
    description = ("A simple django library that generates SLD documents from geographic models."),
    license = "Apache 2.0",
    keywords = "ogc sld geo geoserver mapserver osgeo geodjango",
    url = "http://github.com/azavea/django-sld/",
    requires = ["python_sld", "pysal"],
    packages = ["djsld","djsld.tests","djsld.tests.djsld-test"],
    long_description = read('README.markdown'),
    cmdclass={'test': RunTests},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: GIS"
    ]
)
