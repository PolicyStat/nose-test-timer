from setuptools import setup

setup(
    name='ipdbplugin',
    version='1',
    url='http://github.com/PolicyStat/nose-test-timer',
    author='Kyle Gibson',
    author_email = 'kyle.gibson@policystat.com',
    description = 'Nose plugin to track run times of tests',
    install_requires=['nose'],
    license = 'BSD',
    keywords = 'test unittest nose nosetests plugin debug profile',
    py_modules = ['testtimer'],
    entry_points = {
        'nose.plugins.0.10': [
            'testtimer = testtimer:TestTimer',
        ],
    },
)
