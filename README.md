# AI Agent

Project for boot.dev

This is a toy code-fixing AI Agent.  I wouldn't recommend using it.

In main.py you can define `working_directory` to be the directory that the agent can access.  Be very careful with this setting.  It is set to the `calculator` subdirectory of the repo by default.

Currently the agent used is Google Gemini.  It has access to 4 functions that canoperate on files within the `working_directory` and its subfolders in the following ways:

- View directory contents
- View file contents
- Write/overwrite files (dangerous!)
- Execute python code (dangerous!)

Please use with caution.
