# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s sc.seo -t test_seo.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src sc.seo.testing.SC_SEO_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_seo.robot
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

Scenario: As a site administrator I can add a SEO
  Given a logged-in site administrator
    and an add seo form
   When I type 'My SEO' into the title field
    and I submit the form
   Then a seo with the title 'My SEO' has been created

Scenario: As a site administrator I can view a SEO
  Given a logged-in site administrator
    and a seo 'My SEO'
   When I go to the seo view
   Then I can see the seo title 'My SEO'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add seo form
  Go To  ${PLONE_URL}/++add++SEO

a seo 'My SEO'
  Create content  type=SEO  id=my-seo  title=My SEO


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the seo view
  Go To  ${PLONE_URL}/my-seo
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a seo with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the seo title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
