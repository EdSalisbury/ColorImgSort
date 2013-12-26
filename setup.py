from distutils.core import setup

setup(
    name='ColorImgSort',
    version='0.1.0',
    author='Ed Salisbury',
    author_email='ed@edsalisbury.net',
    packages=[],
    scripts=['bin/colorimgsort.py'],
    url='http://pypi.python.org/pypi/ColorImgSort/',
    license='LICENSE.txt',
    description='Sorts images based on color.',
    long_description=open('README.txt').read(),
    install_requires=[
        "PIL >= 1.1.7",
    ],
)
