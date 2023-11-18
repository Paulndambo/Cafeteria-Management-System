data = [['first_name', 'last_name', 'email', 'gender', 'id_number', 'phone_number', 'reg_number', 'status', 'student_type'],
        ['Felike', 'Atthowe', 'fatthowe0@behance.net', 'Male', '27746664-5', '805 999 1770', 'JR608188', 'Active', 'Boarder'],
        ['Ernest', 'Rivenzon', 'erivenzon1@china.com.cn', 'Male', '33112291-3', '999 222 5742', 'GP084838', 'Deactivated', 'Boarder'],
        ['Cchaddie', 'Overthrow', 'coverthrow2@friendfeed.com', 'Male', '82873006-6', '868 784 1038', 'JL166772', 'Active', 'Prepaid'],
        ['Gardy', 'Burchard', 'gburchard3@un.org', 'Male', '19448298-4', '919 277 4224', 'AM135432', 'Deactivated', 'Prepaid'],
        ['Hanny', 'Sharland', 'hsharland4@spotify.com', 'Female', '43435629-1', '507 514 0110', 'KH770945', 'Deactivated', 'Prepaid'],
        ['Sally', 'Briddle', 'sbriddle5@goo.gl', 'Female', '64638887-1', '324 216 1438', 'PC818515', 'Active', 'Boarder'],
        ['Anderson', 'Serfati', 'aserfati6@angelfire.com', 'Male', '75864010-9', '271 156 1233', 'RV089955', 'Active', 'One-Time'],
        ['Julianna', 'Hursey', 'jhursey7@miibeian.gov.cn', 'Female', '39065999-3', '724 489 4385', 'NL715175', 'Active', 'One-Time'],
        ['Eugenio', 'Binestead', 'ebinestead8@time.com', 'Male', '00850372-2', '669 802 3726', 'ZQ127878', 'Deactivated', 'Prepaid'],
        ['Kevyn', 'Hedaux', 'khedaux9@trellian.com', 'Female', '09787176-1', '492 628 2028', 'DS905881', 'Deactivated', 'Prepaid']]

# Extract keys from the first sub-list
keys = data[0]

# Create a list of dictionaries using the remaining sub-lists as values
list_of_dicts = [dict(zip(keys, values)) for values in data[1:]]

# Print the resulting list of dictionaries
for entry in list_of_dicts:
    print(entry)
