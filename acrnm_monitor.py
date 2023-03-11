import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SENDER_EMAIL, RECEIVER_EMAIL, PASSWORD

url = 'https://acrnm.com/'
filename = './data/links.txt'
wait_time = 60  # seconds

# Get the current list of links
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
links = [a['href'] for a in soup.find_all('a') if a.has_attr('href')]

try:
    # Read the previous list of links from file
    with open(filename, 'r') as f:
        previous_links = f.read().splitlines()
except FileNotFoundError:
    previous_links = []

# Compare the current and previous lists of links
new_links = set(links) - set(previous_links)
if new_links:
    print('New links found:')
    for link in new_links:
        print(link)
        previous_links.append(link)

    # Write the current list of links to file
    with open(filename, 'w') as f:
        for link in links:
            f.write(link + '\n')
    
    # Email notification
    subject = "New links found on ACRNM website"
    body = "\n".join(new_links)
    
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = RECEIVER_EMAIL
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, PASSWORD)
        smtp.send_message(message)
else:
    print('No new links found.')

# Keep checking for new links every 60 seconds
while True:
    time.sleep(wait_time)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a') if a.has_attr('href')]

    # Compare the current and previous lists of links
    new_links = set(links) - set(previous_links)
    if new_links:
        print('New links found:')
        for link in new_links:
            print(link)
            previous_links.append(link)

        # Write the current list of links to file
        with open(filename, 'w') as f:
            for link in links:
                f.write(link + '\n')

        # Email notification
        subject = "New links found on ACRNM website"
        body = "\n".join(new_links)
        
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = RECEIVER_EMAIL
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, PASSWORD)
            smtp.send_message(message)
    else:
        print('No new links found.')
        break
