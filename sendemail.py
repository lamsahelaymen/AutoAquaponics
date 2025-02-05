# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.
import smtplib
import csv
#from main import user_settings
#from main import user_settings
from data import Reader
from datetime import datetime
import os
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def sendEmail(user_settings):
    while True:
        #if not sunday - return
        weekday = datetime.today().weekday()
        time =  datetime.now()
        hour = time.hour
        minute = time.minute
        second = time.second
        
        if weekday == 6 and hour == 12 and minute == 0 and second == 0:
            pass
        else: 
            continue

        config_path, db_path, _ = user_settings()
        with open(config_path, 'r') as file:
            config_settings = list(csv.reader(file))
            strTos = config_settings[3]
            strTos = list(filter(('Email').__ne__, strTos))


        # Define these once; use them twice!
        strFrom = 'nu.urbanagriculture@gmail.com'

        ###########
        
        #we need to edit this so that it takes from GUI
        #we will DEFINITELY have to 'import GUI'

        ###########
        sec_per_week = 7 * 24 * 60 * 60
        tsamp = 1
        nsamp = 10
        information = Reader(db_path,'sensor_db.db').query_by_num(table="SensorData", num= sec_per_week / (tsamp * nsamp)) #num is the number of data points. We need to figure out what num is for a whole week
        #Daniel will apply SQL lite later
    
        def func1(x):
            return x[1:]
        
        information = list(map(func1,information))
        #print('information')
        #print(information)

        param_list = ['pH', 'TDS (ppm)', 'Rela. Humidity (%)', 'Air Temp (\N{DEGREE SIGN}C)', 'Water Temp (\N{DEGREE SIGN}C)', 'Water Level (cm)']
        plt.figure(figsize = (11,8))
        plt.suptitle('Weekly Graphs', fontsize = 20, color='#4e2a84')
        #allOfData = {}
        for i in range(len(param_list)):
            def func2(x):
                return x[i]
            
            partOfInfo = list(map(func2,information))
            #print('part of info')
            #print(partOfInfo)
            #allOfData[param_list[i]] = partOfInfo
            plt.subplot(3,2,1+i)
            plt.plot(partOfInfo, color='#4e2a84')
            plt.title(param_list[i])
            ax = plt.gca()
            ax.axes.xaxis.set_visible(False)
        
        title = 'thisweek.png'

        plt.tight_layout()
        plt.savefig(title)

        avgs = []
        mins = []
        maxs = []
        for i in range(len(param_list)):
            def func2(x):
                return x[i]
            partOfInfo = list(map(func2,information))
            partOfInfo = [x for x in partOfInfo if x]
            avgs.append(round(sum(partOfInfo)/len(partOfInfo), 3))
            mins.append(round(min(partOfInfo), 3))
            maxs.append(round(max(partOfInfo), 3))


        for strTo in strTos:
            # Create the root message and fill in the from, to, and subject headers
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = 'NU-ESW Aquaponics Weekly Update'
            msgRoot['From'] = strFrom
            msgRoot['To'] = strTo
            msgRoot.preamble = 'This is a multi-part message in MIME format.'

            # Encapsulate the plain and HTML versions of the message body in an
            # 'alternative' part, so message agents can decide which they want to display.
            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)

            msgText = MIMEText('This is the alternative plain text message.')
            msgAlternative.attach(msgText)




            
            #num needs to be changed accordingly
            

            # We reference the image in the IMG SRC attribute by the ID we give it below
            #msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
            html = '''
                <head>
                    <style>
                        header {
                            position: fixed;
                            top: 0;
                            left: 0;
                            width: 100%;
                            border: solid 1px #CCC;
                            padding: 10px;
                            color: white;
                            background-color: #4e2a84;
                        }
                        h1 {
                            font-size: 40px;
                        }
                        h3 {
                            font-size: 20px;
                        }
                        header * {
                            padding: 0px;
                            margin: 0px;
                        }
                        h2 {
                            color: #4e2a84;
                            font-size: 30px;
                            text-align: center;
                        }
                        .griddy {
                            max-width: 40%;
                            margin: 0 auto;
                        }
                        .item {
                            font-size: 15px;
                            color: black;
                            width: 22%;
                            float: left;
                            border: solid 1px black;
                            padding: 1%;
                        }
                        .blank {
                            width: 100%;
                        }
                        br {
                            margin: auto;
                        }
                    </style>
                </head>
                <body>
                    <header>
                        <h1>AutoAquaponics</h1>
                        <h3>Weekly Report</h3>
                    </header>
                    <h2>Weekly Statistics</h2>
                    <div class="griddy">
                        <div class="item"><b>Metric</b></div>
                        <div class="item"><b>Average</b></div>
                        <div class="item"><b>Minimum</b></div>
                        <div class="item"><b>Maximum</b></div>
                        <div class="item">pH</div>
                        <div class="item">'''+str(avgs[0])+'''</div>
                        <div class="item">'''+str(mins[0])+'''</div>
                        <div class="item">'''+str(maxs[0])+'''</div>
                        <div class="item">TDS (ppm)</div>
                        <div class="item">'''+str(avgs[1])+'''</div>
                        <div class="item">'''+str(mins[1])+'''</div>
                        <div class="item">'''+str(maxs[1])+'''</div>
                        <div class="item">Humidity (%)</div>
                        <div class="item">'''+str(avgs[2])+'''</div>
                        <div class="item">'''+str(mins[2])+'''</div>
                        <div class="item">'''+str(maxs[2])+'''</div>
                        <div class="item">Air Temp</div>
                        <div class="item">'''+str(avgs[3])+'''</div>
                        <div class="item">'''+str(mins[3])+'''</div>
                        <div class="item">'''+str(maxs[3])+'''</div>
                        <div class="item">Water Temp</div>
                        <div class="item">'''+str(avgs[4])+'''</div>
                        <div class="item">'''+str(mins[4])+'''</div>
                        <div class="item">'''+str(maxs[4])+'''</div>
                        <div class="item">Water Level</div>
                        <div class="item">'''+str(avgs[5])+'''</div>
                        <div class="item">'''+str(mins[5])+'''</div>
                        <div class="item">'''+str(maxs[5])+'''</div>
                    </div>
                    <br><img src="cid:image1"><br>
                </body>
                
            '''
            msgText = MIMEText(html, 'html')
            msgAlternative.attach(msgText)

            # This example assumes the image is in the current directory

            fp = open(title, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            # Define the image's ID as referenced above
            msgImage.add_header('Content-ID', '<image1>')
            msgRoot.attach(msgImage)
            
            
            #otherwise it goes here
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            # Send the email (this example assumes SMTP authentication is required)
            
            email = strFrom
            smtp = 'smtp.gmail.com'
            port = 587
            password = 'Hydroponics1!1'
            server = smtplib.SMTP(smtp, port)

            server.starttls()

            server.login(email,password)
            server.sendmail(email, strTo, msgRoot.as_string())
            

        os.remove(title)
        #return

