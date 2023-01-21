# FrogWatch USA Data Collection

## Video run-through: https://www.youtube.com/watch?v=w2pvLD0pS7w&ab_channel=Allie

#### Description:
FrogWatch USA is an organization that uses Community Conservation initiatives to gain information about specific fragile ecosystems. (You can learn more about this specific organization here: <https://www.aza.org/frogwatch?locale=en>. Volunteers are trained in the calls of frogs in their specific chapter area, and then go out to a registered survey site at dusk to listen to the frog calls. They then record which frogs they hear, the calling intensity, weather conditions, etc., and submit this information to the organization. FrogWatch USA uses frogs as a metric for environmental health because amphibians are sensative creatures and their presence is a good indicuator of the health of the envioronment. Additionally, frogs have distinct and loud calls, making them easy to track. To lay out an example, I am a part of the FrogWatch chapter in Albany, NY, and my registered survey sites are in the Albany Pine Bush and John Thatcher Park. I go to these locations and, using my training, listen to the calls that I hear to then provide that information to FrogWatch USA. This information helps them track trends in these areas. For example, if we stop hearing calls from the Eastern Spadefoot Frog, we know that there are not enough shallow wetland locations in that ecosystem for that frog to be present, which can help conservationists know where to focus their conservation efforts.

## App Utilization ##
* Volunteers create logins which are managed by a SQL backend.
* Volunteers can register their specific survey sites including GPS coordinates with the built in geo-locator feature.
* Volunteers can submit their watch logs.
  * Historically these have been printed out paper forms which are then mailed into the organization to be added to the database manually. This is cumbersome for both the volunteer, and the data analyst. The purpose of this project is to reduce the barrier to data entry for the valuable information gathered by the volunteers in order to increase the efficieny and scope of the FrogWatch USA conservation efforts. I wanted to do this by making it easier to submit data, easier to organize data, and offer users a mobile option.
  * The log form also includes valueable information about how FrogWatch wants the data collected to help the user in their logs.
  * There are fail-safes on the site which ensure proper data collection, like prohibiting forms from being submitted with empty fields, etc. 
* Volunteers can update their profile information to reflect their location, name, etc.
* Volunteers can view a summary of their logs on the home page.
* The site is mobile compatible so volunteers can log watches as they happen.

FUTURE IMPROVEMENTS:
- Improve the site by adding in a couple more fail safes for data collection (eg: ensuring the user inputs profile info before trying to submit a log, as the profile info is needed to input the SQL data into the database).
- Translate this onto a standard web page (so anyone can use it).
- Create a data analyst version of the site so that the organization can manipulate the data on the site itself instead of downloading a .csv from the SQL database.

Thanks to FrogWatch USA for the helpful training and information which informed this website.

NOTE: All images on the site are ones that I personally took, which is why they don't have markings for copyright or trademark.
