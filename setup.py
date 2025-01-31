from setuptools import setup, find_packages

setup(
    name='AI Cerberus',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "Flask",
        "llm_guard"
    ],
    author='Leigh Dastey',
    author_email='ldastey@outlook.com',
    description='Services to support AI guardrails using the LLM Guard library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ldastey-dev/ai-cerberus.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
