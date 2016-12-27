from setuptools import setup, find_packages

setup(
        name='lunasane',
        version='0.0.1',
        description='An audio/video editor.',
        author='akayado',
        author_email='akayado@akayado.com',
        url='http://www.akayado.com/',
        packages=find_packages(),
        install_requires=[
            'pyqt5',
            'qtpy',
            'moviepy',
            'numpy',
            'scipy',
            ],
        entry_points="""
        [console_scripts]
        lunasane = lunasane.main:main
        """
        )
