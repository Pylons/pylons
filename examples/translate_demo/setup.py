from setuptools import setup, find_packages

setup(
    name='translate_demo',
    version="",
    #description="",
    #author="",
    #author_email="",
    #url="",
    install_requires=["Pylons==dev,>=0.8dev-r292"],
    packages=find_packages(),
    include_package_data=True,
    package_data={'translate_demo': ['i18n/*/LC_MESSAGES/*.mo']},
    entry_points="""
    [paste.app_factory]
    main=translate_demo:make_app
    [paste.app_install]
    main=paste.script.appinstall:Installer
    """,
)