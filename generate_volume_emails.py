from jinja2 import Environment, FileSystemLoader
import csv

# Load Jinja2 template
env = Environment(loader=FileSystemLoader('./env'))
template = env.get_template('email_template.md')

# Read CSV file containing affected volumes
with open('./env/volume_details.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Group data by user_email
    user_data = {}
    for row in csv_reader:
        email = row['user_email']
        if email not in user_data:
            # Email does not exist yet, create new entry
            user_data[email] = []
        user_data[email].append(row)

    # Generate email for each user
    for email, volumes in user_data.items():
        print(f'Email: {email}, Volumes: {len(volumes)}')
        if not email:
            print(f'Skipping, because no email found for volumes {volumes}')
            continue
        # Populate template
        email_content = template.render(
            affected_volumes=volumes
        )
        # Write to text file
        with open(f'./env/emails/email_to_{email}.md', 'w') as email_file:
            email_file.write(email_content)
