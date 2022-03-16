from setuptools import setup

with open('README.md', 'rt') as f:
    long_description = f.read()

setup(name='guerilla-transform-stack',
      version="0.0.1",
      license='MIT',
      author='Dorian Fevrier',
      url='https://github.com/Narann/guerilla-transform-stack',
      author_email='fevrier.dorian@yahoo.fr',
      description="Manipulate Guerilla transform stack as Python object.",
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords='guerilla, transform, stack',
      packages=['guerilla_transform_stack'],
      package_dir={'': 'src'},
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Operating System :: OS Independent',
      ],
      python_requires='>=2.7',
      options={'bdist_wheel': {'universal': True}},
      )
