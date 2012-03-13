from setuptools import setup

setup(
    name='nose_test_timer',
    version='1',
    url='http://github.com/PolicyStat/nose-test-timer',
    author='Kyle Gibson',
    author_email = 'kyle.gibson@policystat.com',
    description = 'Nose plugin to track run times of tests',
    install_requires=['nose'],
    license = 'BSD',
    keywords = 'test unittest nose nosetests plugin debug profile',
    py_modules = ['nose_test_timer'],
    entry_points = {
        'nose.plugins.0.10': [
            'nose_test_timer = nose_test_timer:TestTimer',
        ],
    },
)
