import ssl
import socket
import requests
import OpenSSL
from datetime import date

#Input: string with filename to file with websites
#Return: nothing, create files of information
def create_certificate_file(filename):

    f = open(filename, 'r')

    #Creating lits for storing data
    hsts_list = []
    data = []
    dates = []
    
    ssl_errors = []
    req_errors = []
    other_errors = []

    print("\nNew file: " + filename)
    print('Fetching pem-certificates...\n')

    #Check every website in the file
    for website in f:

        #Get url
        website = 'www.' + str(website.strip().lower())
        
        temp = []
        
        try:
            
            #ssl.PROTOCOL_SSLv23
            #Selects SSL version 2 or 3 as the channel encryption protocol.
            #This is a setting to use with servers for maximum compatibility with the other end of an SSL connection,
            #but it may cause the specific ciphers chosen for the encryption to be of fairly low quality.

            #ssl.PROTOCOL_SSLv3
            #Selects SSL version 3 as the channel encryption protocol.
            #For clients, this is the maximally compatible SSL variant.

            #ssl.PROTOCOL_TLSv1
            #Selects TLS version 1 as the channel encryption protocol.
            #This is the most modern version, and probably the best choice for maximum protection, if both sides can speak it.

            #Fetch certificate
            socket.setdefaulttimeout(10)
            certificate = ssl.get_server_certificate((socket.gethostbyname(website), 443), ssl_version = ssl.PROTOCOL_SSLv23)

            #Create certificate-files
            pem = OpenSSL.crypto.FILETYPE_PEM
            cert = OpenSSL.crypto.load_certificate(pem, certificate)
            cert_file = open('certificates\\'+filename[9:-4]+'-'+website+'.txt', 'w')
    
            #Website
            cert_file.write(website + '\n')

            #HSTS or NOT
            req = requests.get('https://' + website)
            if 'strict-transport-security' in req.headers:
                cert_file.write("HSTS" + "\n")
                temp.append(website + ":" + "HSTS" + "\n")
            else:
                cert_file.write("NO HSTS" + "\n")
                temp.append(website + ":" + "NO HSTS" + "\n")

            #Signature algorithm
            cert_file.write(cert.get_signature_algorithm().decode("utf-8") + '\n')
            temp.append(website + ":" + cert.get_signature_algorithm().decode("utf-8") + '\n')

            #Issuer organisation
            cert_file.write(cert.get_issuer().O + '\n')
            temp.append(website + ":" + cert.get_issuer().O + '\n')

            #Public key type and bits, types: 6 = RSA, 116 = DSA, 408 = EC
            key_type = cert.get_pubkey().type()
            if key_type == 6:
                cert_file.write('RSA ' + str(cert.get_pubkey().bits()) + '\n')
                temp.append(website + ":" + 'RSA ' + str(cert.get_pubkey().bits()) + '\n')
            elif key_type == 116:
                cert_file.write('DSA ' + str(cert.get_pubkey().bits()) + '\n')
                temp.append(website + ":" + 'DSA ' + str(cert.get_pubkey().bits()) + '\n')
            elif key_type == 408:
                cert_file.write('EC ' + str(cert.get_pubkey().bits()) + '\n')
                temp.append(website + ":" + 'EC ' + str(cert.get_pubkey().bits()) + '\n')
            
            #Close certificate file
            cert_file.close()
            
            #Store certificate data
            data.append(temp)

            #Store the certificate dates
            dates.append([])
            dates[-1].append(website)
            
            #Certificate startdate
            start = cert.get_notBefore().decode("utf-8")
            y = int(start[:4])
            m = int(start[4:6])
            d = int(start[6:8])
            dates[-1].append(date(y,m,d))
            
            #Certificate enddate
            end = cert.get_notAfter().decode("utf-8")
            y = int(end[:4])
            m = int(end[4:6])
            d = int(end[6:8])
            dates[-1].append(date(y,m,d))

            
        except ssl.SSLError as e:
            ssl_errors.append(website)
            print('\nssl:')
            print(website + ' failed.')

        except requests.exceptions.SSLError as e:
            req_errors.append(website)
            print('\nreq:')
            print(website + ' failed.')
        
        #ConnectionRefusedError, ConnectionResetError or TimeoutError etc  
        except Exception as e:
            other_errors.append(website + ":" + str(type(e)))
            print('\n' + website + ' failed.')

    f.close()
    failures = len(ssl_errors)  + len(req_errors) + len(other_errors)

    #Print summary
    print('\nTotal number of SSL Errors: ' + str(len(ssl_errors)) + '.')
    print('Total number of Request Errors: ' + str(len(req_errors)) + '.')
    print('Total number of other errors: ' + str(len(other_errors)) + '.')
    print(str(len(data)) + ' successful certificates, ' + str(failures)  + ' websites failed.')
    print('Done fetching and saving certificates.')

    #Write certificate data to file
    create_data_file(filename, data)

    #Write errors to files
    create_error_file(filename, ssl_errors, "SSL")
    create_error_file(filename, req_errors, "REQ")
    create_error_file(filename, other_errors, "OTHER")

    #Write dates to file
    create_date_file(filename, dates)

    #Write stats to file
    create_stat_file(filename, len(ssl_errors), len(req_errors), len(other_errors))



#Input: filename, list of errors and string with type of error
#Return: nothing, create file with information about the errors
def create_error_file(filename, errors, error_type):

    #Open file
    error_file = open('errors\\' + filename[9:-4] + '-' + error_type + '-errors.txt', 'w')

    #Write information about the errors to file
    error_file.write('Total number of ' + error_type + ' errors:' + str(len(errors)) + '\n')
    error_file.write('\n')

    #Add each website with errors to file
    for domain in errors:
        error_file.write(domain + '\n')

    #Close the file     
    error_file.close()
    print('\n' + filename[9:-4] + '-' + error_type + '-errors.txt are ready.')   



#Input: string with filename and list with data
#Return: nothing, create file with information about the data
def create_data_file(filename, data):

    #Open file
    data_file = open('data\\' + filename[9:-4] + '-data.txt', 'w')

    #Write all data about websites to file
    for i in range(len(data[0])):
        for j in range(len(data)):
            data_file.write(data[j][i])
        data_file.write('\n')

    #Close the file
    data_file.close()
    print('\n' + filename[9:-4] + '-data.txt are ready.')



#Input: string with filename and list with dates
#Return: nothing, create file with information about the dates
def create_date_file(filename, dates):

    #Open file
    date_file = open('dates\\' + filename[9:-4] + '-dates.txt', 'w')

    #Sort the file
    dates = list(reversed(sort_tuples(dates, 2)))

    #Write every date to file
    for d in dates:
        date_file.write(d[0] + ':' + str(d[1]) + ':' + str(d[2]) + '\n')

    #Close the file      
    date_file.close()
    print('\n' + filename[9:-4] + '-dates.txt are ready.')   



#Input: list of tuples of data
#Return: list of sorted tubles with data
def sort_tuples(data_list, pos):
    
    #Sort list depending on second pos value
    for i in range(len(data_list)):
            for j in range(1,len(data_list)):
                
                #Greatest element first in list
                if data_list[j-1][pos] < data_list[j][pos]:
                    temp = data_list[j-1]
                    data_list[j-1] = data_list[j]
                    data_list[j] = temp

    #Return the sorted list
    return data_list



#Input: string with filename and number of different errors
#Return: nothing, create file with information with statistics
def create_stat_file(filename, a, b, c):

    #Open file
    f = open('data\\' + filename[9:-4] + '-data.txt', 'r')

    #Create lists to store data
    data = [[]]
    stat = []

    #Read all the data and add to list
    for line in f:
        if line == '\n':
            data.append([])
        else:
            data[-1].append(line.strip('\n').split(":")[1])
 
    #Go through all categories
    for category in data:
        data_set = set(category)
        data_list = []

        #Count number of distinct elements and add to list
        for element in data_set:
            data_list.append((element, category.count(element)))

        #Add information to list and add a dummy point
        stat.extend(sort_tuples(data_list),1)
        stat.append((0,0))

    #Open stat file
    f = open('stat\\' + filename[9:-4] + '-stat.txt', 'w')

    #Write information about the errors to the file
    f.write("SSL errors:" + str(a) + "\n")
    f.write("REQ errors:" + str(b) + "\n")
    f.write("Other errors:" + str(c) + "\n")
    f.write("Total number of errors:" + str(a+b+c) + "\n\n")

    #Go througf every data-tuple in the lsit
    for tup in stat:
        #Write the information to the file
        if tup == (0,0):
            f.write('\n')
        else:
            f.write(tup[0] + ':' + str(tup[1]) + '\n')

    #Close the file
    f.close()
    print('\n' + filename[9:-4] + '-stat.txt are ready.')
