# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s cerclefolk.core -t test_esdeveniment.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src cerclefolk.core.testing.CERCLEFOLK_CORE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_esdeveniment.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Esdeveniment
  Given a logged-in site administrator
    and an add esdeveniment form
   When I type 'My Esdeveniment' into the title field
    and I submit the form
   Then a esdeveniment with the title 'My Esdeveniment' has been created

Scenario: As a site administrator I can view a Esdeveniment
  Given a logged-in site administrator
    and a esdeveniment 'My Esdeveniment'
   When I go to the esdeveniment view
   Then I can see the esdeveniment title 'My Esdeveniment'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add esdeveniment form
  Go To  ${PLONE_URL}/++add++Esdeveniment

a esdeveniment 'My Esdeveniment'
  Create content  type=Esdeveniment  id=my-esdeveniment  title=My Esdeveniment


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the esdeveniment view
  Go To  ${PLONE_URL}/my-esdeveniment
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a esdeveniment with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the esdeveniment title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
