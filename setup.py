from setuptools import setup, find_packages

setup(
    name='onfon-sms-sender',
    version='0.1.3',
    packages=find_packages(include=['sms_sender', 'sms_sender.*']),
    install_requires=[
        'requests',
        'python-dotenv',],
    entry_points={
        'console_scripts': [
            # Add command-line scripts here if needed
        ],
    },
    include_package_data=True,
    description='A package to send SMS using Onfon Media API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/antonnifo/Onfon-SMS-Sender',
    author='Antonnifo',
    author_email='antonnifo@live.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
