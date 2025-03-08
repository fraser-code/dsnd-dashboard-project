from pathlib import Path
from setuptools import setup, find_packages

cwd = Path(__file__).resolve().parent
requirements = (
    cwd / 'employee_events' / 'requirements.txt').read_text().split('\n'
                                                                    )

setup_args = dict(
    name='employee_events',
    version='0.1.0',
    description='SQL Query API for employee and team events',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

if __name__ == "__main__":
    setup(**setup_args)
