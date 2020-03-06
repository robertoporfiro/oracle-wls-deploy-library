
# The customization file to execute after the import.
#Note: if different customization files are used for each environment, this setting MUST be moved to an envrionment
#CUSTOMIZATION_FILE = "common.Customization.xml"


# Session ID and Name
SESSION_ID          = "OSB_PROJECT_NAME_Deployment"
SESSION_DESCRIPTION = "Automated OSB Configuration Import - OSB_PROJECT_NAME"

# Eclipse Project Name
SOURCE_PROJECT_NAME = "OSB_PROJECT_NAME"

# ALSB folder under which the eclipse project needs to be imported. The first node(for example, Common) is the ALSB project
#NOTE: If the target folder is different per environment or per deployment, this property MUST be moved to an environment specific config.py like SIT1.config.py
TARGET_FOLDER_NAME = ""

# Boolean with true or false tells whether the ALSB project needs be deleted and recreated or just updated
RECREATE_TARGET_PROJECT = "true"

# ALSB Project description
PROJECT_DESCRIPTION = "This is a test of the build deploy system."

#ALSB folder description
FOLDER_DESCRIPTION = "Folder Description"
