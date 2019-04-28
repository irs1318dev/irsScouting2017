# irsScouting2017
irsScouting2017 continues to be developed by the Issaquah Robotics Society (IRS), a FIRST Robotics Competition (FRC) team (see note 1) at Issaquah High School in Issaquah, Washington.

## Purpose
Scouting systems are used by FIRST robotics teams to collect detailed performance data on all robots that participate in a competition. This data is used to make strategy decisions for competition matches and to select other teams for playoff alliances.

## Components
1. Android Application: irsScouting2017 uses an Android client app for data entry. The apps run on six Android tablets (one for each robot in a competition match) that are tethered to a server running on a Windows laptop. The Java code for the Android app is located in the *irs-scout* folder.
2. PostgreSQL Server: All data is written to a PostgreSQL server that runs on the Windows laptop. We use the *Psycopg2* and *sqlalchemy* Python modules for reading and writing to the PostgreSQL database. The database uses a star scheme that can be used for any FRC season without making any schema changes.
3. HTTP Server: The client tablets communicate with the server via Hypertext Transfer Protocol (HTTP). We use the *Cherrypy* Python module for the HTTP server.
4. Data Anaysis: In addition to Structured Query Language (SQL), we use the *Pandas* Python package for data manipulation.
5. Output: We use the *Bokeh* Python package to generate output charts and tables. We also use the *Xlsxwriter* Python package for exporting data to Excel spreadsheets.

## Example Output
Output data from the 2019 season is available at https://irs1318dev.github.io/scouting2019/.

### Notes
1. FIRST stands for ***F**or **I**nspiration and **R**ecognition in **S**cience and **T**echnology*. FIRST's mission is to inspire young people to be science and technology leaders, by engaging them in exciting mentor-based programs that build engineering and technology skills, that inspire innovation, and that foster well-rounded life capabilities including self-confidence, communication, and leadership. Learn more at https://www.firstinspires.org/.
