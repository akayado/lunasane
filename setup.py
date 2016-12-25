from setuptools import setup, find_packages

setup(
        name='snipav',
        version='0.0.1',
        description='A audio/video editor.',
        author='akayado',
        author_email='akayado@akayado.com',
        url='http://www.akayado.com/',
        packages=find_packages(),
        entry_points="""
        [console_scripts]
        snipav = snipav.main:main
        """
        )
